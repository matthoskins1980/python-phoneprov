from jinja2 import Environment
from sqlalchemy.orm.exc import NoResultFound
from fbtftp.base_handler import ResponseData
from io import StringIO
from ..db import get_session
from ..models import Phone
from ..config import Config

import os
import errno

sqla = get_session()
config = Config()

class SCCPResponseData(ResponseData):
    def __init__(self, mac_address):
        self._mac_address = mac_address
        self._template = self.get_template()

        if self._template:
            self._size = len(self._template.encode('latin-1'))
            self._reader = StringIO(self._template)
        else:
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), self._mac_address)

    def get_template(self):
        q = sqla.query( Phone ).filter( Phone.mac_address == self._mac_address )
        try:
            p = q.one()
        except NoResultFound as exc:
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), self._mac_address)

        t = Environment().from_string( p.template ).render( phone=p, config=config )

        return t

    def read(self, n):
        return bytes(self._reader.read(n).encode('latin-1'))

    def size(self):
        return self._size

    def close(self):
        pass

class FileResponseData(ResponseData):
    def __init__(self, path):
        self._size = os.stat(path).st_size
        self._reader = open(path, 'rb')

    def read(self, n):
        return self._reader.read(n)

    def size(self):
        return self._size

    def close(self):
        self._reader.close()
