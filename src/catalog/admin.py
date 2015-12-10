from harmonic.mixins import SeoAdmin
from modeltranslation.admin import TranslationAdmin


class SectionAdmin(SeoAdmin, TranslationAdmin):
    pass
