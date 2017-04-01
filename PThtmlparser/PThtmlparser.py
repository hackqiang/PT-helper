import logging

import http
from nexusphp import nexusphp


class PThtmlparser():
    def __init__(self, host, type, https):
        self.parser = None
        if type == 'NexusPHP':
            self.parser = nexusphp(host, https)
        else:
            logging.error('not support type %s' % type)
            raise Exception('not support type %s' % type)


    def signin(self):
        if self.parser:
            self.parser.sync_cookie()
            return self.parser.signin()

    def search(self, keywords):
        if self.parser:
            self.parser.sync_cookie()
            return self.parser.search(keywords)

    def get_user_info(self):
        '''
            return (True, upload_siz, download_size, coin)
        '''
        if self.parser:
            self.parser.sync_cookie()
            return self.parser.get_user_info()
        else:
            return False, '', '', ''
