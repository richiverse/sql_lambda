#! /usr/bin/env python
from os import urandom, environ as env
from traceback import format_exc

from flask import Flask, flash, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from markupsafe import escape
import requests

from forms.register_backend import BackendRegistrationForm
from ..utils import encrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = urandom(64).encode('hex')
csrf = CSRFProtect(app)
Bootstrap(app)

@app.errorhandler(Exception)
def exception_handler(error):
    # type: (Exception) -> Exception
    """Show uncaught exceptions.

    Args:
        error

    Raises:
        Exception
        """
    raise Exception(format_exc())

def _process_backend_registration_form_data(data):
    api_key = data.pop('api_key')
    backend = data.pop('backend')
    description = data.pop('description')
    credentials = encrypt(dict(
        dialect=data['dialect'],
        driver=data['driver'],
        host=data['host'],
        username=data['username'],
        password=data['password'],
        database=data['database'],
        port=data['port'],
    ),key=api_key)

    api_url=env['SQL_%s_URL' % env['STAGE'].upper()]
    url = dict(api_url=api_url, backend=backend)
    endpoint = '{api_url}/register/{backend}'.format(**url)
    json = dict(credentials=credentials, description=description)
    headers = {'x-api-key': api_key}

    response = requests.post(endpoint,json=json, headers=headers)
    return response.json()


@app.route('/register/backend', methods=['GET', 'POST'])
def register_backend():
    form = BackendRegistrationForm()

    if form.validate_on_submit():
        processed = _process_backend_registration_form_data(form.data)
        flash(escape(processed))

        return redirect(url_for('index'))

    return render_template('register_backend.html', form=form)

@app.route('/')
def index():
    return render_template('index.html', stage=env['STAGE'])

if __name__ == '__main__':
    DEBUG = False if env['STAGE'] == 'prod' else True
    app.run(debug=DEBUG)
