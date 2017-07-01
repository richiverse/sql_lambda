from flask_wtf import FlaskForm
from wtforms import (
    TextField,
    PasswordField,
    SelectField,
    IntegerField,
    SubmitField,
)
from wtforms.validators import Required, URL, Length, Regexp, NumberRange
from wtforms.widgets import TextArea

class BackendRegistrationForm(FlaskForm):
    #api_gateway_url = TextField(
    #    'API Gateway URL',
    #    validators=[
    #        Required(),
    #        URL(),
    #    ]
    #)
    api_key = PasswordField(
        'API Gateway key',
        validators=[Required()],
        description='An AWS admin would have given you this key.'
    )
    backend = TextField(
        'Backend',
        validators=[
            Required(),
            Length(max=64),
            Regexp('^[a-zA-Z_]+$'),
        ],
        description='Provide a descriptive name for this unique backend.'
    )
    description = TextField(
        'Description',
        validators=[
            Required(),
            Length(min=16, max=1024),
        ],
        widget=TextArea(),
        description='Please enter a description for this backend'
    )
    dialect = SelectField(
        'Dialect',
        choices=[
            ('mssql', 'SQL Server'),
            ('postgres', 'Postgres'),
            ('redshift', 'Redshift'),
        ]
    )
    driver = SelectField(
        'Driver',
        choices=[
            ('pymssql', 'pymssql'),
            ('psycopg2', 'psycopg2'),
        ]
    )
    host = TextField(
        'Database Host',
        validators=[
            Required(),
        ]
    )
    username = TextField(
        'User Name',
        validators=[
            Required(),
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            Required(),
        ]
    )
    database = TextField(
        'Database',
        validators=[
            Required(),
            Regexp('^[a-zA-Z0-9_-]+$'),
        ]
    )
    port = IntegerField(
        'Port',
        validators=[
            Required(),
            NumberRange(min=1024, max=65535),
        ]
    )
    submit = SubmitField('Register Backend')
