from django.conf.urls import url

from general import views

urlpatterns = [
    url(r'^tea-party$', views.teapot),
]
