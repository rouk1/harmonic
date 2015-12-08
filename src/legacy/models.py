class PersistentObject(object):
    '''an object that can be pickle'''

    prefix = 'default'

    def __init__(self, name, prefix):
        self.name = name
        self.prefix = prefix or PersistentObject.prefix


class Artist(PersistentObject):
    '''an artist that has recorded a disc in the catalog'''

    prefix = 'artist'

    def __init__(self, name, prefix=None):
        super(Artist, self).__init__(name, Artist.prefix)


class Album(PersistentObject):
    '''an album off the catalog'''

    prefix = 'album'

    def __init__(self, name, prefix=None):
        super(Album, self).__init__(name, Album.prefix)


class Section(PersistentObject):
    '''an section off the catalog'''

    prefix = 'section'

    def __init__(self, name, prefix=None):
        super(Section, self).__init__(name, Section.prefix)


class Page(PersistentObject):
    '''an section off the catalog'''

    prefix = 'site'

    def __init__(self, name, prefix=None):
        super(Page, self).__init__(name, Page.prefix)


class HomePage(Page):
    '''an section off the catalog'''
    pass
