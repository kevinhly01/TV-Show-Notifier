from django.conf.urls import patterns, url
from subscription import views

urlpatterns = patterns('',
        url(r'^$', views.reminder, name='index'))