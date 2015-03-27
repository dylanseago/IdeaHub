from django.conf.urls import patterns, url
from jumpstart.apps.home import views


urlpatterns = patterns('',
   url(r'^/?$', views.index, name='index'),
   url(r'^about/?$', views.about, name='about'),
   url(r'^user/(?P<user_id>\d+)/?', views.user, name='user'),
   url(r'^ideas/?$', views.ideas, name='ideas'),
   url(r'^idea/create/?$', views.post_idea, name='post_idea'),
   url(r'^idea/(?P<idea_id>\d+)/?', views.idea, name='idea'),
)


