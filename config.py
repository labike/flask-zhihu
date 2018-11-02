# encoding: utf-8

import os
import pymysql

DEBUG = True

SECRET_KEY = os.urandom(24)

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:admin@127.0.0.1:3306/zhihu?charset=utf8'
SQLALCHEMY_TRACK_MODIFICATIONS = False