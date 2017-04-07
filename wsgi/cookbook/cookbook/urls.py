import re
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.static import serve

urlpatterns = [
    url(r'^', include('public.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^recipes/', include('recipes.urls')),
    url(r'^admin/', include(admin.site.urls)),
    # /health, /env used by openshift
    url(r'^%s(?P<path>.*)$' % re.escape(settings.MEDIA_URL.lstrip('/')), serve, {'document_root': settings.MEDIA_ROOT}),
]
