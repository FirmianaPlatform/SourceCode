'''
Created on 2013-7-10

@author: garfield
'''
from django.conf.urls import patterns, include, url
from leafy import settings
urlpatterns = patterns('repository.views',
                       (r'^$', 'repository'),
                       (r'^printHelloWorld_test/$', 'printHelloWorld_test'),
                       )
