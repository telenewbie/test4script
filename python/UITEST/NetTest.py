# encoding:utf-8
import urllib2

# urllib2和urllib 最大的区别在于urllib2可以请求身份验证的网址(适用于更加复杂的打开url的情况)
LOGIN = "1175023786@qq.com"
PASSWORD = "telenewbieDong"
URL_LOGIN = "https://passport.csdn.net/account/login?from=http://bbs.csdn.net/topics"


def handler_version(url):
    from urlparse import urlparse as up
    hdlr = urllib2.HTTPBasicAuthHandler()
    hdlr.add_password('Archives', up(url)[1], LOGIN, PASSWORD)
    opener = urllib2.build_opener(hdlr)
    urllib2.install_opener(opener)
    r = request_version(url)
    print r.data
    print r.headers
    print r.host, ":", r.port
    return url


def request_version(url):
    from base64 import encodestring
    req = urllib2.Request(url)
    b64str = encodestring('%s:%s' % (LOGIN, PASSWORD))[:-1]
    req.add_header("Authorization", "Basic %s" % b64str)
    return req


# for funcType in ('handler', 'request'):
#     print "*** Using %s:" % funcType.upper()
#     url = eval("%s_version")(URL_LOGIN)
#     f = urllib2.urlopen(url)
#     print f.readline()
#     f.close()

print handler_version(URL_LOGIN)
