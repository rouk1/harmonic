import os
import pickle
import sys
from tempfile import TemporaryDirectory
from zipfile import ZipFile

import html2text
from catalog.models import Section, Artist, Album
from django.core.files.base import File
from django.db import transaction
from django.forms import forms
from django.utils import translation
from django.utils.text import slugify
from pages.models import Page, HomePage, HomePagePush
from renderer.models import MasterImage
from . import models

__author__ = 'rouk1'


class ImportLegacyDatabaseForm(forms.Form):
    zip_file = forms.FileField(
        required=True,
        help_text='zip file from old site'
    )


def copy_seo_data(target, data):
    target.seo_keywords = data.keywords

    translation.activate('en')
    target.seo_description = data.description_en
    translation.deactivate()

    translation.activate('fr')
    target.seo_description = data.description_fr
    translation.deactivate()


def make_master_image(path, legacy_path, alternate_text):
    image_path = os.path.join(path, '..', legacy_path)
    image_path = os.path.normpath(image_path)

    with open(image_path, 'rb') as img:
        master_image = MasterImage(
            alternate_text=alternate_text
        )
        master_image.master.save(os.path.basename(legacy_path), File(img))
        master_image.save()

    return master_image


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

            if hasattr(data, 'background'):
                img = make_master_image(
                    path,
                    data.background,
                    '{}-background'.format(data.title_en)
                )
                p.background = img

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

        if hasattr(data, 'background'):
            img = make_master_image(
                path,
                data.background,
                '{}-background'.format(data.title_en)
            )
            s.background = img

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

        if hasattr(data, 'photo'):
            master_image = make_master_image(path, data.photo, a.name)
            a.photo = master_image

        a.save()


def import_album(name, path):
    with open(os.path.join(path, name, 'data'), 'rb') as f:
        data = pickle.load(f)

        a = Album()
        copy_seo_data(a, data)

        a.is_published = data.published
        a.title = data.title
        a.reference = data.reference

        a.itunes_url = data.itunes_url
        a.is_digital_release = data.digital_release
        a.track_list = html2text.html2text(data.track_list)

        translation.activate('en')
        a.description = html2text.html2text(data.description_en)
        a.musicological_text = html2text.html2text(data.music_text_en)
        a.instrument_name = data.insturment_name_en
        a.instrument_text = html2text.html2text(data.instrument_text_en)
        a.press_review = html2text.html2text(data.review_en)
        translation.deactivate()

        translation.activate('fr')
        a.description = html2text.html2text(data.description_fr)
        a.musicological_text = html2text.html2text(data.music_text_fr)
        a.instrument_name = data.insturment_name_fr
        a.instrument_text = html2text.html2text(data.instrument_text_fr)
        a.press_review = html2text.html2text(data.review_fr)
        translation.deactivate()

        cover = make_master_image(path, data.cover, a.reference)
        a.cover = cover

        if hasattr(data, 'instrument_photo') and isinstance(data.instrument_photo, str):
            instrument_photo = make_master_image(
                path,
                data.instrument_photo,
                '{}-instrument'.format(a.reference)
            )
            a.instrument_photo = instrument_photo

        a.save()

        translation.activate('fr')
        section = Section.objects.get(title__iexact=data.section)
        a.sections.add(section)
        translation.deactivate()

        for artist in data.artist:
            a.artists.add(Artist.objects.get(name__iexact=artist))


@transaction.atomic
def import_zip(zip_file):
    feedback = []
    with ZipFile(zip_file) as zip:
        with TemporaryDirectory() as extract_path:
            zip.extractall(extract_path)

            sys.modules['models'] = models

            # delete all master iamges
            MasterImage.objects.all().delete()

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

            # delete
            Album.objects.all().delete()

            # import
            count = 0
            section_extracted_data = os.path.join(extract_path, 'album')
            for dir in os.listdir(section_extracted_data):
                import_album(dir, section_extracted_data)
                count += 1

            feedback.append((0, '{:d} album(s) imported'.format(count)))

            del sys.modules['models']

    return feedback
