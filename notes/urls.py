# define url patterns for app notes
from django.conf.urls import url

from . import views


app_name = 'notes'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^topics/$', views.topics, name='topics'),
    url(r'^topics/(?P<pk>\d+)$', views.topic, name='topic'),
    url(r'^new_topic/$', views.new_topic, name='new_topic'),
    url(r'^edit_topic/(?P<topic_pk>\d+)/$', views.edit_topic, name="edit_topic"),
    url(r'^delete_topic/(?P<topic_pk>\d+)/$', views.delete_topic, name="delete_topic"),
    url(r'^new_entry/(?P<topic_pk>\d+)/$', views.new_entry, name='new_entry'),
    url(r'^edit_entry/(?P<entry_pk>\d+)/$', views.edit_entry, name='edit_entry'),
    url(r'^delete_entry/(?P<entry_pk>\d+)/$', views.delete_entry, name='delete_entry'),
]

