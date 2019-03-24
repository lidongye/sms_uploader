#!/usr/bin/env python
# -*- coding=utf-8 -*-
# author: Dongye Li<dongye@gooalgene.com>
# 2019-03-20 1:21

import sys
from optparse import OptionParser
import app

args = sys.argv


def main(options):
    app.run(options)


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-t", "--type", dest="type", default="sms",
                      help="启动方式 上传phone_number或轮询信息", metavar="sms or phone")
    (options, args) = parser.parse_args()
    main(options)
