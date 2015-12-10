#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = 'rouk1'

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
