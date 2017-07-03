#! /usr/bin/env python
"""SQL as a Service"""
from json import loads
from os import environ as env
from traceback import format_exc

from flask import Flask, request, jsonify
from sqlalchemy.exc import ProgrammingError, OperationalError
from pynamodb.exceptions import (
    QueryError,
    GetError,
    DeleteError,
    DoesNotExist
)

from engine import SqlClient
from jinja2 import Environment
from models import Backend
from middleware import list_routes
from ..utils import decrypt

api = Flask(__name__)

def raise_if_not_exists(model):
    if not model.exists():
        raise DoesNotExist()

@api.errorhandler(Exception)
def exception_handler(error):
    # type: (Exception) -> Exception
    """Show uncaught exceptions.

    Args:
        error

    Raises:
        Exception
        """
    raise Exception(format_exc())

@api.route('/')
def list_api_routes():
    """List all endpoints"""
    return jsonify(list_routes(api))

@api.route('/backend/list')
def get_backends():
    raise_if_not_exists(Backend)
    return ''.join({item.name:
                    item.description
                    for item in Backend.scan()})

@api.route('/register/<backend>', methods=['POST'])
def register_backend(backend):
    """See client.py to generate new backends."""

    if not Backend.exists():
        print('Creating table Backend for item: %s' % backend)
        Backend.create_table(wait=True)

    json = request.json
    credentials = json['credentials']
    description = json['description']

    new_backend = Backend(
        name=backend,
        description=description,
        credentials=credentials,
    )
    new_backend.save()
    return jsonify("""{backend}: {description} has been registered.
              Run ./scripts/sqlcmd to run SQL
            """.format(backend=backend, description=description)
    )


@api.route('/backend/<backend>', methods=['DELETE'])
def delete_backend(backend):
    raise_if_not_exists(Backend)
    items = Backend.query('name', name__eq=backend)
    for item in items:
        try:
            item.delete()
        except DeleteError as err:
            return err
    return jsonify("%s has been deleted" % backend)


def _get_credentials(backend):
    raise_if_not_exists(Backend)
    backend_results = {item.name: item.credentials
                       for item in Backend.query('name', name__eq=backend)}
    return backend_results[backend]


def _format_sql(sql, sql_params):
    return Environment(autoescape=True).from_string(
        sql).render(json.loads(sql_params))


def _connect(backend, key, autocommit):
    credentials = _get_credentials(backend)
    backend_client = SqlClient(decrypt(credentials, key=key), autocommit)
    return backend_client.sql_client()


def _sql_cmd(client, sql):
    try:
        return client(sql)
    except ProgrammingError as err:
        return str(err), 400
    except OperationalError as err:
        return str(err), 400
    except Exception as err:
        return str(err), 400

@api.route('/view/<backend>', methods=['GET'])
def view_sql(backend):
    """View data from database.

    By default, thise route runs in autocommit false.

    Args:
        sql: Valid sql for your backend
        sql_params: Optional jinja2 params

    Returns:
        json
    """
    key = request.headers['x-api-key']
    args = request.args
    sql = args['sql']
    sql_params = args.get('sql_params', '{}')
    autocommit = False

    client = _connect(backend, key, autocommit)
    rendered_sql = _format_sql(sql, sql_params)
    results = _sql_cmd(client, rendered_sql)

    return jsonify([(dict(row.items())) for row in results])


@api.route('/execute/<backend>', methods=['POST'])
def execute_sql(backend):
    """Modify data from the database.

    Args:
        sql: valid sql for your backend
        sql_params: Optional jinja2 params

    Returns:
        json
    """
    key = request.headers['x-api-key']
    args = request.json
    sql = args['sql']
    sql_params = args.get('sql_params', '{}')
    autocommit = args.get('autocommit', False)

    client = _connect(backend, key, autocommit)
    rendered_sql = _format_sql(sql, sql_params)
    results = _sql_cmd(client, rendered_sql)

    return jsonify(str("%s row(s) affected." % results.rowcount))


if __name__ == '__main__':
    DEBUG = False if env['STAGE'] == 'prod' else True
    api.run(debug=DEBUG, port=5001)
