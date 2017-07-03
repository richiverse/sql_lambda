from functools import partial

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
