from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.utils import timezone
from django.conf import settings
from django.db.models import Q
from .decorators import auth_client
import json

from .models import User, Server

def meta_data(status):
    return {
      'api_version': settings.API_VERSION,
      'result': status,
      'min_id': settings.MIN_ID,
    }


@auth_client
def user_list(request):
    if settings.CLIENT_AUTH_METHOD in ('TLS', 'basic'):
        server = Server.objects.prefetch_related('roles')\
                    .get(name=request.user)
        #for role in server.roles.all():
        #    print(role.id)
        #    print(role.name)
        users = User.objects.select_related()\
                    .prefetch_related('publickeys')\
                    .prefetch_related('roles')\
                    .filter(roles__in=[role.id for role in server.roles.all()])\
                    .filter(disabled=False)\
                    .filter(Q(expiry_date__gte=timezone.now())\
                          | Q(expiry_date__isnull=True))
    else:
        users = User.objects.select_related()\
                    .prefetch_related('publickeys')\
                    .filter(disabled=False)\
                    .filter(Q(expiry_date__gte=timezone.now())\
                          | Q(expiry_date__isnull=True))
    result = {
        'metadata': meta_data('success'),
        'items': [],
    }
    for user in users:
        keys = []
        for k in user.publickeys.all():
            keys.append(k.key)
        result['items'].append({
            user.name: {
                'id': user.uid,
                'password': user.password,
                'group_id': user.group.gid,
                'directory': user.directory,
                'shell': user.shell,
                'gecos': user.gecos,
                'keys': keys,
                'link_users': None,
            }
        })
    return HttpResponse(json.dumps(result, indent=4),
                        content_type='application/json')

def user_data(user):
    keys = []
    for k in user.publickeys.all():
        keys.append(k.key)
    return {
        'metadata': meta_data('success'),
        'items': {
            user.name: {
                'id': user.uid,
                'password': user.password,
                'group_id': user.group.gid,
                'directory': user.directory,
                'shell': user.shell,
                'gecos': user.gecos,
                'keys': keys,
                'link_users': None,
            }
        }
    }

@auth_client
def user_by_uid(request, uid):
    users = User.objects.select_related()\
                .prefetch_related('publickeys')\
                .filter(uid=uid)\
                .filter(disabled=False)\
                .filter(Q(expiry_date__gte=timezone.now()) | Q(expiry_date__isnull=True))
    if len(users) == 0:
        return HttpResponseNotFound('Resource not found')
    else:
        return HttpResponse(json.dumps(user_data(users[0]), indent=4),
                            content_type='application/json')


@auth_client
def user_by_name(request, user_name):
    users = User.objects.select_related()\
                .prefetch_related('publickeys')\
                .filter(name=user_name)\
                .filter(disabled=False)\
                .filter(Q(expiry_date__gte=timezone.now()) | Q(expiry_date__isnull=True))
    
    if len(users) == 0:
        return HttpResponseNotFound('Resource not found')
    else:
        return HttpResponse(json.dumps(user_data(users[0]), indent=4),
                        content_type='application/json')
