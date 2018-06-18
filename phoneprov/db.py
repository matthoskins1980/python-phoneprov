from sqlalchemy import create_engine, event
from sqlalchemy.pool import QueuePool
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import sqlalchemy.exc
from .config import Config

c = Config(config_filename="~/.phoneprov/config.json")
print(c)
Session = sessionmaker()
sqla_base = declarative_base()
schema_name = ''
sqla_url = c.sqla_url

def get_session( echo=False, poolclass=None, *args ):
    if not args:
        _sqla_url = sqla_url
    else:
        _sqla_url = argv[0]

    if not poolclass:
        poolclass = QueuePool

    e = create_engine(_sqla_url, echo=echo, pool_recycle=1800, poolclass=poolclass, pool_size=10, max_overflow=25)
    Session.configure(bind=e)

    return scoped_session(Session)

def do_commit( sqla, attempts=3 ):
    while attempts > 0:
        attempts -= 1
        try:
            return sqla.commit()
        except sqlalchemy.exc.DBAPIError as exc:
            if attempts > 0 and exc.connection_invalidated:
                sqla.rollback()
            else:
                raise

