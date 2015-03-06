from django.conf.urls import patterns, include, url
from django.contrib import admin
from activity_bucket import views

urlpatterns = patterns('',
    url(r'^$', views.get_activity_data, name='the-form'),
)
