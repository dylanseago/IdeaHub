from django.conf.urls import patterns, url
from jumpstart.apps.api import views


urlpatterns = patterns('',
   url(r'^ideas/?$', views.ideas, name='ideas'),
   url(r'^category_graph/?$', views.category_graph, name='category_graph')
)


