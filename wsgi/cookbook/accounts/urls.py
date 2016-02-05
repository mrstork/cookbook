from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^request_account$', views.request_account, name='request_account'),
    url(r'^create_account/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.confirm_account, name='confirm_account'),
]
