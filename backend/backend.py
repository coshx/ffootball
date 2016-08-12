import json

import tornado.ioloop
import tornado.httpserver
import tornado.web

import nfldb
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
        """Respond to POST requests with optimal allocations."""
        data = json.loads(self.request.body.decode('utf-8'))
        # Process data to make it usable
        clean_data = dict_from_data(data)
        # Call helper method, which will interact with the database
        fantasy_scores = get_scores()
        self.write(fantasy_scores)
        self.finish()


def make_app():
    tornado.options.parse_command_line()
    return tornado.web.Application([
        (r"/", MainHandler)
    ])


def get_scores(scoring_config):
    """Gets fields from database and applies scoring."""
    # TODO: Implement contact_database()
    stats = contact_database()
    # TODO: Implement scoring multiplication here
    fantasy_scores = stats * scoring_config
    return fantasy_scores


def dict_from_data(data):
    """Maps data from POST request to a Python dictionary"""
    output = {}
    data = dict(data)
    mapping = {"startDate": "start_date",
               "endDate": "end_date",
               "initialInvestment": "principle"}
    for k, v in data.items():
        if k in mapping:
            output[mapping[k]] = v
        else:
            output[k] = v
    return output


def main():
    """Runs application on httpserver with handler for '/'."""
    app = make_app()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    main()
