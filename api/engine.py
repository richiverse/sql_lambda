"""Engine Builder."""
from sqlalchemy import create_engine

def _create_engine(engine, autocommit=True):
    """Return an engine from standard format."""
    base_con_str = (
        '{dialect}+{driver}://{username}:{password}@{host}'
        ':{port}/{database}').format(**engine)

    return create_engine(
        base_con_str,
        execution_options=dict(autocommit=autocommit))


class SqlClient(object):
    """SQL Client for any engine in ENGINES.

    >>> redshift = SqlClient('REDSHIFT')
    >>> viewer = redshift.sql_client()
    >>> viewer('select * from table;')
    """

    def __init__(self, engine, autocommit=True):
        """Just need engine from ENGINES object."""
        self.engine = _create_engine(engine, autocommit)

    def sql_client(self):
        """Convenience function to view query results."""
        return self.engine.execute
