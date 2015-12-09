import os
import pickle
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile

import html2text
from catalog.models import Page
from django.forms import forms
from django.utils import translation
from django.utils.text import slugify
from . import models

__author__ = 'rouk1'


class ImportLegacyDatabaseForm(forms.Form):
    zip_file = forms.FileField(required=True, help_text='zip file from old site')


def import_page(name, path):
    with open(os.path.join(path, name, 'data'), 'rb') as f:
        data = pickle.load(f)

        if isinstance(data, models.HomePage):
            pass
        else:
            p = Page()
            p.keywords = data.keywords
            p.slug = slugify(data.title_en.lower())

            translation.activate('en')
            p.title = data.title_en
            p.content = html2text.html2text(data.text_en)
            p.description = data.description_en
            translation.deactivate()

            translation.activate('fr')
            p.title = data.title_fr
            p.content = html2text.html2text(data.text_fr)
            p.description = data.description_fr
            translation.deactivate()

            # FIXME store backgroudn image
            if hasattr(data, 'background'):
                pass

            p.save()


def import_zip(zip_file):
    feedback = []
    with ZipFile(zip_file) as zip:
        with TemporaryDirectory() as extract_path:
            zip.extractall(extract_path)

            sys.modules['models'] = models

            site_extracted_data = os.path.join(extract_path, 'site')
            count = 0

            Page.objects.all().delete()
            for dir in os.listdir(site_extracted_data):
                import_page(dir, site_extracted_data)
                count += 1

            feedback.append((0, '{:d} page(s) imported'.format(count)))

            del sys.modules['models']

    return feedback