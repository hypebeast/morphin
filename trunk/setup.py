from distutils.core import setup

NAME = "Morphin"
VERSION = "0.0.2"

DESC = "Simple video player"

LONG_DESC = """"""

DATA_FILES = [("share/games/pychess",
    ["README", "AUTHORS", "LICENSE", "open.db"])]

# UI
DATA_FILES += [("share/games/pychess/glade", glob('glade/*.glade'))]
DATA_FILES += [("share/games/pychess/glade", glob('glade/*.png'))]
DATA_FILES += [("share/games/pychess/flags", glob('flags/*.png'))]

# Sidepanel (not a package)
DATA_FILES += [("share/games/pychess/sidepanel", glob('sidepanel/*.glade'))]
DATA_FILES += [("share/games/pychess/sidepanel", glob('sidepanel/*.py'))]
DATA_FILES += [("share/games/pychess/sidepanel", glob('sidepanel/*.pyc'))]
DATA_FILES += [("share/games/pychess/sidepanel", glob('sidepanel/*.pyo'))]

# Data
DATA_FILES += [('share/applications', ['pychess.desktop'])]
DATA_FILES += [('share/icons/hicolor/scalable/apps', ['pychess.svg'])]
DATA_FILES += [('share/pixmaps', ['pychess.svg'])]
DATA_FILES += [('share/icons/hicolor/24x24/apps', ['pychess.png'])]
DATA_FILES += [('share/gtksourceview-1.0/language-specs', ['gtksourceview-1.0/language-specs/pgn.lang'])]

setup (name='Morphin',
      version          = VERSION,
      author           = 'Sebastian Ruml',
      author_email     = 'sebastian.ruml@gmail.com',
      url              = 'http://code.google.com/p/morphin/',
      description      = DESC,
      long_description = LONG_DESC,
      license          = 'GPL2',
      url              = 'http://code.google.com/p/morphin/',
      download_url     = '',
      package_dir      = {'': 'lib'},
      packages         = PACKAGES,
      data_files       = DATA_FILES,
      scripts          = ['pychess']
)