import json

import tornado.ioloop
import tornado.httpserver
import tornado.web
import querydb

# from optimizer.utils import get_data
# from optimizer.optimize import optimize_portfolio

from tornado.options import define, options, parse_command_line

# Add command line flags
define("port", default=8000, help="run on the given port", type=int)
define("debug", default=False, help="run in debug mode")


class MainHandler(tornado.web.RequestHandler):
    """Handles post requests by responding with a JSON file."""
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Max-Age', 1000)
        #self.set_header('Access-Control-Allow-Headers', 'origin, x-csrftoken, content-type, accept')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Content-type', 'application/json')

    @tornado.web.asynchronous
    def get(self):
        """Respond to GET requests for debugging purposes."""
        self.write("Success!")
        self.finish()

    @tornado.web.asynchronous
    def post(self):
        """Respond to POST requests with scores."""
        scoring_config = json.loads(self.request.body.decode('utf-8'))
        print scoring_config
        # TODO: Get the timeframe from the POST request
        scores = querydb.get_scores(scoring_config, 2015)
        self.write(scores)
        self.finish()


class OnloadHandler(tornado.web.RequestHandler):
    """Handles post requests by responding with a JSON file."""
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Max-Age', 1000)
        #self.set_header('Access-Control-Allow-Headers', 'origin, x-csrftoken, content-type, accept')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Content-type', 'application/json')

    @tornado.web.asynchronous
    def get(self):
        """Respond to GET requests with JSON file."""
        scores = []
        with open('scores.json') as f:
            scores = json.load(f)
        self.write(scores)
        self.finish()

    @tornado.web.asynchronous
    def post(self):
        """Respond to POST requests with JSON file."""
        scores = []
        with open('scores.json') as f:
            scores = json.load(f)
        self.write(scores)
        self.finish()


def make_app():
    tornado.options.parse_command_line()
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/onload", OnloadHandler)
    ])


def main():
    """Runs application on httpserver with handler for '/'."""
    app = make_app()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
