#! /usr/bin/env python2
from os import environ as env
import random
import string
from sys import argv
from subprocess import check_output


def initialize_docker():
    """Initialize docker for sql server on linux.

    Be sure to have your environment variables set
    for MSSQL_PASSWORD
    """
    check_output("docker run -e 'ACCEPT_EULA=Y' -e 'SA_PASSWORD=%s'"
                " -p 1433:1433 -d microsoft/mssql-server-linux"
                % env['MSSQL_PASSWORD'], shell=True
    )

def seed_database():
    check_output(
        'sqlcmd -S $MSSQL_HOST '
        '-U $MSSQL_USER -P $MSSQL_PASSWORD '
        '-i ./scripts/init.sql', shell=True
    )

def initialize_process():
    initialize_docker()
    seed_database()

def destroy_tables():
    check_output(
        'sqlcmd -S $MSSQL_HOST '
        '-U $MSSQL_USER -P $MSSQL_PASSWORD '
        '-i ./scripts/destroy.sql', shell=True
    )

def generate_secret(size=64):
    return ''.join(
        random.SystemRandom().choice(
        string.ascii_letters + string.digits)
        for _ in range(size)
    )

if __name__ == '__main__':
    args = {'init': initialize_process,
            'docker': initialize_docker,
            'seed': seed_database,
            'destroy': destroy_tables,
            'secret': generate_secret,
        }
    print(args[argv[1]]())

