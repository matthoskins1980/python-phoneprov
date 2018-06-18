from sqlalchemy import create_engine, event
from sqlalchemy.pool import QueuePool

def vm_view():

    sqla_url = "mysql://engineering:timeout@npg-asterisk-app.npgco.com/realtime_asterisk"

    e = create_engine(sqla_url, echo=True, pool_recycle=1800, poolclass=QueuePool, pool_size=10, max_overflow=25)
    with e.connect() as conn:
        rs = conn.execute("SELECT mailbox, lastname, firstname, location FROM view_directory WHERE lastname_key='467' AND location='10.160.220.5' ORDER BY lastname, firstname")

        for row in rs:
            print(row)

vm_view()
