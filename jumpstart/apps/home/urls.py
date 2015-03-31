from django.conf.urls import patterns, url
from jumpstart.apps.home import views
from jumpstart.apps.home.views import IdeaDetail, IdeaUpdate, IdeaDelete, IdeaCreate


urlpatterns = patterns('',
   url(r'^/?$', views.index, name='index'),
   url(r'^ideas/?$', views.ideas, name='ideas'),
   url(r'^idea/(?P<pk>\d+)/?$', IdeaDetail.as_view(), name='idea'),
   url(r'^idea/create/?$', IdeaCreate.as_view(), name='idea_create'),
   url(r'^idea/(?P<pk>\d+)/edit/?$', IdeaUpdate.as_view(), name='idea_update'),
   url(r'^idea/(?P<pk>\d+)/delete/?$', IdeaDelete.as_view(), name='idea_delete'),
   url(r'^idea/(?P<pk>\d+)/rate/?$', views.idea_rate, name='idea_rate'),
   url(r'^ideas/cards/?$', views.idea_cards, name='idea_cards'),
)


