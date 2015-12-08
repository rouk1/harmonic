#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os

from django.contrib.auth.models import User
from django.test import TestCase, Client
from harmonic import settings
from legacy.importer import import_zip

__author__ = 'rouk1'


def create_superuser():
    admin_email = 'admin@admin.fr'
    admin_password = 'toto'
    User.objects.create_superuser(admin_email, admin_email, admin_password)
    return admin_email, admin_password


class LegacyImpoterTest(TestCase):
    def test_import(self):
        c = Client()

        admin_email, admin_password = create_superuser()
        c.login(username=admin_email, password=admin_password)

        zip_path = os.path.join(settings.BASE_DIR, 'legacy', 'testdata', '08_12_2015.zip')
        import_zip(zip_path)
