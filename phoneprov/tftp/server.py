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
#    counters = stats.get_and_reset_all_counters()
#    print('Server stats - every {} seconds'.format(stats.interval))
#    print(counters)

class DynamicAndStaticHandler(BaseHandler):
    regexes = [
        {
            'regex': '^([0-9a-fA-F]{12})\.cnf\.xml',
            'handler': SCCPResponseData
        }
    ]

    def __init__(self, server_addr, peer, path, options, root, stats_callback, config):
        self._root = root
        self.config = config
        super().__init__(server_addr, peer, path, options, stats_callback)

    def get_response_data(self):
        if os.path.isfile( os.path.join(self._root, self._path)):
            return FileResponseData(os.path.join(self._root, self._path))

        for regex in self.regexes:
            m = re.match( regex.get('regex', ''), os.path.basename(self._path) )
            if m: return regex.get('handler')(self.config, *m.groups())

        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), self._path)

class DynamicAndStaticServer(BaseServer):
    def __init__(self, address, port, retries, timeout, root,
                 handler_stats_callback, server_stats_callback=None):
        self.config = Config()
        self._root = root
        self._handler_stats_callback = handler_stats_callback
        super().__init__(address, port, retries, timeout, server_stats_callback)

    def get_handler(self, server_addr, peer, path, options):
        return DynamicAndStaticHandler(
            server_addr, peer, path, options, self._root,
            self._handler_stats_callback, self.config)

def main():
    server = DynamicAndStaticServer('0.0.0.0', 1069, 3, 5,
                          '/var/tftproot', print_session_stats,
                          print_server_stats )
    try:
        server.run()
    except KeyboardInterrupt:
        server.close()

if __name__ == '__main__':
    main()
