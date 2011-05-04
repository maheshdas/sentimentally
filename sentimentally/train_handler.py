#!/usr/bin/env python
#
# Copyright 2011 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""TrainHandler handles requests to train our prediction model.

TrainHandler simply yields a text/plain response with a message.
"""


__author__ = 'Dan Holevoet <danielholevoet@google.com>'


import httplib2
import os
import pickle
import sys

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from client.apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run

from sentimentally import utils

class TrainHandler(webapp.RequestHandler):
  """A webapp.RequestHandler to respond to all training requests."""

  # The name of the Google Storage object holding training data.
  OBJECT_NAME = ''

  def get(self):
    user = users.get_current_user()
    credentials = utils.get_credentials(user.user_id())
    if credentials is None:
      callback = self.request.relative_url('/oauth2callback')
      authorize_url = utils.get_authorize_uri(callback, user.user_id(),
                                              self.request.path)
      self.redirect(authorize_url)
      return

    http = httplib2.Http()
    credentials.authorize(http)
    service = build("prediction", "v1.2", http=http)
    train = service.training()
    start = train.insert(data=OBJECT_NAME, body={}).execute()

    """Yield a simple text message for a request."""
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write('Started training')


# The application container that runs a PredictHandler and maps it to the
# /predict URI.
application = webapp.WSGIApplication(
    [('/train', TrainHandler)],
    debug=True)

def main():
  """Run the TrainHandler application."""
  run_wsgi_app(application)

if __name__ == "__main__":
    main()
