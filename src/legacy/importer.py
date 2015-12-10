import os
import pickle
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile

import html2text
from catalog.models import Section, Artist
from pages.models import Page, HomePage, HomePagePush
from django.forms import forms
from django.utils import translation
from django.utils.text import slugify
from . import models

__author__ = 'rouk1'


class ImportLegacyDatabaseForm(forms.Form):
    zip_file = forms.FileField(required=True, help_text='zip file from old site')

def copy_seo_data(target, data):
    target.seo_keywords = data.keywords

    translation.activate('en')
    target.seo_description = data.description_en
    translation.deactivate()

    translation.activate('fr')
    target.seo_description = data.description_fr
    translation.deactivate()

def import_page(name, path):
    with open(os.path.join(path, name, 'data'), 'rb') as f:
        data = pickle.load(f)

        def copy_data(target, data):
            copy_seo_data(target, data)
            translation.activate('en')
            target.content = html2text.html2text(data.text_en)
            translation.deactivate()

            translation.activate('fr')
            target.content = html2text.html2text(data.text_fr)
            translation.deactivate()

        if isinstance(data, models.HomePage):
            hp = HomePage.get_solo()

            copy_data(hp, data)

            push = HomePagePush()
            push.home_page = hp
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


def import_section(name, path):
    with open(os.path.join(path, name, 'data'), 'rb') as f:
        data = pickle.load(f)

        s = Section()
        copy_seo_data(s, data)

        if data.title_color == 'black':
            s.title_color = '#000000'
        else:
            s.title_color = '#ffffff'

        translation.activate('en')
        s.title = data.title_en
        translation.deactivate()

        translation.activate('fr')
        s.title = data.title_fr
        translation.deactivate()

        # FIXME store background image
        if hasattr(data, 'background'):
            pass

        s.save()


def import_artist(name, path):
    with open(os.path.join(path, name, 'data'), 'rb') as f:
        data = pickle.load(f)

        a = Artist()
        a.name = data.name

        translation.activate('en')
        a.bio = html2text.html2text(data.bio_en)
        translation.deactivate()

        translation.activate('fr')
        a.bio = html2text.html2text(data.bio_fr)
        translation.deactivate()

        # FIXME store image
        if hasattr(data, 'photo'):
            pass

        a.save()



def import_zip(zip_file):
    feedback = []
    with ZipFile(zip_file) as zip:
        with TemporaryDirectory() as extract_path:
            zip.extractall(extract_path)

            sys.modules['models'] = models

            # delete
            Page.objects.all().delete()
            HomePagePush.objects.all().delete()

            # import
            count = 0
            site_extracted_data = os.path.join(extract_path, 'site')
            for dir in os.listdir(site_extracted_data):
                import_page(dir, site_extracted_data)
                count += 1

            feedback.append((0, '{:d} page(s) imported'.format(count)))

            # delete
            Section.objects.all().delete()

            # import
            count = 0
            section_extracted_data = os.path.join(extract_path, 'section')
            for dir in os.listdir(section_extracted_data):
                import_section(dir, section_extracted_data)
                count += 1

            feedback.append((0, '{:d} section(s) imported'.format(count)))

            # delete
            Artist.objects.all().delete()

            # import
            count = 0
            section_extracted_data = os.path.join(extract_path, 'artist')
            for dir in os.listdir(section_extracted_data):
                import_artist(dir, section_extracted_data)
                count += 1

            feedback.append((0, '{:d} artist(s) imported'.format(count)))

            del sys.modules['models']

    return feedback
