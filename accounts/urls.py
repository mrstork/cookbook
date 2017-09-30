from django.conf.urls import url, include

from accounts import views

urlpatterns = [
    url(r'^login$', views.authentication, name='login'),
    url(r'^register$', views.register, name='register'),
    url(r'^request_account$', views.request_account, name='request_account'),
    url(r'^create_account/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.confirm_account, name='confirm_account'),
    url(r'^logout$', views.logout_view, name='logout'),
]
