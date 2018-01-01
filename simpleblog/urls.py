#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.conf.urls import *
import views

urlpatterns = [
    url(r'^$', views.blog_list, name= 'bloglist_index'),
    url(r'^bloglist/$', views.blog_list, name='bloglist'),
    url(r'^blog/tag/(?P<id>\d+)/$', views.blog_filter, name='filtrblog'),
    url(r'^blog/search/$', views.blog_search, name='searchblog'),
    url(r'^blog/(?P<id>\d+)/$', views.blog_show, name='detailblog'),
    url(r'^blog/(?P<id>\w+)/del/$', views.blog_del, name='delblog'),
    url(r'^blog/(?P<id>\w+)/update/$', views.blog_update, name='updateblog'),
    url(r'^blog/add/$', views.blog_add, name='addblog'),
    url(r'^blog/addmassage/$', views.add_weibo, name='addmassage'),
    url(r'^blog/showweibo/$', views.show_weibo, name='showweibo'),
    url(r'^blog/(?P<id>\d+)/commentshow/$', views.blog_show_comment, name='showcomment'),
]