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

"""OauthHandler handles callbacks from the Oauth2 flow."""


__author__ = 'Dan Holevoet <danielholevoet@google.com>'


import pickle

from google.appengine.api import memcache
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from sentimentally import utils

class OauthHandler(webapp.RequestHandler):
  """A webapp.RequestHandler to respond to all Oauth2 callbacks."""

  def get(self):
    user = users.get_current_user()
    flow = pickle.loads(memcache.get(user.user_id()))
    if flow:
      credentials = flow.step2_exchange(self.request.params)
      utils.store_credentials(user.user_id(), credentials)
      redirect = '/'
      if hasattr(flow, 'redirect_path') and flow.redirect_path:
        redirect = flow.redirect_path
      self.redirect(redirect)
    else:
      pass

# The application container that runs an OauthHandler and maps it to the
# /oauth2callback URI.
application = webapp.WSGIApplication(
    [('/oauth2callback', OauthHandler)],
    debug=True)

def main():
  """Run the OauthHandler application."""
  run_wsgi_app(application)

if __name__ == "__main__":
    main()
