# coding=utf-8

import urllib, urllib2
import base64
import cookielib
from HTMLParser import HTMLParser as hp
import random


class MyHTMLParser(hp):
    rno = ""

    def handle_starttag(self, tag, attrs):
        if (tag == 'input' and len(attrs) > 3 and attrs[3] != None and attrs[3][0] == 'value'):
            self.rno = attrs[3][1]

def random_cookie():
    s = str()
    s += ''.join(random.sample('ASDXCVARTXZBJHCVXBZVXB',8))
    s += ''.join(random.sample('FDHQTASFDGDSFGVCXBZVXB',8))
    s += ''.join(random.sample('ZXCBCVNDFHJRTKHMABZVXB',8))
    s += ''.join(random.sample('ERYEDHSDWERHRHFGNHWRHT',8))
    return s


def md5(str):
    import hashlib
    import types
    if type(str) is types.StringType:
        m = hashlib.md5()
        m.update(str)
        return m.hexdigest().upper()
    else:
        return ''


class Client:
    opener = None
    rno = ""

    def __init__(self):
        pass
        # cookiejar = cookielib.MozillaCookieJar()
        # cookiejar.clear()
        # cookie_support = urllib2.HTTPCookieProcessor(cookiejar)
        # self.opener = urllib2.build_opener(cookie_support)

    def getResponse(self, url, cookie=None, data=None, referer=None):
        try:
            postData = urllib.urlencode(data) if data != None else None
            header = {"Cookie": cookie, 'Referer': referer}
            request = urllib2.Request(url, postData, header)
            response = urllib2.urlopen(request)
            return response
        except Exception, e:
            print e.message


    def getJSESSIONID(self):
        url = 'http://uems.sysu.edu.cn/jwxt/'
        response = self.getResponse(url)
        return response.info().getheader("Set-Cookie").split(";")[0].split("=")[1]


    def getRno(self, cookie=None):
        url = 'http://uems.sysu.edu.cn/jwxt/'
        parser = MyHTMLParser()
        response = self.getResponse(url, cookie)
        parser.feed(response.read().decode('utf-8'))
        return parser.rno


    def getJcodeImage(self, cookie=None):
        url = 'http://uems.sysu.edu.cn/jwxt/jcaptcha'
        refered = 'http://uems.sysu.edu.cn/jwxt/'
        response = self.getResponse(url, cookie, referer=refered)
        # 打开登录主页面,下载图片
        data = response.read()

        # data = base64.b64encode(data)
        return data


    def loginPost(self, username, password, j_code, rno, cookie):
        url = 'http://uems.sysu.edu.cn/jwxt/j_unieap_security_check.do'
        data = {'j_username': username, 'j_password': md5(password), 'jcaptcha_response': j_code, 'rno': rno}
        try:
            self.getResponse(url, cookie, data)
            return True
        except urllib2.HTTPError, e:
            return False


    def loginGet(self, cookie):
        url = 'http://uems.sysu.edu.cn/jwxt/login.do?method=login'
        self.getBase(url, cookie)


    def personDataGet(self, cookie):
        url = 'http://uems.sysu.edu.cn/jwxt/edp/menu/RootMenu.jsp'
        return self.getBase(url, cookie)


    def getClass(self, cookie, xq, xnd):
        url = 'http://uems.sysu.edu.cn/jwxt/KcbcxAction/KcbcxAction.action?method=getList'
        refer = 'http://uems.sysu.edu.cn/jwxt/sysu/xk/xskbcx/xskbcx.jsp?xnd='+xnd+'&xq='+xq
        data = {"header":{"code": -100, "message": {"title": "", "detail": ""}},
         "body":{"dataStores":{},"parameters":{"args": ["1", "2014-2015"], "responseParam": "rs"}}
         }
        return self.getBase(url=url, cookie=cookie, data=data, referer=refer)


    def electLogin(self, username, password, j_code, cookie):
        url = "http://uems.sysu.edu.cn/elect/login/"
        data = {'username': username, 'password': md5(password), 'j_code': j_code}
        return self.getBase(url=url, cookie=cookie, data=data)



    def electGetImage(self, cookie):
        url = "http://uems.sysu.edu.cn/elect/login/code"
        return self.getBase(url, cookie)

    def getGrade(self, xn, xq, cookie):
        pass
    def getBase(self, url, cookie, data=None, referer=None):
        try:
            response = self.getResponse(url, cookie, data, referer)
            return response.read()
        except urllib2.HTTPError, e:
            print e
            return e
