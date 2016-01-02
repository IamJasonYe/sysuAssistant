# coding=utf-8

import urllib, urllib2
import base64
import httplib
import cookielib
from HTMLParser import HTMLParser as hp
import random
import json


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

    def getResponse(self, url, data=None, encode=True, header={}):
        try:
            if encode:
                postData = urllib.urlencode(data) if data != None else None
            else:
                postData = data
            request = urllib2.Request(url, data=postData, headers=header)
            response = urllib2.urlopen(request)
            return response
        except Exception, e:
            print "fuck: ",e.message
    
    
    def getJSESSIONID(self):
        url = 'http://uems.sysu.edu.cn/jwxt/'
        response = self.getResponse(url)
        return response.info().getheader("Set-Cookie").split(";")[0].split("=")[1]


    def getRno(self, cookie=None):
        url = 'http://uems.sysu.edu.cn/jwxt/'
        parser = MyHTMLParser()
        header = {"Cookie": cookie}
        response = self.getResponse(url, header=header)
        parser.feed(response.read().decode('utf-8'))
        return parser.rno


    def getJcodeImage(self, cookie=None):
        url = 'http://uems.sysu.edu.cn/jwxt/jcaptcha'
        referer = 'http://uems.sysu.edu.cn/jwxt/'
        header = {}
        header['Referer'] = referer
        header['Cookie'] = cookie
        response = self.getResponse(url, header=header)
        # 打开登录主页面,下载图片
        data = response.read()
        # data = base64.b64encode(data)
        return data


    def loginPost(self, username, password, j_code, rno, cookie):
        url = 'http://uems.sysu.edu.cn/jwxt/j_unieap_security_check.do'
        data = {'j_username': username, 'j_password': md5(password), 'jcaptcha_response': j_code, 'rno': rno}
        try:
            header = {"Cookie":cookie}
            self.getResponse(url, header=header, data=data)
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
        header = {}
        refer = 'http://uems.sysu.edu.cn/jwxt/sysu/xk/xskbcx/xskbcx.jsp?xnd='+xnd+'&xq='+xq
        header['Referer'] = refer 
        data = {"header":{"code": -100, "message": {"title": "", "detail": ""}},
         "body":{"dataStores":{},"parameters":{"args": ["1", "2014-2015"], "responseParam": "rs"}}
         }
        return self.getBase(url=url, cookie=cookie, data=data, header = header)


    def electLogin(self, username, password, j_code, cookie):
        url = "http://uems.sysu.edu.cn/elect/login/"
        data = {'username': username, 'password': md5(password), 'j_code': j_code}
        return self.getResponse(url, data=data, header={"Cookie":cookie})



    def electGetImage(self, cookie):
        url = "http://uems.sysu.edu.cn/elect/login/code"
        return self.getResponse(url, header={"Cookie":cookie})

    def getGrade(self, xn, xq, cookie=None):
        url = "http://uems.sysu.edu.cn/jwxt/xscjcxAction/xscjcxAction.action?method=getKccjList"
        referer = "http://uems.sysu.edu.cn/jwxt/forward.action?path=/sysu/xscj/xscjcx/xsgrcj_list"
        data = "{header:{\"code\": -100, \"message\": {\"title\": \"\", \"detail\": \"\"}},body:{dataStores:{kccjStore:{rowSet:{\"primary\":[],\"filter\":[],\"delete\":[]},name:\"kccjStore\",pageNumber:1,pageSize:10,recordCount:14,rowSetName:\"pojo_com.neusoft.education.sysu.xscj.xscjcx.model.KccjModel\",order:\"t.xn, t.xq, t.kch, t.bzw\"}},parameters:{\"kccjStore-params\": [{\"name\": \"Filter_t.pylbm_0.982323750833501\", \"type\": \"String\", \"value\": \"'01'\", \"condition\": \" = \", \"property\": \"t.pylbm\"}, {\"name\": \"Filter_t.xn_0.6320431695071709\", \"type\": \"String\", \"value\": \"'%s'\", \"condition\": \" = \", \"property\": \"t.xn\"}, {\"name\": \"Filter_t.xq_0.6051254247425051\", \"type\": \"String\", \"value\": \"'%s'\", \"condition\": \" = \", \"property\": \"t.xq\"}], \"args\": [\"student\"]}}}"%(xn,xq)
        header = {}
        header['Referer']= referer
        header['Cookie']= cookie
        header['render']= 'unieap'
        header['Content-Type']='multipart/form-data'
        print header
        return self.getResponse(url, data=data, header=header, encode=False).read()
        
    def getBase(self, url, cookie=None, data=None, header={}):
        try:
            response = self.getResponse(url, data=data, header={"Cookie":cookie})
            return response.read()
        except urllib2.HTTPError, e:
            print e
            return e
