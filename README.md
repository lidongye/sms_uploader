# sms_uploader

#### 介绍

新酷卡软件短信检测服务，检测数据库中新信息上传至服务端

#### 软件架构

mysql -> sms_uploader server -> remote http server  
number list file -> sms_uploader server -> remote http server

#### 安装教程

1. git clone https://github.com/lidongye/sms_uploader.git
2. cd sms_uploader
3. mkdir instance
4. edit config.py
5. pip install -r requirements.txt

#### 使用说明

1. 上传号码信息 `python main.py -t phone`
2. 短信检测上传 `python main.py -t sms`
