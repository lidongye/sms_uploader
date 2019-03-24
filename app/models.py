#!/usr/bin/env python
# -*- coding=utf-8 -*-
# author: Dongye Li<dongye_bio@qq.com>
# 2019-03-17 20:36

import sys
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base

from app import local_engine, pool_engine

args = sys.argv
local_model = declarative_base(bind=local_engine, name="local_model")
pool_model = declarative_base(bind=pool_engine, name="pool_model")

class SMS_Receive(local_model):
    """
    接收待上传信息表
    """
    __tablename__ = 'SMS_Receive'
    id = Column(String(64), primary_key=True)
    phone_number = Column(String(32), index=True)
    from_number = Column(String(32))
    content = Column(Text)
    receive_time = Column(DateTime, index=True)

    def __init__(self, id, phone_number, from_number, content, receive_time = None):
        self.id = id
        self.phone_number = phone_number
        self.from_number = from_number
        self.content = content

        try:
            if isinstance(receive_time, str):
                receive_time = datetime.strptime(receive_time, "%Y-%m-%d %H:%M:%S")
            elif isinstance(receive_time, bytes):
                receive_time = datetime.strptime(receive_time.decode("utf-8"), "%Y-%m-%d %H:%M:%S")
            elif not isinstance(receive_time, datetime):
                receive_time = datetime.now()
        except:
            receive_time = datetime.now()

        self.receive_time = receive_time


class SMS_Upload(local_model):
    """
    上传成功信息表
    """
    __tablename__ = 'SMS_Upload'
    id = Column(String(64), primary_key=True)
    phone_number = Column(String(32), index=True)
    from_number = Column(String(32))
    content = Column(Text)
    receive_time = Column(DateTime, index=True)
    upload_time = Column(DateTime, index=True)

    def __init__(self, id, phone_number, from_number, content, receive_time = None, upload_time=None):
        self.id = id
        self.phone_number = phone_number
        self.from_number = from_number
        self.content = content
        try:
            if isinstance(receive_time, str):
                receive_time = datetime.strptime(receive_time, "%Y-%m-%d %H:%M:%S")
            elif isinstance(receive_time, bytes):
                receive_time = datetime.strptime(receive_time.decode("utf-8"), "%Y-%m-%d %H:%M:%S")
            elif not isinstance(receive_time, datetime):
                receive_time = datetime.now()
        except:
            receive_time = datetime.now()
        try:
            if isinstance(upload_time, str):
                upload_time = datetime.strptime(upload_time, "%Y-%m-%d %H:%M:%S")
            elif isinstance(upload_time, bytes):
                upload_time = datetime.strptime(upload_time.decode("utf-8"), "%Y-%m-%d %H:%M:%S")
            elif not isinstance(upload_time, datetime):
                upload_time = datetime.now()
        except:
            upload_time = datetime.now()

        self.receive_time = receive_time
        self.upload_time = upload_time


class SMS_RECV(pool_model):
    """
    卡池接收短信表
    """
    __tablename__ = 'sms_recv'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    PortNum = Column(Integer)
    PhoNum = Column(String(255))
    IMSI = Column(String(255))
    ICCID = Column(String(255))
    smsDate = Column(String(255))
    smsNumber = Column(String(255))
    smsContent = Column(String(255))


def main(args):
    local_model.metadata.create_all(local_engine)
    pool_model.metadata.create_all(pool_engine)
    pass


if __name__ == '__main__':
    main(args)
