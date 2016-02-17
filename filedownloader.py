import os
import sys
import urllib
import urlparse
from time import sleep

class UrlRetriever(urllib.FancyURLopener):
    """
     urlretrieve()のエラー補足用クラス
    """
    def __init__(self):
        self.info = None
        urllib.FancyURLopener.__init__(self)

    # override
    def http_error_default(self, url, fp, errcode, errmsg, headers):
        self.info = urllib.addinfourl(fp, headers, "http:" + url, errcode)
        return self.info

    # must call this method after called URLopener.retrieve()
    def get_errorcode(self):
        if self.info == None :
            return 0

        return self.info.getcode()

class FileDownloader(object):
    DOWNLOAD_SUCCESS =  0
    DOWNLOAD_FAILED  = -1

    def __init__(self, download_path=''):
        self.retriever = UrlRetriever()
        self.host      = ''
        self.url       = ''
        self.byte      = 0
        self.total     = 0
        self.outlen    = 0

        self.download_path = download_path
        self.download_list = list()
        self.download_file = ''

        self.cb_inst = None
        self.cb_func = None

    def setup(self, download_path=''):
        self.download_path = download_path

    def add_source(self, path, filename):
        """
          Add download source for test
        """
        base_url = urlparse.urljoin(self.host, path)
        url = urlparse.urljoin(base_url, filename)

        source = dict(url=url, filename=filename)

        self.download_list.append(source)

    def add_url(self, url, pkgname=''):
        """
          Add download URL
        """
        scheme, host, path, query, fragment = urlparse.urlsplit(url)
        filename = path.split('/')[-1]

        source = dict(url=url, filename=filename, pkgname=pkgname)

        self.download_list.append(source)

    def run(self):
        for s in self.download_list :
            self._download_file(s['url'], s['filename'], s['pkgname'])
        
        # Clear download list
        del self.download_list[:]

    def register_callback(self, inst, func):
        """
          Register a callback function for notice of download complete
        """
        self.cb_inst = inst
        self.cb_func = func

    def _download_file(self, url, filename, pkgname=''):
        result = ''
        self.url = url
        self.download_file = pkgname
        self.total = 0
        self.byte  = 0

        #print 'Fetch %s from [%s]' % (pkgname, self.url)
        filepath = os.path.join(self.download_path, filename)

        self.retriever.retrieve(url, filepath, reporthook=self._cb_download_progress)
        b, ecode = self._is_connected()

        self._clear_stdout()
        if b == True:
            # Calculate the download size
            dlsize = round(int(os.path.getsize(filepath)) / 1024.0, 1)
            size = '{:,.1f}'.format(dlsize)

            out = '\r' + '=> Done' + ' [' + filename + '] ' + str(size) + ' kB\n'
            result = self.DOWNLOAD_SUCCESS

        else :
            out = '\r' + 'HTTP Error(' + str(ecode) + ') [' + url + ']\n'
            result = self.DOWNLOAD_FAILED

        sys.stdout.write(out)

        # Send download complete message
        if self.cb_inst != None and self.cb_func != None:
            self.cb_func(self.cb_inst, pkgname, result)

    def _cb_download_progress(self, count, blocksize, totalsize):
        """
          show progress bar
        """
        self.byte += blocksize
        self.total = totalsize

        readsize = '{:,d}'.format(self.byte / 1024)
        total    = '{:,.1f}'.format(self.total / 1024.0)

        dn = len(str(total))

        per = 100 * count * blocksize / totalsize
        out = '\r' + 'Downloading ' + str(per).rjust(3) + '%' + ' [' + self.download_file + '] ' + str(readsize).rjust(dn) + ' kB/' + str(total) + ' kB'

        sys.stdout.write(out)
        sys.stdout.flush()
        self.outlen = len(out)

    def _is_connected(self):
        ecode = self.retriever.get_errorcode()
        if (ecode > 0):
            return False, ecode
        return True, 200

    def _clear_stdout(self):
        sys.stdout.flush()
        sys.stdout.write('\r')
        sys.stdout.write(' ' * self.outlen)
