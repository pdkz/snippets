import os
import inspect
import logging
import datetime

DEBUG = 'debug'
VIEW  = 'view'
INFO  = 'info'
WARN  = 'warn'
ERROR = 'error'
FATAL = 'fatal'

loglevel = {
    DEBUG : 10,
    VIEW  : 15,
    INFO  : 20,
    WARN  : 30,
    ERROR : 40,
    FATAL : 50}

def file_loghandler(loglevel=loglevel[DEBUG]):
    logfmt = '%(asctime)s [%(levelname)8s] %(message)s %(file)s%(line)s'
    fmt = logging.Formatter(logfmt)
    
    handler = logging.FileHandler(os.path.join(logpath, logfilename), 'a+')

    handler.setFormatter(fmt)
    handler.setLevel(loglevel)

    return handler

def console_loghandler(loglevel=loglevel[DEBUG]):
    logging.addLevelName(15, 'VIEW')
    
    logfmt = '%(asctime)s [%(levelname)8s] %(message)s %(file)s%(line)s'
    fmt = logging.Formatter(logfmt)

    handler = logging.StreamHandler()
    handler.setFormatter(fmt)
    handler.setLevel(loglevel)

    return handler

class Singleton(object):
    def __new__(cls, *args, **kwargs) :
        if '_inst' not in vars(cls) :
            cls._inst = super(Singleton, cls).__new__(cls)
        return cls._inst

class Logger(Singleton):
    def __init__(self,
                loghandler: list,
                loglevel=logging.DEBUG, 
                filename='log',
                logpath='.\\log',
                is_logfile_output=False):

        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.DEBUG)

        for handler in loghandler:
            self.log.addHandler(handler)

    @classmethod
    def initialize(
        cls,
        loghandler: list, 
        loglevel=logging.DEBUG,
        filename='log',
        logpath='..\\log'):
        
        cls._inst = Logger(
            loghandler,
            loglevel=loglevel,
            filename=filename,
            logpath=logpath)
        
    @staticmethod
    def finalize():
        logging.shutdown()

    @classmethod
    def get_instance(cls):
        if '_inst' not in vars(cls) :
            return None
        return cls._inst

    @staticmethod
    def save_message(level, msg, filename='', funcname='', line=0, *args, **kwrgs):
        d = {'file': '', 'line': ''}
        if level == 'error' or level == 'fatal':
            d['file'] = '@' + filename
            d['line'] = ', line ' + str(line)
        
        if funcname:
            msg = f'{funcname}: {msg}'

        _inst = Logger.get_instance()
        if _inst is None:
            return

        _inst.log.log(loglevel[level], msg, extra=d)

def LOGD(msg, depth=0, *args): Logger.save_message(DEBUG, msg, filename=inspect.currentframe().f_back.f_code.co_filename, funcname=inspect.currentframe().f_back.f_code.co_name, line=inspect.currentframe().f_back.f_lineno, args=args)
def LOGV(msg, depth=0, *args): Logger.save_message(VIEW,  msg, filename=inspect.currentframe().f_back.f_code.co_filename, funcname=inspect.currentframe().f_back.f_code.co_name, line=inspect.currentframe().f_back.f_lineno, args=args)
def LOGI(msg, depth=0, *args): Logger.save_message(INFO,  msg, filename=inspect.currentframe().f_back.f_code.co_filename, funcname=inspect.currentframe().f_back.f_code.co_name, line=inspect.currentframe().f_back.f_lineno, args=args)
def LOGW(msg, depth=0, *args): Logger.save_message(WARN,  msg, filename=inspect.currentframe().f_back.f_code.co_filename, funcname=inspect.currentframe().f_back.f_code.co_name, line=inspect.currentframe().f_back.f_lineno, args=args)
def LOGE(msg, depth=0, *args): Logger.save_message(ERROR, msg, filename=inspect.currentframe().f_back.f_code.co_filename, funcname=inspect.currentframe().f_back.f_code.co_name, line=inspect.currentframe().f_back.f_lineno, args=args)
def LOGF(msg, depth=0, *args): Logger.save_message(FATAL, msg, filename=inspect.currentframe().f_back.f_code.co_filename, funcname=inspect.currentframe().f_back.f_code.co_name, line=inspect.currentframe().f_back.f_lineno, args=args)

def test():
    LOGI('info')

if __name__ == '__main__':
    loghandler = [console_loghandler(loglevel[VIEW])]
    Logger.initialize(loghandler)

    LOGD('debug %d' % 10)
    LOGI('info')
    LOGW('warn')
    LOGE('error')
    LOGF('fatal')
    
    test()
