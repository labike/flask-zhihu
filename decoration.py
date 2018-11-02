# encoding: utf-8

from functools import wraps
from flask import session, redirect, url_for


def login_require(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if session.get('user_id'):
            return fn(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrapper
