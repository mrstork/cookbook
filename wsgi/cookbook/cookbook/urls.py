from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler400, handler403, handler404, handler500

handler404 = 'cookbook.views.page_not_found_view'
handler500 = 'cookbook.views.error_view'
handler403 = 'cookbook.views.permission_denied_view'
handler400 = 'cookbook.views.bad_request_view'

urlpatterns = [
    url(r'^', include('public.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^recipes/', include('recipes.urls')),
    url(r'^admin/', include(admin.site.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
