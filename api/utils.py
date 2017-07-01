from os import environ as env
from functools import partial
import random
import string

from jose import jwt

encrypt = partial(
    jwt.encode,
    algorithm='HS256'
)
decrypt = partial(
    jwt.decode,
    algorithms=['HS256'],
    options={'verify_signature': False}
)
