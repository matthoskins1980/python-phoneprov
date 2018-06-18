from ..models import *
from ..db import sqla_base, sqla_url
import sqlalchemy as sa

def drop_database():
    print("dropping database...")
    e = sa.create_engine(sqla_url, echo=True, pool_recycle=1800, poolclass=sa.pool.QueuePool)
    sqla_base.metadata.drop_all(e)

if __name__ == '__main__':
    drop_database()

