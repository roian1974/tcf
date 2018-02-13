import logging,logging.handlers



def set_logger2() :
    FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
    logging.basicConfig(format=FORMAT)
    logger.setLevel(logging.DEBUG)


def set_logger():

    fomatter = logging.Formatter('[%(levelname)s|%(filename)s:%(funcName)s:%(lineno)s] %(asctime)s > %(message)s')
    # fomatter = logging.Formatter('[%(levelname)s|%(filename)s:%(module)s:%(lineno)s] %(asctime)s > %(message)s')
    # file_handler = logging.FileHandler(doc["location"]['log'] + 'myLoggerTest.log')
    # file_handler = logging.handlers.RotatingFileHandler(filenamefilename, maxBytes=fileMaxByte, backupCount=10)
    # file_handler = logging.handlers.TimedRotatingFileHandler('C:/jDev/MyWorks/PycharmProjects/Roian/log/output/' + __file__ +'.log'
    file_handler = logging.handlers.TimedRotatingFileHandler(__file__ + '.log'
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

logger = logging.getLogger(__name__)
logger = logging.getLogger('root')

set_logger2()

logger.info('0000000')
logger.debug('0000000')
logger.error('0000000')
logger.critical('0000000')
logger.warning('edeeeed')


