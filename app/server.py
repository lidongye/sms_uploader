#!/usr/bin/env python
# -*- coding=utf-8 -*-
# author: Dongye<dongye_bio@qq.com>
# 2019-03-23 19:34

import sys
import uuid
import requests
import app
import json
import utility
from app import local_session, pool_session
from app import sms_logging
from app import auth
from .models import SMS_Receive, SMS_Upload, SMS_RECV

args = sys.argv
_logger = sms_logging.get_logger("server")


def put_phone():
    phone_number_list = []
    with open(app.config.PHONE_NUMBER_FILE, 'r') as f:
        for line in f:
            (phone_number, area, enable) = line.strip().split()
            enable = True if enable == "1" else False
            phone_number_list.append({
                "number": phone_number,
                "area": area,
                "enable": enable
            })
    token = auth.generate_auth_token("", 5)
    headers = {"Content-Type": "application/json", "Authorization":"Bearer %s" % token}
    res = requests.put(app.config.URL["post_phone"],
                       data=json.dumps({
                           "phone_number": phone_number_list
                       }), headers=headers)
    if res.status_code != 200:
        print ("upload error, code: %s, info: %s" % (res.status_code, res.text))
        raise ("upload error, code: %s, info: %s" % (res.status_code, res.text))

    res = json.loads(res.text)
    _logger.info("put phone number res: %s" % res)
    print(res)


def check_sms():
    pool = pool_session()
    local = local_session()
    query = pool.query(SMS_RECV)
    new_sms_number = query.count()
    # 将新收到的数据从卡池数据库读取到本地信息库，插入成功后将卡池数据库中数据删除
    for sms in query.all():
        try:
            local.add(SMS_Receive(
                str(uuid.uuid1()),
                sms.PhoNum,
                sms.smsNumber,
                sms.smsContent,
                sms.smsDate
            ))
        except Exception as e:
            _logger.error(e)
            continue
        else:
            pool.delete(sms)
    pool.commit()
    pool.close()
    local.commit()
    #将本地信息库中数据上传至服务器，成功的数据转移到upload表，失败的不动待下次再上传

    query = local.query(SMS_Receive)
    sms_receive_dict = {}
    sms_receive_list = []
    for sms in query.all():
        sms_receive_dict[sms.id] = sms
        sms_receive_list.append({
            "id" : sms.id,
            "phone_number": sms.phone_number,
            "from_number": sms.from_number,
            "content": sms.content,
            "receive_time": utility.format_time(sms.receive_time)
        })
    if sms_receive_list == []:
        local.close()
        return
    token = auth.generate_auth_token("", 60)
    headers = {"Content-Type": "application/json", "Authorization":"Bearer %s" % token}
    res = requests.post(app.config.URL["post_message"], headers=headers, data=json.dumps({
        "data":sms_receive_list
    }))
    if res.status_code != 200:
        _logger.error("upload error, code: %s, info: %s" % (res.status_code, res.text))
        raise ("upload error, code: %s, info: %s" % (res.status_code, res.text))

    res = json.loads(res.text)
    sms_upload = 0
    sms_upload_fail = 0
    if res["status"] == 200:
        sms_upload = len(res["add_list"])
        sms_upload_fail = len(res["fail_list"])
        for id in res["add_list"]:
            sms = sms_receive_dict[id]
            local.add(SMS_Upload(sms.id, sms.phone_number, sms.from_number, sms.content, sms.receive_time, None))
            local.delete(sms)
        local.commit()
    local.close()
    _logger.debug("new sms: %s, upload: %s, upload fail: %s" % (new_sms_number, sms_upload, sms_upload_fail))


def main(args):
    pass


if __name__ == '__main__':
    main(args)