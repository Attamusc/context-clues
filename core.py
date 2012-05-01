#!/usr/bin/env python

import logging
import tornado.escape
import tornado.database
import tornado.ioloop
import tornado.options
import tornado.web
import os.path
import urllib2
import features

import logging  
from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)
define("debug", default="false", help="if the server should be run in debug mode", type=bool)
#define("mysql_host", default="127.0.0.1:3306", help="blog database host")
#define("mysql_database", default="genrebot", help="blog database name")
#define("mysql_user", default="root", help="blog database user")
#define("mysql_password", default="", help="blog database password")

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/parse", FeatureStripHandler)
        ]
        settings = dict(
            cookie_secret="43oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "assets"),
            xsrf_cookies=True,
            autoescape=None,
            debug=options.debug
        )
        tornado.web.Application.__init__(self, handlers, **settings)

        # Have one global connection to the DB across all handlers
        #self.db = tornado.database.Connection(
        #    host=options.mysql_host, database=options.mysql_database,
        #    user=options.mysql_user, password=options.mysql_password)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class FeatureStripHandler(tornado.web.RequestHandler):
    def get(self):
        filename = self.get_argument("filename", None)
        f1, f2 = features.strip(filename)
        feature_names = ['title','genre','amp1mean','amp1std','amp1skew',
                         'amp1kurt','amp1dmean','amp1dstd','amp1dskew',
                         'amp1dkurt','amp10mean','amp10std','amp10skew',
                         'amp10kurt','amp10dmean','amp10dstd','amp10dskew',
                         'amp10dkurt','amp100mean','amp100std','amp100skew',
                         'amp100kurt','amp100dmean','amp100dstd','amp100dskew',
                         'amp100dkurt','amp1000mean','amp1000std','amp1000skew',
                         'amp1000kurt','amp1000dmean','amp1000dstd','amp1000dskew',
                         'amp1000dkurt','power1','power2','power3','power4',
                         'power5','power6','power7','power8','power9','power10']
        f1_json = zip(feature_names, f1)
        f2_json = zip(feature_names, f2)
        json_response = dict(f1=dict(f1_json), f2=dict(f2_json))
        self.write (json_response)

def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
