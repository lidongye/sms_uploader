#!/usr/bin/env python
# -*- coding=utf-8 -*-
# author: Dongye Li<dongye_bio@qq.com>
# 2019-03-17 16:54

import os
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
run_path = os.path.dirname(os.path.split(os.path.realpath(__file__))[0])
if os.path.isfile(os.path.join(run_path, "instance/config.py")):
    from instance import config
else:
    import config
from app import sms_logging
import utility




secret_key_file = os.path.join(run_path, 'instance/secret_key')
if not os.path.isfile(secret_key_file):
    open(secret_key_file, 'w').write(utility.random_str(64))
config.secret_key = open(secret_key_file).read()

# 初始化数据库连接:
pool_engine = create_engine(config.POOL_DB)
local_engine = create_engine(config.LOCAL_DB)
# 创建DBSession类型:
pool_session = sessionmaker(bind=pool_engine)
local_session = sessionmaker(bind=local_engine)

_logger = sms_logging.get_logger('app')

def run(options):
    from app import server
    if options.type == "phone":
        server.put_phone()
        return

    scan_interval = config.SCAN_INTERVAL
    while True:
        try:
            clock = time.time()
            server.check_sms()
        except Exception as e:
            _logger.error(e)
            print(e)
        finally:
            # sleep for the remaining seconds of interval
            if (time.time() - clock) < scan_interval:
                time_remaining = scan_interval - (time.time() - clock)
            else:
                time_remaining = 0
            time.sleep(time_remaining)
