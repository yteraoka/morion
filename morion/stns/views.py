from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.utils import timezone
from django.conf import settings
from django.db.models import Q
from .decorators import auth_client
import json

from .models import User, Server, Group, UserGroupMembership

def meta_data(status, min_id):
    return {
      'api_version': 2.1,
      'result': status,
      'min_id': min_id,
    }


def get_users(request):
    if settings.CLIENT_AUTH_METHOD in ('TLS', 'basic'):
        server = Server.objects.prefetch_related('roles')\
                    .get(name=request.user)
        users = User.objects\
                    .filter(roles__in=[role.id for role in server.roles.all()])\
                    .filter(disabled=False)\
                    .filter(Q(expiry_date__gte=timezone.now())\
                          | Q(expiry_date__isnull=True))
    else:
        users = User.objects\
                    .filter(disabled=False)\
                    .filter(Q(expiry_date__gte=timezone.now())\
                          | Q(expiry_date__isnull=True))

    return users


def single_user_data(user):
    keys = []
    gid = -1
    for k in user.publickeys.all():
        keys.append(k.key)
    for g in user.groups.filter(usergroupmembership__primary=True):
        gid = g.gid
        break
    return {
        'metadata': meta_data('success', user.uid),
        'items': {
            user.name: {
                'id': user.uid,
                'password': user.password,
                'group_id': gid,
                'directory': user.directory,
                'shell': user.shell,
                'gecos': user.gecos,
                'keys': keys,
                'link_users': None,
            }
        }
    }


def json_response(data, request):
    if 'pretty' in request.GET:
        return HttpResponse(json.dumps(data, indent=4),
                            content_type='application/json')
    else:
        return HttpResponse(json.dumps(data),
                            content_type='application/json')


@auth_client
def view_user_list(request):
    users = get_users(request)
    result = {
        'items': [],
    }
    min_uid = -1
    for user in users:
        gid = -1
        if min_uid == -1 or user.uid < min_uid:
            min_uid = user.uid
        keys = []
        for k in user.publickeys.all():
            keys.append(k.key)
        for g in user.groups.filter(usergroupmembership__primary=True):
            gid = g.gid
            break
        result['items'].append({
            user.name: {
                'id': user.uid,
                'password': user.password,
                'group_id': gid,
                'directory': user.directory,
                'shell': user.shell,
                'gecos': user.gecos,
                'keys': keys,
                'link_users': None,
            }
        })
    result['metadata'] = meta_data('success', min_uid)
    return json_response(result, request)

@auth_client
def view_user_by_uid(request, uid):
    if settings.CLIENT_AUTH_METHOD in ('TLS', 'basic'):
        server = Server.objects.prefetch_related('roles')\
                    .get(name=request.user)
        users = User.objects\
                    .filter(uid=uid)\
                    .filter(roles__in=[role.id for role in server.roles.all()])\
                    .filter(disabled=False)\
                    .filter(Q(expiry_date__gte=timezone.now())\
                          | Q(expiry_date__isnull=True))
    else:
        users = User.objects\
                    .filter(uid=uid)\
                    .filter(disabled=False)\
                    .filter(Q(expiry_date__gte=timezone.now())\
                          | Q(expiry_date__isnull=True))

    if len(users) == 0:
        return HttpResponseNotFound('Resource not found')
    else:
        return json_response(single_user_data(users[0]), request)


@auth_client
def view_user_by_name(request, user_name):
    if settings.CLIENT_AUTH_METHOD in ('TLS', 'basic'):
        server = Server.objects.prefetch_related('roles')\
                    .get(name=request.user)
        users = User.objects\
                    .filter(name=user_name)\
                    .filter(roles__in=[role.id for role in server.roles.all()])\
                    .filter(disabled=False)\
                    .filter(Q(expiry_date__gte=timezone.now())\
                          | Q(expiry_date__isnull=True))
    else:
        users = User.objects\
                    .filter(name=user_name)\
                    .filter(disabled=False)\
                    .filter(Q(expiry_date__gte=timezone.now())\
                          | Q(expiry_date__isnull=True))
    
    if len(users) == 0:
        return HttpResponseNotFound('Resource not found')
    else:
        return json_response(single_user_data(users[0]), request)


def group_list(request):
    items = {}
    min_gid = 0
    users = get_users(request)
    for user in users:
        for group in user.groups.all():
            if min_gid == 0 or group.gid < min_gid:
                min_gid = group.gid
            if group.name not in items:
                items[group.name] = {
                    'id': group.gid,
                    'users': [],
                    'link_groups': None,
                }
            items[group.name]['users'].append(user.name)
    return min_gid, items


@auth_client
def view_group_list(request):
    result = {}
    min_gid, items = group_list(request)
    result = {
        'items': items,
        'metadata': meta_data('success', min_gid),
    }
    return json_response(result, request)


@auth_client
def view_group_by_gid(request, gid):
    result = {}
    min_gid, items = group_list(request)
    for group_name in items:
        if items[group_name]['id'] == int(gid):
            result['items'] = {
                group_name: items[group_name]
            }
            break
    result['metadata'] = meta_data('success', min_gid)
    return json_response(result, request)


@auth_client
def view_group_by_name(request, group_name):
    result = {}
    min_gid, items = group_list(request)
    if group_name not in items:
        return HttpResponseNotFound('Resource not found')
    result = {
            'items': {
	        group_name: items[group_name],
            },
            'metadata': meta_data('success', min_gid),
    }
    return json_response(result, request)
