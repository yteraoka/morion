from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^user/list$', views.view_user_list),
    url(r'^user/id/(?P<uid>[0-9]+)$', views.view_user_by_uid),
    url(r'^user/name/(?P<user_name>[a-zA-Z0-9_\-]+)$', views.view_user_by_name),
    url(r'^group/list$', views.view_group_list),
    url(r'^group/name/(?P<group_name>[a-zA-Z0-9_\-]+)$', views.view_group_by_name),
    url(r'^group/id/(?P<gid>[0-9]+)$', views.view_group_by_gid),
]
