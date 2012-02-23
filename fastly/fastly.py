import httplib
import urllib
import json

from connection import *
from auth import *
from errors import *
from models import *

class API(object):
    def __init__(self, host='api.fastly.com', secure=True, port=None, root='',
                 timeout=5.0, key=None):
        self.conn = Connection(host, secure, port, root, timeout)

        if key:
            self.authenticate_by_key(key)


    def authenticate_by_key(self, key):
        self.conn.authenticator = KeyAuthenticator(key)

    def authenticate_by_password(self, login, password):
        self.conn.authenticator = SessionAuthenticator(self.conn, login, password)

    def deauthenticate(self):
        self.conn.authenticator = None


    def service(self, id):
        return Service.find(self.conn, id=id)

    def version(self, service_id, version):
        return Version.find(self.conn, service_id=service_id, number=version)

    def domain(self, service_id, version, name):
        return Domain.find(self.conn, service_id=service_id, version=version, name=name)

    def backend(self, service_id, version, name):
        return Backend.find(self.conn, service_id=service_id, version=version, name=name)


    def purge_url(self, host, path):
        resp, data = self.conn.request('PURGE', path, headers={'Host':host})
        return resp.status == 200
