from django.conf import settings
from django.conf.urls import url
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    url(r'^favicon\.ico$', RedirectView.as_view(url='%sfavicon.ico' % settings.STATIC_URL, permanent=True)),
    url(r'^robots\.txt$', RedirectView.as_view(url='%srobots.txt' % settings.STATIC_URL, permanent=True)),
    url(r'^humans\.txt$', RedirectView.as_view(url='%shumans.txt' % settings.STATIC_URL, permanent=True)),
    url(r'^$', views.index),
]
