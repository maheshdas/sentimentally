#!/usr/bin/env python
#
# Copyright 2011 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Provides auth utility methods."""


__author__ = 'danielholevoet@google.com (Dan Holevoet)'


import httplib2
import os
import pickle

from oauth2client.appengine import StorageByKeyName
from oauth2client.client import OAuth2WebServerFlow
from client.apiclient.discovery import build_from_document
from google.appengine.api import memcache

import model


ENDPOINT = 'https://www.googleapis.com'

MEMCACHE_LIFETIME = 3600

CLIENT_ID = ''
CLIENT_SECRET = ''
SCOPES = (
    'https://www.googleapis.com/auth/prediction',
)
USER_AGENT = 'sentimentally/0.1'
DOMAIN = 'anonymous'

CREDENTIALS_VERSION = 'v1'


def get_authorize_uri(callback, user_id=None, request_path='/'):
  """Generate the OAuth 2.0 authorization URI and store the flow in memcache
  if requested.

  Args:
    callback: The OAuth 2.0 redirect page.
    user_id: The ID of the user for which to store the flow. If None, the flow
             is not stored in memcache.
    request_path: The originally requested path. Only used if user_id is not
                  None.

  Returns:
    The OAuth 2.0 authorization URI.
  """
  flow = OAuth2WebServerFlow(client_id=CLIENT_ID,
                             client_secret=CLIENT_SECRET,
                             scope=' '.join(SCOPES),
                             user_agent=USER_AGENT,
                             domain=DOMAIN)
  flow.redirect_path = request_path
  authorize_url = flow.step1_get_authorize_url(callback)

  if user_id is not None:
    memcache.set(user_id, pickle.dumps(flow))
  return authorize_url


def get_credentials(user_id):
  """Get the stored OAuth2 credentials for the current user
  from the datastore.

  Args:
    user_id: Id of the user for which to get the credentials.

  Returns:
    The current user's creentials.
  """
  key = '%s_%s' % (CREDENTIALS_VERSION, user_id)
  credentials = StorageByKeyName(model.Credentials,
                                 key,
                                 'credentials').get()
  return credentials


def store_credentials(user_id, credentials):
  """Store the credentials in the datastore.

  Args:
    user_id: The ID of the user whose `credentials' is being stored.
    credentials: The credentials to store.
  """
  key = '%s_%s' % (CREDENTIALS_VERSION, user_id)
  StorageByKeyName(model.Credentials,
                   key,
                   'credentials').put(credentials)
