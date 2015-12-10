import os
import pickle
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile

import html2text
from catalog.models import Page, HomePage, HomePagePush
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

        def copy_data(target, data):
            translation.activate('en')
            target.content = html2text.html2text(data.text_en)
            target.description = data.description_en
            translation.deactivate()

            translation.activate('fr')
            target.content = html2text.html2text(data.text_fr)
            target.description = data.description_fr
            translation.deactivate()

        if isinstance(data, models.HomePage):
            hp = HomePage()
            hp.keywords = data.keywords

            copy_data(hp, data)

            push = HomePagePush()
            translation.activate('en')
            push.title = data.push_title_en
            push.content = html2text.html2text(data.push_content_en)
            translation.deactivate()

            translation.activate('fr')
            push.title = data.push_title_fr
            push.content = html2text.html2text(data.push_content_fr)
            translation.deactivate()
            push.save()

            hp.save()

        else:
            p = Page()
            p.keywords = data.keywords
            p.slug = slugify(data.title_en.lower())

            copy_data(p, data)
            translation.activate('en')
            p.title = data.title_en
            translation.deactivate()

            translation.activate('fr')
            p.title = data.title_fr
            translation.deactivate()

            # FIXME store background image
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
            HomePagePush.objects.all().delete()
            for dir in os.listdir(site_extracted_data):
                import_page(dir, site_extracted_data)
                count += 1

            feedback.append((0, '{:d} page(s) imported'.format(count)))

            del sys.modules['models']

    return feedback
