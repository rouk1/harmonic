import os
import pickle
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile

import html2text
from django.forms import forms
from . import models

__author__ = 'rouk1'


class ImportLegacyDatabaseForm(forms.Form):
    zip_file = forms.FileField(required=True, help_text='zip file from o    ld site')


def import_page(name, path):
    with open(os.path.join(path, name, 'data'), 'rb') as f:
        data = pickle.load(f)

        if isinstance(data, models.HomePage):
            pass
        else:
            print(data.title_fr)
            print(data.title_en)

            print(html2text.html2text(data.text_en))
            print(html2text.html2text(data.text_fr))

            if hasattr(data, 'background'):
                print(data.background)

            print(data.description_fr)
            print(data.description_en)
            print(data.keywords)


def import_zip(zip_file):
    with ZipFile(zip_file) as zip:
        with TemporaryDirectory() as extract_path:
            zip.extractall(extract_path)

            sys.modules['models'] = models

            site_extracted_data = os.path.join(extract_path, 'site')
            for dir in os.listdir(site_extracted_data):
                import_page(dir, site_extracted_data)

            del sys.modules['models']
