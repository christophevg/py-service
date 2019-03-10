"""
Base Class for services.

A Service consists of a class that runs forever and can optionally.be contacted
through an HTTP API. If the class provides a PORT class variable, the API is
set up and handles by default the /shutdown
"""

import sys
import time
import traceback
import threading
import json
import logging
import requests

from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from werkzeug.exceptions import HTTPException, NotFound

logging.getLogger("werkzeug").setLevel(logging.ERROR)

class base(object):

  PORT     = None
  HANDLERS = {}

  # the loop methos must be overridden to do something useful
  def loop(self):
    raise NotImplementedError
  
  # incoming API actions can be handled by handlers
  def execute_handler(self, action, data):
    return self.HANDLERS[action](self, data)

  def fatal(self, msg):
    logging.error(msg)
    sys.exit(1)

  def run_api(self):
    try:
      run_simple( "localhost", self.PORT, self )
    except OSError as e:
      self.running = False
      self.fatal("Couldn't start API, probably the port is in use.")

  # run method starts the service
  def run(self):
    # start API in a thread, if we have a port
    self.running = True
    if self.PORT:
      threading.Timer(0, self.run_api).start()
    try:
      time.sleep(1)  # wait 1s to catch e.g. port in use errors
      while self.running:
        self.loop()
    except KeyboardInterrupt:
      self.shutdown()
    except Exception as e:
      logging.error("crash: " + str(traceback.format_exc()))
  
  def shutdown(self, request):
    logging.info("shutdown requested")
    self.running = False
    if self.PORT:
      request.environ.get('werkzeug.server.shutdown')()
    self.finalize()

  def finalize(self):
    pass
  
  # HTTP API implementation
  def dispatch_request(self, request):
    try:
      {
        "/shutdown" : self.shutdown
      }[request.path](request)
    except KeyError:
      try:
        return Response(self.execute_handler(request.path, request.data))
      except Exception as e:
        logging.error(str(traceback.format_exc()))
        NotFound()
    return Response("ok")

  def wsgi_app(self, environ, start_response):
    request = Request(environ)
    response = self.dispatch_request(request)
    return response(environ, start_response)

  def __call__(self, environ, start_response):
    return self.wsgi_app(environ, start_response)

  # generic helper function to call into the HTTP API
  @classmethod
  def perform(cls, action, data=None):
    if cls.PORT:
      if data:
        return cls.post(cls.url(action), data)
      else:
        return cls.get(cls.url(action))

  @classmethod
  def post(cls, url, data):
    return requests.post(url, json=data)

  @classmethod
  def get(cls, url):
    return requests.get(url)

  @classmethod
  def url(cls, action, port=None):
    if port is None:
      port = cls.PORT
    if not port is None:
      return "http://localhost:" + str(port) + "/" + action
    else:
      return None

  # decorator for registering handlers
  @classmethod
  def handle(cls, action):
    def handler(f):
      cls.HANDLERS["/"+action] = f
      return f
    return handler

  # decorator for setting defining the endpoint
  @classmethod
  def endpoint(c, port=None):
    def handler(cls):
      cls.PORT = port
      return cls
    return handler

# cosmetic naming class wrapper something ;-)
class API(base):
  pass
