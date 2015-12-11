from django.utils.translation import ugettext_lazy as _

from harmonic.mixins import SeoAdmin
from modeltranslation.admin import TranslationAdmin, TranslationStackedInline
from pages.models import HomePagePush
from renderer.widgets import MasterImageAdminMixin
from solo.admin import SingletonModelAdmin


class DefaultBackgroundAdmin(MasterImageAdminMixin, SingletonModelAdmin):
    pass


class PageAdmin(MasterImageAdminMixin, SeoAdmin, TranslationAdmin):
    list_display = ('slug', 'get_background',)
    list_display_links = ('slug', 'get_background',)
    search_fields = ('slug', 'content',)

    def get_background(self, obj):
        '''admin image tag for easy browse'''
        if obj.background is not None:
            t = (obj.background.get_rendition_url(100), obj.background.alternate_text)
        else:
            t = (
                'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAADYUlEQVR4Xu3caW7qQBAEYHwM5hrc/wbmGDC3eEROxAsBL7P0UmU3f5CI3d1TnxdkKQzjOD7O5/MpXv4J5JxPw+12+5dzHi6Xi/9EB57ger2eUkqPb5CU0jB9ECg+R8Qz+5zzL8g0SqDYg7xm/gESKLYg7yfALEig2KDMXY0WQQJFF2Xp1rAKEig6KGv36U2QQJFF2frSVAQSKDIoWxhTl2KQQOlDKcGoBgmUNpRSjCaQQKlDqcFoBgmUMpRajC6QQFlHacHoBgmUeZRWDBGQQPmL0oMhBhIoPyi9GKIgUgOV3S7xtpLAEAc5KooUhgrI0VAkMdRAjoIijaEKsncUDQx1kL2iaGGYgOwNRRPDDGQvKNoYpiDsKBYY5iCsKFYYLiBsKJYYbiAsKNYYriDoKB4Y7iCoKF4YECBoKJ4YMCAoKN4YUCDeKAgYcCBeKCgYkCDWKEgYsCBWKGgY0CDaKIgY8CBaKKgYFCDSKMgYNCBSKOgYVCC9KAwYdCCtKCwYlCC1KEwYtCClKGwY1CBbKIwY9CBLKKwYuwB5R2HG2A3IE2V6Z/95qar/U58WjPqazowAAdF5vUzFJcsZZQ6AGYX6krUWPCsKLUhJ4CXbOJ/gH+0pQWqCrtkWAYcOpCXgln28cKhAeoLt2dcShwZEIlCJGto4FCCSQUrW0sCBB9EIUKOmFA40iGZwmrV7cGBBLAKz6FGLAwliGZRlrxIcOBCPgDx6LuFAgXgG49n7FQcGBCEQhBkgQBCCeB6l3rO4g3gHMHct95zJFcRz4VvfeLxmcwPxWvAWxOvfPWZ0AfFYaA2EJ4o5CBOGx43eFIQRwxrFDIQZwxLFBGQPGFYo6iB7wrBAUQXZI4Y2ihrInjE0UVRAjoChhSIOciQMDRRRkCNiSKOIgRwZQxJFBCQwfp9+9WbRDdI7QOtDP+T9ejLpAulpjByoxGyt2TSDtDaUWCxLjZaMmkBaGrGEKD1nbVbVILUNpBfIWK8msyqQmsKMwWnOXJpdMUhpQc1FsdcuybAIpKQQe1hW829luQmyVcBqIXvqs5bpKkhg6B0GS9kuggSGHsbas69ZkMDQx1hC+QAJDDuMOZQ/IIFhj/GO8h8k5zyw//iXX5wynacTIqX0GMZxfKSUZKpGla4E7vf76QtfDj7Wr5LB3QAAAABJRU5ErkJggg==',
                'no background'
            )
        return '<img src="%s" alt="%s"/>' % t

    get_background.allow_tags = True
    get_background.short_description = _('background')


class HomePagePushAdmin(TranslationStackedInline):
    model = HomePagePush
    extra = 0


class HomePageAdmin(SeoAdmin, TranslationAdmin, SingletonModelAdmin):
    inlines = [
        HomePagePushAdmin
    ]
