import logging
import os
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler
import sys
sys.path.append(os.path.join(os.getcwd(), '..'))
sys.path.append('../')

#  Create PATH for logging

PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'utils/utils.log')
PARAMS = {'hosts': '127.0.0.1', 'port': 7777}



# Create loger

logger = logging.getLogger('utils')
formatter = logging.Formatter('%(levelname)-15s %(asctime)s %(message)s')
logger.setLevel(logging.DEBUG)


# Create file handler log with rotation big file

fl = logging.FileHandler(PATH, mode='w', encoding='utf-8')
fl.setLevel(logging.DEBUG)
fl.setFormatter(formatter)



# Create stream handler log

sl = logging.StreamHandler(sys.stderr)
sl.setLevel(logging.DEBUG)
sl.setFormatter(formatter)


# Create handler TimeRotationHandler and RotatingFileHandler

handler_time = TimedRotatingFileHandler(PATH, when='D')   # Every day rotation file
handler_time.setLevel(logging.DEBUG)
handler_time.setFormatter(formatter)
# handler_file = RotatingFileHandler(PATH, maxBytes=99999,  backupCount=10, encoding='utf-8')
# handler_file.setLevel(logging.ERROR)
# handler_file.setFormatter(formatter)

# Added handler to logger

logger.addHandler(handler_time)
# logger.addHandler(handler_file)
logger.addHandler(fl)
logger.addHandler(sl)


