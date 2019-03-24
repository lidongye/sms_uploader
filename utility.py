#!/usr/bin/env python
# -*- coding=utf-8 -*-
# author: Dongye Li<dongye_bio@qq.com>
# 2019-03-17 23:35

import sys
import json
import random, string
from datetime import datetime

args = sys.argv


def get_request_entity(request):
    if request.method in ["POST", "PUT"]:
        if request.mimetype == "application/json":
            return request.json
        elif request.mimetype == "text/plain":
            entity_json = request.get_data(as_text=True)
            try:
                return json.loads(entity_json, encoding="utf-8")
            except:
                raise ("No Json Data")
        elif request.mimetype == "multipart/form-data":
            return request.form.to_dict()
        else:
            raise ("No Json Data")
    elif request.method == "GET":
        if request.mimetype == "application/json":
            return request.json
        entity_dict = request.args.to_dict()
        return entity_dict
    else:
        raise("method error")


def random_str(len=10):
    """
    生成指定长度字符串
    :param len:
    :return:
    """

    return ''.join(random.choices(string.ascii_letters + string.digits, k=len))


def get_past_time(last_time):
    """
    返回指定时间据当前时间差
    :param last_time:
    :return:
    """
    try:
        t = datetime.now() - last_time
        if t.total_seconds() / 3600 / 24 > 1:
            return "%s 天" % (int(t.total_seconds() / 3600 / 24))
        if t.total_seconds() / 3600 > 1:
            return "%s 小时" % (int(t.total_seconds() / 3600))
        if t.total_seconds() / 60 > 1:
            return "%s 分钟" % (int(t.total_seconds() / 60))
        if t.total_seconds() > 1:
            return "%s 秒" % (int(t.total_seconds()))
    except Exception:
        return "--"
    return "--"


def format_time(t, format = "%Y-%m-%d %H:%M:%S"):
    """
    调整时间格式为 "%Y-%m-%d %H:%M:%S"
    :param t:
    :param format: 调整的格式
    :return:
    """
    return datetime.strftime(t, format)


def main(args):
    pass


if __name__ == '__main__':
    main(args)
