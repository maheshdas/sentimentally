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

"""DefaultHandler is the default handler for unmapped sentimentally GET requests.

DefaultHandler simply yields a text/plain response with a message.
"""


__author__ = 'Vic Fryzel <vicfryzel@google.com>'


from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


class DefaultHandler(webapp.RequestHandler):
  """A webapp.RequestHandler to respond to all unmapped GET requests."""

  def get(self):
    """Yield a simple text message for a request."""
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write('Hello')


# The application container that runs a DefaultHandler and maps it to th / URI.
application = webapp.WSGIApplication(
    [('/', DefaultHandler)],
    debug=True)

def main():
  """Run the DefaultHandler application."""
  run_wsgi_app(application)

if __name__ == "__main__":
    main()
