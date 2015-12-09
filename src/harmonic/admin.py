#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''

'''
from catalog.admin import PageAdmin
from catalog.models import Page
from django.conf.urls import url
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group, User
from django.shortcuts import render
from legacy.importer import ImportLegacyDatabaseForm, import_zip



class HarmonicAdminSite(admin.AdminSite):
    '''override admin site to add custom views'''
    site_header = 'Harmonic'
    site_title = 'Harmonic Administration'

    def import_legacy_catalog(self, request):
        if request.method == 'POST':
            form = ImportLegacyDatabaseForm(request.POST, request.FILES)
            if form.is_valid():
                import_zip(request.FILES['zip_file'])

                messages.success(request, 'youhou')
        else:
            form = ImportLegacyDatabaseForm()

        context = {
            'form': form
        }
        return render(request, 'admin/import.html', context)

    def get_urls(self):
        urls = super(HarmonicAdminSite, self).get_urls()
        extra_urls = [
            url(
                r'^import/$',
                self.admin_view(self.import_legacy_catalog),
                name='import_database'
            ),
        ]

        return extra_urls + urls


# register models in custom site
site = HarmonicAdminSite()

# auth
site.register(User, UserAdmin)
site.register(Group, GroupAdmin)

# catalog
site.register(Page, PageAdmin)
