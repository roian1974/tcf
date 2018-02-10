import logging,logging.handlers
import os

from src.com.fwk.business.info import include
from src.com.fwk.business.util.common import comutil


# logging
logger = logging.getLogger(__name__)
logger = logging.getLogger('root')

def set_logger2(logger) :
    FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(format=FORMAT)
    logger.setLevel(logging.DEBUG)

def set_logger(logger):


    fomatter = logging.Formatter('[%(levelname)4s|%(filename)15s:%(funcName)18s:%(lineno)3s:%(process)d] %(asctime)s > %(message)s')
    # fomatter = logging.Formatter('[%(levelname)s|%(filename)s:%(module)s:%(lineno)s] %(asctime)s > %(message)s')
    # file_handler = logging.FileHandler(doc["location"]['log'] + 'myLoggerTest.log')
    # file_handler = logging.handlers.RotatingFileHandler(filenamefilename, maxBytes=fileMaxByte, backupCount=10)
    # file_handler = logging.handlers.TimedRotatingFileHandler('C:/jDev/MyWorks/PycharmProjects/Roian/log/output/' + __file__ +'.log'



    if include.getOSType() == 'Windows':
        out_log_fname = include.gtcfenv['output_dir'] + '\\' + include.getServiceName() + ".out." + comutil.getsysdate()
    else:
        out_log_fname = include.gtcfenv['unix_output_dir'] +'/' + include.getServiceName() +".out." + comutil.getsysdate()


    print("--out_log_fnmae=",out_log_fname)
    file_handler = logging.handlers.TimedRotatingFileHandler(out_log_fname
                                                             , when="d"
                                                             , interval=7
                                                             , backupCount=0
                                                             , encoding='utf-8'
                                                             )
    stream_handler = logging.StreamHandler()
    # rotate_handler = logging.handlers.RotatingFileHandler(when='d', interval='1')

    file_handler.setFormatter(fomatter)
    stream_handler.setFormatter(fomatter)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


    try :
        LEV=comutil.getenviron("LOGLEV")
        if LEV == "DEBUG" :
            logger.setLevel(logging.DEBUG)
        elif LEV == "INFO":
            logger.setLevel(logging.INFO)
        elif LEV == "ERROR":
            logger.setLevel(logging.ERROR)
        else :
            logger.setLevel(logging.ERROR)
    except Exception as err:
        logger.setLevel(logging.DEBUG)


def set_loglevel() :
    # 환경변수를 읽어서 로깅 레벨과 로그를 남길 파일의 경로를 변수에 저장한다
    if (os.environ['NODE_ENV'] == 'local'):
        loggerLevel = logging.DEBUG
        filename = '/tmp/test.log'
    elif (os.environ['NODE_ENV'] == 'test'):
        loggerLevel = logging.DEBUG
        filename = '/home/www/log/testServer.log'
    else:
        loggerLevel = logging.INFO
        filename = '/home/www/log/server.log'
