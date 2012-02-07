#!/usr/bin/env python

import logging
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import os.path
import urllib2

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/OpenGraphQuery", OpenGraphHandler)
        ]
        settings = dict(
            cookie_secret="43oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "assets"),
            xsrf_cookies=True,
            autoescape=None,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class OpenGraphHandler(tornado.web.RequestHandler):
    def get(self):
        query = self.get_argument("query")
        result = ""
        if query != "":
            req = urllib2.Request("https://graph.facebook.com/search?q=" + 
                                  query + 
                                  "&type=post&access_token=AAAAAAITEghMBAHin0WyVzppnZAzZAVgfzpvgrhaO8tazZBG1fxTU9erWwiwJOJ5uC0sJUzBHsJe942bMQfErtASGTDyTBVlrkHnEg6dXwZDZD")
            result = urllib2.urlopen(req).read()
        self.finish(result)

def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
