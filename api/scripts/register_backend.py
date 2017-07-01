#! /usr/bin/env python2
"""This script serves as a client example of registering a backend.
Your credentials are encrypted prior to transport and your api gateway key
is used to encrypt and validate you as a user on the other end.
"""
from functools import partial
from os import environ as env, path
import sys
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

import requests

from utils import encrypt

def prompt_user_for_credentials():
    return dict(
        dialect=raw_input('dialect: mssql | postgres | redshift for example '),
        driver=raw_input('driver: pymssql | psycopg2 | asyncpg for example '),
        host=raw_input('host: server this database resides on '),
        username=raw_input('username: '),
        password=raw_input('password: '),
        database=raw_input('database: '),
        port=raw_input('port: '),
    )

def register_backend(backend, description, credentials, deployed_url, api_key):
    endpoint = (
        '{app_endpoint}/sql/register/{backend}'
        .format(app_endpoint=deployed_url, backend=backend)
    )
    json = dict(credentials=credentials,
                description=description)
    headers = {'x-api-key': api_key}
    if env['STAGE'] != 'prod':
        print("http {endpoint} x-api-key:{api_key} "
              "credentials={credentials} "
              'description="{description}"\n\n'
              .format(endpoint=endpoint,
                      api_key=api_key,
                      credentials=credentials,
                      description=description)
              )
    try:
        response = requests.post(endpoint, json=json, headers=headers)
    except Exception as err:
        print(err)
    return response.json

def main():
    deployed_url = raw_input('Zappa URL: ')
    api_key = raw_input('API Key: ')
    backend = raw_input('Backend: Reference name for your backend ')
    description = raw_input('Description: ')
    encrypted_credentials = encrypt(prompt_user_for_credentials(), key=api_key)
    print(register_backend(
        backend,
        description,
        encrypted_credentials,
        deployed_url,
        api_key)
    )

if __name__ == '__main__':
    main()
