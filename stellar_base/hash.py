# coding:utf-8
import hashlib


def hash(data):
    return hashlib.sha256(data).digest()
