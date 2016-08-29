from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('public.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^recipes/', include('recipes.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
