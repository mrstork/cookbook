from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^create/$', views.add_view, name='create-recipe'),
    url(r'^(?P<user>.+)/(?P<slug>.+)/view$', views.detail_view, name='view-recipe'),
    url(r'^(?P<user>.+)/(?P<slug>.+)/edit$', views.edit_view, name='edit-recipe'),
    url(r'^(?P<user>.+)(/)?$', views.list_view, name='list-recipes'),
    url(r'^$', views.base_view),
]
