from ..models import *
from ..db import sqla_base, sqla_url
import sqlalchemy as sa

def create_database():
    print("creating database...")
    e = sa.create_engine(sqla_url, echo=True, pool_recycle=1800, poolclass=sa.pool.QueuePool)
    sqla_base.metadata.create_all(e, checkfirst=True)

if __name__ == '__main__':
    create_database()

