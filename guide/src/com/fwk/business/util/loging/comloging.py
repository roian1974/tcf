import logging,logging.handlers

from src.com.fwk.business.info import include
from src.com.fwk.business.util.common import comutil

# logging
# mn_logger = logging.getLogger(__name__)
# mn_logger = logging.getLogger('root')
#
# tcf_logger = logging.getLogger(__name__)
# tcf_logger = logging.getLogger('root')
#
# stf_logger = logging.getLogger(__name__)
# stf_logger = logging.getLogger('root')
#
# sp_commo_logger = logging.getLogger(__name__)
# sp_commo_logger = logging.getLogger('root')



def set_logger2(logger) :
    FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(format=FORMAT)
    logger.setLevel(logging.DEBUG)

def set_logger(logger):

    fomatter = logging.Formatter('[%(levelname)s|%(filename)s:%(funcName)s:%(lineno)s] %(asctime)s > %(message)s')
    # fomatter = logging.Formatter('[%(levelname)s|%(filename)s:%(module)s:%(lineno)s] %(asctime)s > %(message)s')
    # file_handler = logging.FileHandler(doc["location"]['log'] + 'myLoggerTest.log')
    # file_handler = logging.handlers.RotatingFileHandler(filenamefilename, maxBytes=fileMaxByte, backupCount=10)
    # file_handler = logging.handlers.TimedRotatingFileHandler('C:/jDev/MyWorks/PycharmProjects/Roian/log/output/' + __file__ +'.log'
    out_log_fname = 'C:\jDev\MyWorks\PycharmProjects\Roian\log\output' +'\\' + include.getServiceName() +".out." + comutil.getsysdate()
    file_handler = logging.handlers.TimedRotatingFileHandler(out_log_fname + '.log'
                                                             , when="d"
                                                             , interval=7
                                                             , backupCount=0
                                                             )
    stream_handler = logging.StreamHandler()
    # rotate_handler = logging.handlers.RotatingFileHandler(when='d', interval='1')

    file_handler.setFormatter(fomatter)
    stream_handler.setFormatter(fomatter)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.setLevel(logging.DEBUG)
