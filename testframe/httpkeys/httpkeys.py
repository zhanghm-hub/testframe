#!/usr/bin/env
#-*-coding:utf-8 -*-
import requests,json,base64
import datetime
#消除禁用https验证的警告
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
class Http:

    def __init__(self):
        #初始化session用来模拟客户端的会话管理
        self.session=requests.session()
        #给出请求头部默认值
        self.session.headers['Content-Type']='application/json;charset=UTF-8'
        self.session.headers['User-Agent'] = '''Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'''
        #当前请求的响应结果
        self.response={}
        #保存需要保存的响应字段，便于之后使用
        self.saveres={}

    def post(self,url,data):
        #如果是登录接口的话，需要对参数中的用户名和密码经过base64编码
        if 'login' in url:
            data['user_pwd']=base64.b64encode(data['user_pwd'].encode()).decode()
        now=datetime.datetime.now()
        while True:
            try:
                res=self.session.post(url,json=data,verify=False)
                try:
                    self.response=json.loads(res.text)
                #响应状态码不为200的时候，直接保存
                except:
                    self.response=res.text
            #若是http连接太过频繁，导致连接超时则再次发起请求，否则抛出异常
            except (requests.exceptions.SSLError, requests.exceptions.ConnectionError) as error:
                if 'bad handshake' in str(error) or '10054' in str(error):
                    continue
                else:
                    raise Exception(error)
            break
        delta=datetime.datetime.now()-now
        elapse=delta.total_seconds()

    def update_headers(self,hkey,vkey):
        value=self.__getparam(vkey)
        self.session.headers[hkey]=value

    def savere(self,key,vkey):
     '''保存响应结果中键为vkey的值到saveres中键为key'''
     vkey='self.response'+vkey
     self.saveres[key]=eval(vkey)

    def __getparam(self,keystr):
        '''将其他函数中用到已保存响应结果的地方，用保存的值替换掉，实现关联'''
        for key in self.saveres.keys():
            keystr=keystr.replace("{"+key+'}',str(self.saveres[key]))
        return keystr

    def assert_equal(self,key,value):
        '''断言响应中键为key的值与value相等'''
        if str(self.response[key])==str(value):
            print('pass')
        else:
            print("fail")

    def assert_contain(self,key,value):
        '''断言响应中键为key的值包含value'''
        if str(self.response[key]) in str(value):
            print('pass')
        else:
            print("fail")


if __name__=='__main__':
    http=Http()
    data={"user_id":"wanggangtest","user_pwd":"SYhyyVqM","verify_code":"wanggangtestpystandard","force":1}
    http.post('https://www.pystandard.com.cn/pyfinance2v2/pyplatform_v2/front_system/user/validate/login',data)
    http.savere('token','["flag"]')

