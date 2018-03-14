# -*- coding: utf-8 -*-
import logging

import util.loggerutils as loggerUtil


def logShow(msg, level='info', belong_to='', attach='', save_in_db=False):
    logging.basicConfig(level=(logging.INFO if level == 'info' else logging.WARN))
    logger = loggerUtil.bas_console_logger('logger')
    belong_to = (belong_to+':') if belong_to else ''
    logger.info(belong_to + msg)


def warn(msg, belong_to='', attach='', save_in_db=False):
    logShow(msg, level='warn', belong_to=belong_to, attach=attach, save_in_db=save_in_db)


def info(msg, belong_to='', attach='', save_in_db=False):
    logShow(msg, level='info', belong_to=belong_to, attach=attach, save_in_db=save_in_db)

if __name__ == '__main__':
    warn('1111')
    info('222')