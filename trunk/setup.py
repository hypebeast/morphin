# -*- coding: utf-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=90:

# Copyright (C) 2008 Sebastian Ruml <sebastian.ruml@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 1, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

from distutils.core import setup
from distutils.command.install_data import install_data
from distutils.command.install_lib import install_lib
import distutils.dir_util
from distutils import cmd
import glob
import os

NAME = "Morphin"
VERSION = "0.0.5"

DESC = "Simple video player"

LONG_DESC = """"""

# A dictionary for bash scripts and their destination python files.
scripts = {'morphin' : 'morphin.py'}

def replaceStr(file, orig, new):
    ## A function to replace a string with a new string in a given file.
    # Open, read then close the file.
    f = open(file, 'r')
    data = f.read()
    f.close()
    # Replace the string in the data which was read.
    data = data.replace(orig, new)
    # Write the new data back into the file.
    f = open(file, 'w')
    f.write(data)
    f.close()


class libInstall(install_lib):
    ## A class to extend the installation of libraries.
    def run(self):
        # Get the follwing paths.
        root = getattr(self.get_finalized_command('install'), 'root')
        prefix = getattr(self.get_finalized_command('install'), 'prefix')
        libDir = getattr(self.get_finalized_command('build'), 'build_lib')
        
        # To fix the datadir location in morphin.py.
        filename = os.path.join(libDir, 'morphin', 'morphin.py')
        datadir = os.path.join(prefix, 'share', 'morphin', 'data')
        replaceStr(filename, '@dataDir@', datadir)
        
        # To fix the gladedir location in morphin.py.
        filename = os.path.join(libDir, 'morphin', 'morphin.py')
        datadir = os.path.join(prefix, 'share', 'morphin', 'glade')
        replaceStr(filename, '@gladePath@', datadir)
        
        # Run the distutils install_lib function.
        res = install_lib.run(self)
        # Change the datadir in useful.py back to '@datadir@'.
        #replaceStr(filename, datadir, '@datadir@')
        return res


class dataInstall(install_data):
    ## A class to extend the installation of data.
    def run(self):
        # Get the libdir.
        libDir = getattr(self.get_finalized_command('install'), 'install_lib')
        
        if (self.root and libDir.startswith(self.root)):
            # If root dir is defined, and the libDir starts with it, remove it
            # (and add 'morphin' to the end).
            basedir = os.path.join(libDir[len(self.root):], 'morphin')

            if not (basedir.startswith('/')):
                basedir = '/' + basedir
        else:
            # Otherwise, just add the 'morphin'.
            basedir = os.path.join(libDir, 'morphin')
        for x in scripts:
            # For all the scripts defined before.
            # Open the sh script file.
            f = open(x, 'w')
            # Write the appropriate command to the script then close it.
            f.write('#!/bin/sh\nexec python %s/%s "$@"' % (basedir, scripts[x]))
            f.close()
            # Make it executable.
            os.system('chmod 755 %s' % x)
            # Run the distutils install_data function.

        return install_data.run(self)


# A list of tuples containing all the data files & their destinations.
DATA_FILES = [("share/morphin/glade", glob.glob('src/glade/*.glade')),
              ('share/morphin/data/images', glob.glob('data/images/*.png') + glob.glob('data/images/*.svg')),
              ('share/pixmaps', ['data/images/morphin_icon.svg']),
              ('share/icons/hicolor/scalable/apps', ['data/images/morphin_icon.svg']),
              ('share/applications', ['morphin.desktop']),
              ('bin', scripts.keys())]

PACKAGES = ['morphin',
            'morphin.src',
            'morphin.src.gui',
            #'morphin.glade',
            'morphin.src.common',
            'morphin.src.gstreamer',
            'morphin.src.MediaManagement',
            'morphin.src.services',
            'morphin.src.utils']


# The actual setup thing, mostly self explanatory.
setup (name             = NAME,
       version          = VERSION,
       author           = 'Sebastian Ruml',
       author_email     = 'sebastian.ruml@gmail.com',
       url              = 'http://code.google.com/p/morphin/',
       description      = DESC,
       long_description = LONG_DESC,
       license          = 'GPL2',
       url              = 'http://code.google.com/p/morphin/',
       download_url     = 'http://code.google.com/p/morphin/downloads/list',
       packages         = PACKAGES,
       package_dir      = {'morphin' : '.'},
       data_files       = DATA_FILES,
       cmdclass         = {'install_lib' : libInstall,
                           'install_data' : dataInstall}
)
