from recipes import views
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^create$', views.add_view, name='create-recipe'),
    url(r'^(?P<user>.+)/(?P<pk>[0-9]+)$', views.RecipeDetail.as_view(), name='recipe-detail'),
    url(r'^(?P<user>.+)/$', views.RecipeList.as_view(), name='recipe-list'),
    url(r'^(?P<user>.+)$', views.RecipeList.as_view(), name='recipe-list'),
    url(r'^$', views.base_view, name='all-recipes'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
