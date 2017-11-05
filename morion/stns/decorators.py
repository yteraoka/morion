from .models import Server
from django.conf import settings
from django.http import HttpResponse
import logging
import base64
from passlib.hash import sha512_crypt

def auth_client(function):
    logger = logging.getLogger('debug')

    def basic_unauthed():
        response = HttpResponse('Authentication required')
        response['WWW-Authenticate'] = 'Basic realm="STNS"'
        response.status_code = 401
        return response

    def no_client_auth():
        response = HttpResponse('TLS client certificate required')
        response.status_code = 403
        return response

    def auth_server(server_name, password):
        server = Server.objects.get(name=server_name)
        if not server:
            return False
        return sha512_crypt.verify(password, server.password)

    def wrap(request, *args, **kwargs):
        if settings.CLIENT_AUTH_METHOD == 'TLS':
            if not request.META.has_key('HTTP_SSL_CLIENT_S_DN'):
                return no_client_auth()
            request.user = request.META['HTTP_SSL_CLIENT_S_DN']
        elif settings.CLIENT_AUTH_METHOD == 'basic':
            if request.META.get('HTTP_AUTHORIZATION', None) is None:
                return basic_unauthed()
            else:
                authentication = request.META['HTTP_AUTHORIZATION']
                logger.debug(authentication)
                (method, cred) = authentication.split(' ', 1)
                if 'basic' != method.lower():
                    return basic_unauthed()
                auth = base64.b64decode(cred.strip()).decode('utf-8')
                logger.debug(auth)
                username, password = auth.split(':', 1)
                if auth_server(username, password):
                    request.user = username
                else:
                    return basic_unauthed()

        logger.debug("Request User: {0}".format(request.user))

        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__

    return wrap
