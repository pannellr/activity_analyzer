from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
     url(r'^$', include('activity_bucket.urls', namespace="activity_bucket")),
)
