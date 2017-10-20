from django.conf.urls import url
from main import views

urlpatterns = [
    url(r'^$', views.default, name='default'),
    url(r'^request/ehub_id/?$', views.RequestEhubID.as_view(), name='Request Ehub ID'),
    url(r'^authenticate/?$', views.Authenticate.as_view(), name='Authenticate'),
    url(r'^source/(?P<ehub_id>[0-9]+)/?$', views.Source.as_view(), name='Source'),
    url(r'^user/?$', views.User.as_view(), name='User'),
    url(r'^user/(?P<user_id>[0-9a-z-]+)/?$', views.User.as_view(), name='User'),
    url(r'^entry/(?P<id>[0-9a-z-]+)/?$', views.FormStatus.as_view(), name='FormStatus'),
    url(r'^form/(?P<ehub_id>[0-9]+)/?$', views.Form.as_view(), name='Form'),
    url(r'^client/?$', views.RetrieveTokens.as_view(), name='RetrieveTokens'),
]