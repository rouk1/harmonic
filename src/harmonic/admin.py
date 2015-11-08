#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''

'''

from django.conf.urls import patterns, url
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group, User
from django.forms import forms
from django.shortcuts import render


class HarmonicAdminSite(admin.AdminSite):
    '''override admin site to add custom views'''
    site_header = u'Harmonic'

    def import_legacy_catalog(self, request):
        if request.method == 'POST':
            form = ImportForm(request.POST, request.FILES)
            if form.is_valid():
                f = request.FILES['backup']
                sql_data = f.read()
                import_all(sql_data)

                messages.success(request, 'youhou')
        else:
            form = ImportForm()

        context = {
            'form': form
        }
        return render(request, 'admin/import.html', context)

    def get_urls(self):
        urls = super(HarmonicAdminSite, self).get_urls()
        extra_urls = patterns(
            '',
            url(
                r'^import/$',
                self.admin_view(self.import_legacy_catalog),
                name='import_database'
            )
        )

        return extra_urls + urls


# register models in custom site
site = HarmonicAdminSite()

# auth
site.register(User, UserAdmin)
site.register(Group, GroupAdmin)
