from django.conf.urls import patterns, url
from . import views
from ideahub.apps.accounts.forms import LoginForm

urlpatterns = patterns('',
    # TODO: Fix these temporary mappings
    url(r'^login/?$', views.login, name='login'),
    url(r'^signup/?$', views.signup, name='signup'),
    url(r'^get_started/?$', views.get_started, name='get_started'),
    url(r'^user/(?P<pk>\d+)/?$', views.user, name='user'),
    url(r'^profile/?$', views.profile, name='profile'),
    url(r'^logout/?$', 'django.contrib.auth.views.logout', name='logout', kwargs={
        'next_page': 'login',
    }),
)


