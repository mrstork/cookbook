from django.conf import settings
from django.conf.urls import url
from django.views.generic import RedirectView

from public import views

urlpatterns = [
    url(r'.well-known/acme-challenge/Q5SduN6E7TdVdOf-5QctkLAUKfMpBcOGWU9uoe4PGrQ^$', views.letsencrypt_verification),
    url(r'^favicon\.ico$', RedirectView.as_view(url='%sfavicon.ico' % settings.STATIC_URL, permanent=True)),
    url(r'^$', views.index, name='landing-page'),
]
