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
define("debug", default=false, help="if the server should be run in debug mode", type=bool)

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
            facebook_api_id="343864215644943",
            facebook_api_secret="7fc83e7cfeaf584c338eb2e07f30021a",
            xsrf_cookies=True,
            autoescape=None,
            debug=options.debug
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
            token_req = urllib2.Request("https://graph.facebook.com/oauth/access_token?client_id=" + 
                                        self.settings['facebook_api_id'] + 
                                        "&client_secret=" + 
                                        self.settings['facebook_api_secret'] + 
                                        "&grant_type=client_credentials")
            access_token = urllib2.urlopen(token_req).read()
            logging.info(access_token)

            graph_query_url = "https://graph.facebook.com/search?q=" + query + "&type=post&access_token=" + access_token
            req = urllib2.Request("https://graph.facebook.com/search?q=" + query + "&type=post&" + access_token)
            result = urllib2.urlopen(req).read()
        self.finish(result)

def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
