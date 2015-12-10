#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = 'rouk1'

from django.shortcuts import render


def index(request):
    return render(request, 'pages/index.html')
