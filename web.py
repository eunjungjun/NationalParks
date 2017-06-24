#!/usr/bin/env python

import os
import json
import tornado.ioloop
import tornado.web
from parks.db import ParksDB

PORT = 8880
ROOT = '.'

class MainHandler(tornado.web.RequestHandler):
    #Requests for the landing page
    def get(self):
        self.render('search.html')

class StatesHandler(tornado.web.RequestHandler):
    #Requests for valid field values
    def initialize(self, db):
        self.db = db

    def get(self):
        self.write(dict(
            data=self.db.states())
        )

class SearchHandler(tornado.web.RequestHandler):
    #Requests for Searches
    def initialize(self, db):
        self.db = db
    
    def get(self):
        name = self.get_argument("name")
        state = self.get_argument("state")

        self.write(dict(
            data = self.db.search('%{}%'.format(name), '%{}%'.format(state)))
            )     

class DetailHandler(tornado.web.RequestHandler):
    #Requests for a single record

    def initialize(self, db):
        self.db = db
    
    def get(self):
        park_id = self.get_argument("park_id")

        self.write(dict(
            data = self.db.detail(park_id))
            )

class DetailHTMLHandler(tornado.web.RequestHandler):
    #Requests for a single record

    def initialize(self, db):
        self.db = db
    
    def post(self):
        park_id = self.get_argument("park_id")

        self.render('detail.html', data = self.db.detail(park_id))

class FactHandler(tornado.web.RequestHandler):
    #Requests a fact

    def initialize(self, db):
        self.db = db

    def get(self):
        self.write(dict(
            data = self.db.random_fact()
            ))

if __name__ == '__main__':
    db = ParksDB(os.path.join(ROOT, 'data'))
    
    app = tornado.web.Application([

            (r'/', MainHandler),
            (r'/states', StatesHandler, {'db': db}),
            (r'/search', SearchHandler, {'db': db}),
            (r'/detailHTML', DetailHTMLHandler, {'db': db}),
            (r'/fact', FactHandler, {'db': db}),
            
            # TODO: static content handlers
            (r'/css/(.*)', tornado.web.StaticFileHandler, {'path':'web_content/css'}),
            (r'/img/(.*)', tornado.web.StaticFileHandler, {'path':'web_content/img'}),
            (r'/js/(.*)', tornado.web.StaticFileHandler, {'path':'web_content/js'})
        ],
        template_path = os.path.join('web_content', 'html'),
        debug = True
    )

    app.listen(8880)
    tornado.ioloop.IOLoop.current().start()