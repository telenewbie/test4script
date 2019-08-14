#!/usr/bin/env python
# -*- coding:utf-8 -*-
 
import tornado.ioloop
import tornado.web
import os
import shutil
import json
import logging


 
class MainHandler(tornado.web.RequestHandler):
 
    def get(self):
        filename = self.get_argument('filename')
        # http头 浏览器自动识别为文件下载
        self.set_header('Content-Type', 'application/octet-stream')
        # 下载时显示的文件名称
        self.set_header('Content-Disposition', 'attachment; filename=%s'%filename)
        with open(filename, 'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                self.write(data)
        # 记得有finish哦
        self.finish()

    # 这里是代码
 
def uuid_naming_strategy(original_name):
    "File naming strategy that ignores original name and returns an UUID"
    return str(uuid.uuid4())
 
 
class UploadHandler(tornado.web.RequestHandler):
    "Handle file uploads."
 
    '''def initialize(self, upload_path, naming_strategy):
        """Initialize with given upload path and naming strategy.
        :keyword upload_path: The upload path.
        :type upload_path: str
        :keyword naming_strategy: File naming strategy.
        :type naming_strategy: (str) -> str function
        """
        self.upload_path = upload_path
        if naming_strategy is None:
            naming_strategy = uuid_naming_strategy
        self.naming_strategy = naming_strategy'''
 
    def post(self):
        fileinfo = self.request.files['filename'][0]
        filename = fileinfo['filename']
        try:
            with open(filename, 'wb+') as fh:
                fh.write(fileinfo['body'])
            logging.info("%s uploaded %s, saved as %s",str(self.request.remote_ip),str(fileinfo['filename']),filename)
        except IOError as e:
            logging.error("Failed to write file due to IOError %s", str(e))


 
def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/upload", UploadHandler),
    ])
 
if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
