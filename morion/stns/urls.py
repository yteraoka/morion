from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^user/list$', views.user_list),
    url(r'^user/id/(?P<uid>[0-9]+)$', views.user_by_uid),
    url(r'^user/name/(?P<user_name>[a-zA-Z0-9_\-]+)$', views.user_by_name),
]
