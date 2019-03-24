#!/usr/bin/env python
# coding=utf-8

import sys
import os
from app import config
import logging
import logging.handlers

NAME = 'sms_uploader'

logger = logging.getLogger(NAME)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

local_handler = logging.FileHandler(os.path.join(config.LOG_PATH, "sms_uploader.log"))
local_handler.setLevel(logging.DEBUG)
local_handler.setFormatter(formatter)
logger.addHandler(local_handler)


def get_logger(name):
    return logging.getLogger(NAME + '.' + name)


if __name__ == '__main__':
    logger.debug("log_test")
