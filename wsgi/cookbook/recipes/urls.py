from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^add/$', views.add_view, name='add_recipe'),
    url(r'^(?P<user>.+)/(?P<slug>.+)/view$', views.detail_view, name='view_recipe'),
    url(r'^(?P<user>.+)/(?P<slug>.+)/edit$', views.edit_view, name='edit_recipe'),
    url(r'^(?P<user>.+)(/)?$', views.list_view, name='list_recipes'),
]
