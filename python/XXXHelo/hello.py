# coding:utf-8
import os
import webbrowser
import HTMLParser
import urllib
import  commands
import sys
def printStr(str):
    if not isinstance(str, unicode):
        print str.decode("gbk").encode("utf8")
    else:
        print str.encode('utf8')

url = "http://www.baidu.com/"
'''
class parseLinks(HTMLParser.HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name,value in attrs:
                if name == 'href':
                    print value
            print self.get_starttag_text()
lParser = parseLinks()
lParser.feed(urllib.urlopen(url).read())
# sys.path.append("libs")
'''

arg = 20
if arg > 20:
    print("xxx")
else:
    print("rrr")

aaa='''
os.getenv("Computername");


var = os.path.exists("x.txt")
print var
if var == "true":
    print 1
else:
    print 2
var = os.open("xxx.txt", os.O_CREAT | os.O_APPEND)
fd=open("xxx.txt","w")
fd.write("XXXX hello world ")
fd.close()
fd=open("xxx.txt","r")
xxx=fd.read()
print  xxx
# open("http://www.baidu.com")

url = 'http://www.baidu.com'
webbrowser.open(url)
# webbrowser.get().
print webbrowser.get()

#commands.getstatusoutput()

'''

# print(aaa);
#os.system("ping www.baidu.com")
(status, output) = commands.getstatusoutput('cat /proc/cpuinfo')
printStr(output)
print status
re=os.popen("adb shell cat /proc/cpuinfo");
# print test.encode("")
print re.readlines()
s = u'你好'
print(s)
# print sss