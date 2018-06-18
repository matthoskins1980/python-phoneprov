from fbtftp.base_handler import BaseHandler
from fbtftp.base_server import BaseServer
from .datahandlers import *
from ..config import Config

import os
import re

def print_session_stats(stats):
    pass

def print_server_stats(stats):
    pass

class DynamicAndStaticHandler(BaseHandler):
    regexes = [
        {
            'regex': '^SEP([0-9a-fA-F]{12})\.cnf\.xml',
            'handler': SCCPResponseData
        }
    ]

    def __init__(self, server_addr, peer, path, options, root, stats_callback):
        self._root = root
        super().__init__(server_addr, peer, path, options, stats_callback)

    def get_response_data(self):
        if os.path.isfile( os.path.join(self._root, self._path)):
            return FileResponseData(os.path.join(self._root, self._path))

        for regex in self.regexes:
            m = re.match( regex.get('regex', ''), os.path.basename(self._path) )
            if m: return regex.get('handler')(*m.groups())

        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), self._path)

class DynamicAndStaticServer(BaseServer):
    def __init__(self, address, port, retries, timeout, root,
                 handler_stats_callback, server_stats_callback=None):
        self._root = root
        self._handler_stats_callback = handler_stats_callback
        super().__init__(address, port, retries, timeout, server_stats_callback)

    def get_handler(self, server_addr, peer, path, options):
        return DynamicAndStaticHandler(
            server_addr, peer, path, options, self._root,
            self._handler_stats_callback)

def main():
    from argparse import ArgumentParser

    parser = ArgumentParser(description="Phoneprov TFTP file server")
    parser.add_argument( 'tftproot', default='/var/tftpboot', help="directory to serve files from [/var/tftpboot]")
    parser.add_argument( '--host', default='0.0.0.0', help="Address to listen on [0.0.0.0]" )
    parser.add_argument( '--port', default='69', help="Port to listen on [69]" )
    parser.add_argument( '--retries', default='3', help="Number of retries before failing connection [3]" )
    parser.add_argument( '--timeout', default='5', help="Seconds to wait before resending packets [5]" )

    args = parser.parse_args()

    server = DynamicAndStaticServer(args.host, int(args.port), int(args.retries), int(args.timeout),
                          args.tftproot, print_session_stats,
                          print_server_stats )

    try:
        server.run()
    except KeyboardInterrupt:
        server.close()

if __name__ == '__main__':
    main()
