from django.conf import settings
from django.conf.urls import url
from django.views.generic import RedirectView

from public import views

urlpatterns = [
    url(r'^favicon\.ico$', RedirectView.as_view(url='%sfavicon.ico' % settings.STATIC_URL, permanent=True)),
    url(r'^$', views.index, name='landing-page'),
]
