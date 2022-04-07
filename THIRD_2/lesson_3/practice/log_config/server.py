import logging
from logging import handlers

from . import base

log = logging.getLogger('app.server')
log.setLevel(logging.ERROR)

file_handler = logging.handlers.TimedRotatingFileHandler(base.LOG_DIR / 'server.log', when='midnight', encoding='utf-8')
file_handler.setFormatter(base.FORMATTER)
log.addHandler(file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(base.FORMATTER)
log.addHandler(stream_handler)

if __name__ == '__main__':
    log.critical('test critical log msg')
    log.error('test error log msg')
    log.warning('test warning log msg')
    log.info('test info log msg')
    log.debug('test debug log msg')

