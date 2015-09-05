__author__ = 'rouk1'

from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index),
]
