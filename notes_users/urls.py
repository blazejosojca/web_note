# define url patterns for app notes_users
from django.conf.urls import url
from django.contrib.auth.views import login

from . import views
app_name = 'notes_users'


urlpatterns = [
    url(r'^login/$', login, {'template_name': 'notes_users/login.html'}, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^register/$', views.register_view, name='register'),
]