#!/usr/bin/python
# -*- coding: utf-8 -*- 

"""此脚本只用于演示简化的OpenID认证过程，如生产环境使用，
请进行适当修改，或推荐直接使用python-openid library

公司内部的OpenID，因为不是对外开放，也不需要支持各式各样的OpenID服务商
完成一次认证，实际上只需要如下三个步骤：

1. 关联（associate），目前在于与OpenID Server交换共享密钥，用于第3步签名校验
OpenID Server: https://login.netease.com/openid/
使用HTTP POST方式进行关联

2. 生成OpenID Server重定向URL，并使用HTTP 30X通知浏览器跳转至OpenID Server

3. 用户在OpenID Server校验后，会再次重定向回应用站点，应用站点对
重定向回来的数据（query string）进行签名校验，若成功，则可进行用户登录逻辑

"""
import sys
import urllib
import urllib2
import urlparse
import hmac
import hashlib
import base64

ASSOCIATE_DATA = {
    'openid.mode' : 'associate',
    'openid.assoc_type' : 'HMAC-SHA256', # OpenID消息签名算法，or HAMC-SHA1
    'openid.session_type' : 'no-encryption',
}
ASSOCIATE_DATA = urllib.urlencode( ASSOCIATE_DATA )

ASSOC = {}
ASSOC_RESP = urllib2.urlopen(
    'https://login.netease.com/openid/', ASSOCIATE_DATA )
for line in ASSOC_RESP.readlines():
    line = line.strip()
    if not line:
        continue
    k, v = line.split(":")
    ASSOC[k] = v
        
def check_authentication( request,
            idp="https://login.netease.com/openid/" ):
    """ check_authentication communication """
    check_auth = {}
    is_valid_map = {
        'false' : False,
        'true' : True,
    }
    request.update( {'openid.mode' : 'check_authentication'} )
    for k, v in request.iteritems():
        if type(v) is unicode:
            request.update( {k : v.encode('utf-8')} )
    authentication_data = urllib.urlencode( request )
    auth_resp = urllib2.urlopen(idp, authentication_data)
    for line in auth_resp.readlines():
        line = line.strip()
        if not line:
            continue
        k, v = line.split(":", 1)
        check_auth[k] = v

    is_valid = check_auth.get('is_valid', 'false')
    return is_valid_map[is_valid]


REDIRECT_DATA = {
    'openid.ns' : 'http://specs.openid.net/auth/2.0', # 固定字符串
    'openid.mode' : 'checkid_setup', # 固定字符串
    'openid.assoc_handle' : ASSOC['assoc_handle'], # 第一步获取的assoc_handle值
    # 如果想偷懒，可以不做associate操作，直接将openid_assoc_handle设置为空
    # 这种情况下，OpenID Server会自动为你生成一个新的assoc_handle，你需要通过check_authentication进行数据校验
    #'openid.assoc_handle' : None,
    'openid.return_to' : 'http://zealot.hz.netease.com:1234/auth', # 当用户在OpenID Server登录成功后，你希望它跳转回来的地址
    'openid.claimed_id' : 'http://specs.openid.net/auth/2.0/identifier_select', # 固定字符串
    'openid.identity' : 'http://specs.openid.net/auth/2.0/identifier_select', # 固定字符串
    'openid.realm' : 'http://zealot.hz.netease.com:1234/', # 声明你的身份（站点URL），通常这个URL要能覆盖openid.return_to
    'openid.ns.sreg' : 'http://openid.net/extensions/sreg/1.1', # 固定字符串
    # fullname为中文，如果您的环境有中文编码困扰，可以不要
    'openid.sreg.required' : "nickname,email,fullname", # 三个可以全部要求获取，或者只要求一个
}
REDIRECT_DATA = urllib.urlencode(REDIRECT_DATA)

#实际应用中，需要交由浏览器进行Redirect的URL，用户在这里完成交互认证
REDIRECT_URL = "https://login.netease.com/openid/?%s" % REDIRECT_DATA


def getAuth(QUERY):
    if QUERY=={}:
        return None
        
    OPENID_RESPONSE = dict(
        [(k, v[0].decode("UTF-8")) for k,v in urlparse.parse_qs(QUERY).items()] )

    # 第3步，用户成功校验，并跳转至第2步设定的openid.return_to地址
    #做一些基础校验
    if OPENID_RESPONSE['openid.mode'] != 'id_res':
        #一定是出错了，成功认证返回的openid.mode一定是id_res
        print u"openid.mode 不是 id_res"
        sys.exit(1)
    if OPENID_RESPONSE['openid.assoc_handle'] != ASSOC['assoc_handle']:
        # 可能consumer没有assoc或者OpenID Server不认可之前的association handle
        #  （如果你已经做了associate并且assoc_handle是一致的话
        # 那么不允许做check_authentication操作，一定会返回False ）
        if not check_authentication( OPENID_RESPONSE, idp = "https://login.netease.com/openid/" ):
            print u"assoc_handle不一致，check_authentication不成功"
            sys.exit(1)
        else:
            print u"assoc_handle不一致，check_authentication成功"
            print u"恭喜您，成功完成OpenID认证"
            print "nickname: %s" % OPENID_RESPONSE.get('openid.sreg.nickname', None)
            print "email: %s" % OPENID_RESPONSE.get('openid.sreg.email', None)
            print "fullname: %s" % OPENID_RESPONSE.get('openid.sreg.fullname', None)
            sys.exit(0)

    print u"OpenID Server返回的签名值: %s" % OPENID_RESPONSE['openid.sig']
    #构造需要检查签名的内容
    SIGNED_CONTENT = []
    for k in OPENID_RESPONSE['openid.signed'].split(","):
        response_data = OPENID_RESPONSE["openid.%s" % k]
        SIGNED_CONTENT.append(
                "%s:%s\n" % ( k, response_data ))
    SIGNED_CONTENT = "".join(SIGNED_CONTENT).encode("UTF-8")

    # 使用associate请求获得的mac_key与SIGNED_CONTENT进行assoc_type hash，
    # 检查是否与OpenID Server返回的一致
    SIGNED_CONTENT_SIG = base64.b64encode(
        hmac.new( base64.b64decode(ASSOC['mac_key']),
                SIGNED_CONTENT, hashlib.sha256 ).digest() )

    print u"Consumer（本地）计算出来的签名值: %s" % SIGNED_CONTENT_SIG

    if SIGNED_CONTENT_SIG != OPENID_RESPONSE['openid.sig']:
        print u"签名错误，认证不成功"
        sys.exit(1)

    print u"恭喜您，成功完成OpenID认证"
    auth={
          "nickname":OPENID_RESPONSE.get('openid.sreg.nickname', None),
          "email":OPENID_RESPONSE.get('openid.sreg.email', None),
          "fullname":OPENID_RESPONSE.get('openid.sreg.fullname', None)
          }

    print auth
    return auth
    
