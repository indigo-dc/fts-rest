#   Copyright notice:
#   Copyright CERN, 2016.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from paste.deploy.converters import asbool
from sqlalchemy.exc import TimeoutError
from webob.exc import HTTPServiceUnavailable


class TimeoutHandler(object):
    """
    Catch Timeout and similar errors, and return an HTTPServiceUnavailable instead
    """

    def __init__(self, wrap_app, config):
        self.app = wrap_app
        self.config = config

    def __call__(self, environ, start_response):
        try:
            return self.app(environ, start_response)
        except TimeoutError:
            if asbool(self.config.get('debug')):
                raise
            else:
                return HTTPServiceUnavailable()(environ, start_response)
