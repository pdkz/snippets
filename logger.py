#!/usr/bin/env python

import inspect
import logging

class Singleton(object):
    def __new__(cls, *args, **kwargs) :
        if '_inst' not in vars(cls) :
            cls._inst = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._inst

class Logger(Singleton):
    def __init__(self, loglevel=logging.DEBUG):
        filelogfmt = '%(asctime)s [%(levelname)8s] %(message)s'
        strmlogfmt = '%(message)s'

        filefmt = logging.Formatter(filelogfmt)
        strmfmt = logging.Formatter(strmlogfmt)

        fh = logging.FileHandler('test.log', 'a+')
        sh = logging.StreamHandler()

        fh.setFormatter(filefmt)
        sh.setFormatter(strmfmt)
        
        fh.setLevel(logging.INFO)
        sh.setLevel(logging.DEBUG)

        self.log = logging.getLogger(__name__)
        self.log.setLevel(loglevel)

        self.log.addHandler(fh)
        self.log.addHandler(sh)

        self.logfuncs = {'debug' : self.log.debug,
                         'info'  : self.log.info,
                         'warn'  : self.log.warn,
                         'error' : self.log.error,
                         'fatal' : self.log.fatal }
    @classmethod
    def initialize(cls):
        cls._inst = Logger()

    @classmethod
    def get_instance(cls):
        if '_inst' not in vars(cls) :
            return None
        return cls._inst

    @staticmethod
    def save_message(level, msg, filename='', line=0, *args, **kwrgs):
        d = {'file': '', 'line': 0}
        if level == 'error' or level == 'fatal':
            d['file'] = 'in ' + filename
            d['line'] = ', line ' + str(line)
        
        _inst = Logger.get_instance()
        _inst.logfuncs[level](msg, extra=d)

def LOGD(msg, depth=0, *args): Logger.save_message('debug', msg, filename=inspect.currentframe(depth+1).f_code.co_filename, line=inspect.currentframe(depth+1).f_lineno, args=args)
def LOGI(msg, depth=0, *args): Logger.save_message('info',  msg, filename=inspect.currentframe(depth+1).f_code.co_filename, line=inspect.currentframe(depth+1).f_lineno, args=args)
def LOGW(msg, depth=0, *args): Logger.save_message('warn',  msg, filename=inspect.currentframe(depth+1).f_code.co_filename, line=inspect.currentframe(depth+1).f_lineno, args=args)
def LOGE(msg, depth=0, *args): Logger.save_message('error', msg, filename=inspect.currentframe(depth+1).f_code.co_filename, line=inspect.currentframe(depth+1).f_lineno, args=args)
def LOGF(msg, depth=0, *args): Logger.save_message('fatal', msg, filename=inspect.currentframe(depth+1).f_code.co_filename, line=inspect.currentframe(depth+1).f_lineno, args=args)

if __name__ == '__main__':
    Logger.initialize()

    LOGD('debug %d' % 10)
    LOGI('info')
    LOGW('warn')
    LOGE('error')
    LOGF('fatal')
