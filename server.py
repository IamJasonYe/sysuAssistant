#!/usr/bin/env python
# -*- coding: utf-8 -*-
#import requests
from __future__ import with_statement
from functools import wraps
from contextlib import closing
from flask import Flask, request, g, redirect, url_for, abort, \
        render_template, flash, make_response, session
import re
import random

import fakesysujwxt as sysujwxt

# basic config
SITENAME = 'SYSU JWXT'
DEBUG = True
SECRET_KEY = 'development key'
SESSION_TIMEOUT = 60*30

# create application
app = Flask(__name__)
app.config.from_object(__name__)

client = None
# class ClientManage():
#     pool = []
#     def ClientFindById():
#         if ()
# -----------------
# useful functions
# ------
# Pages
# ------
@app.route('/test')
def test():
    return 'hello!'

@app.route('/')
def index():
    client = sysujwxt.Client()
    JSESSIONID = client.getJSESSIONID()
    cookie = "JSESSIONID=" + JSESSIONID
    client2 = sysujwxt.Client()
    rno = client2.getRno(cookie)
    data = client2.getJcodeImage(cookie)
    resp = make_response(data)
    resp.set_cookie('JSESSIONID', JSESSIONID)
    resp.set_cookie('rno', rno)
    print JSESSIONID
    print rno
    return resp

@app.route('/electGetImage')
def electGetImage():
    JSESSIONID = request.cookies.get("JSESSIONID")
    if JSESSIONID == None:
        JSESSIONID = sysujwxt.random_cookie()
    client = sysujwxt.Client()
    cookie = "JSESSIONID=" + JSESSIONID
    data = client.electGetImage(cookie)
    resp = make_response(data)
    resp.set_cookie('JSESSIONID', JSESSIONID)
    return resp


@app.route('/sign_in', methods=['POST', 'GET'])
def sign_in():
    if(request.cookies.get("JSESSIONID") == ""):
        return index()
    JSESSIONID = request.cookies.get("JSESSIONID")
    username = str(request.form.get("username"))
    password = str(request.form.get("password"))
    jcode = request.form.get("jcode")
    rno = request.cookies.get("rno")
    client = sysujwxt.Client()
    cookie = "JSESSIONID="+JSESSIONID
    if client.loginPost(username, password, jcode, rno, cookie):
        client.loginGet(cookie)
        return client.personDataGet(cookie)
    else:
        return u"登陆出错！"

@app.route('/elect_sign_in', methods=['POST', 'GET'])
def getClass():
    username = str(request.form.get("username"))
    password = str(request.form.get("password"))
    j_code = str(request.form.get("jcode"))
    JSESSIONID = request.cookies.get("JSESSIONID")
    cookie = "JSESSIONID="+JSESSIONID
    client = sysujwxt.Client()
    data = client.electLogin(username, password, j_code, cookie)
    resp = make_response(data)
    return resp

@app.route('/grade', methods=['POST','GET'])
def getGrade():
    xn = str(request.form.get("xn"))
    xq = str(request.form.get('xq'))
    print "xn: ", xn, " xq: ", xq
    JSESSIONID = str(request.cookies.get("JSESSIONID")).strip()
    print "JSESSIONID: ", JSESSIONID 
    cookie = "JSESSIONID="+ JSESSIONID
    client = sysujwxt.Client()
    data = client.getGrade(xn, xq, cookie)
    resp = make_response(data)
    return resp

@app.route('/timetable', methods=['POST', 'GET'])
def getTimeTable():
    xn = str(request.form.get("xn"))
    xq = str(request.form.get('xq'))
    print "xn: ", xn, " xq: ", xq
    JSESSIONID = str(request.cookies.get("JSESSIONID")).strip()
    print "JSESSIONID: ", JSESSIONID 
    cookie = "JSESSIONID="+ JSESSIONID
    client = sysujwxt.Client()
    data = client.getTimeTable(xn, xq, cookie)
    resp = make_response(data)
    return resp

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=80)
    app.run(host='0.0.0.0', debug=True)
