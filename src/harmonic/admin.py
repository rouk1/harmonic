#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''

'''
from catalog.admin import SectionAdmin, ArtistAdmin, AlbumAdmin
from catalog.models import Section, Artist, Album
from django.conf.urls import url
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group, User
from django.shortcuts import render
from legacy.importer import ImportLegacyDatabaseForm, import_zip
from pages.admin import PageAdmin, HomePageAdmin
from pages.models import Page, HomePage


class HarmonicAdminSite(admin.AdminSite):
    '''override admin site to add custom views'''
    site_header = 'Harmonic'
    site_title = 'Harmonic Administration'

    def import_legacy_catalog(self, request):
        if request.method == 'POST':
            form = ImportLegacyDatabaseForm(request.POST, request.FILES)
            if form.is_valid():
                feedbacks = import_zip(request.FILES['zip_file'])
                for (error, feedback) in feedbacks:
                    if error > 0:
                        messages.error(request, feedback)
                    else:
                        messages.success(request, feedback)
        else:
            form = ImportLegacyDatabaseForm()

        context = self.each_context(request)
        context['form'] = form
        
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

# pages
site.register(Page, PageAdmin)
site.register(HomePage, HomePageAdmin)

# catalog
site.register(Section, SectionAdmin)
site.register(Artist, ArtistAdmin)
site.register(Album, AlbumAdmin)
