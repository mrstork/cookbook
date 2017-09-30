from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'^', include('public.urls')),
    url(r'^', include('general.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^recipes/', include('recipes.urls')),
]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# This enables static files to be served from the Gunicorn server
# In Production, serve static files from Google Cloud Storage or an alternative
# CDN
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# if settings.DEBUG:
#     urlpatterns += staticfiles_urlpatterns()
