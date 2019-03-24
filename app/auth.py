#!/usr/bin/env python
# -*- coding=utf-8 -*-
# author: Dongye Li<dongye_bio@qq.com>
# 2019-03-19 20:10

import sys
import json
import app
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

args = sys.argv


def generate_auth_token(data, expiration=600):
    """
    将数据封装成token，并设置过期时间

    :param data: 数据
    :param expiration: 过期时间
    :return:
    """
    s = Serializer(
        app.config.secret_key,
        expires_in=expiration
    )
    return s.dumps(json.dumps({
        "time" : s.now(),
        "data" : data
    })).decode()


def verify_token(token, token_time=10):
    """
    验证Token合法性并返回Token中data

    :param token:
    :param token_time:
    :return:
    """
    s = Serializer(app.config.secret_key)
    try:
        info = json.loads(s.loads(token))
        now = s.now()
        if now - info['time'] > token_time:
            return None # token超时
    except SignatureExpired:
        return None  # token过期
    except BadSignature:
        return None  # token无效
    except:
        return None  # 其他错误情况
    return True


def main(args):
    print(generate_auth_token("", 3600))
    pass


if __name__ == '__main__':
    main(args)
