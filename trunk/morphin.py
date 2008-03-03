#!/usr/bin/env python

# Copyright (C) 2007-2008 Sebastian Ruml <sebastian.ruml@gmail.com>
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
#
#
# Potions of the code are form the WHAAW! Media Player
# <http://home.gna.org/whaawmp/> by Jeff Bailes.
# Thanks to Jeff Bailes for the great player.

import sys, os
import xdg.BaseDirectory

from src.common import globals
from src.services import log


__appName__ = 'morphin'


# Check that at least python 2.5 is running
if sys.version_info < (2, 5):
    print _('Cannot continue, python version must be at least 2.5.')
    sys.exit(1)

# Find out the location of morphine's working directory, and insert it to sys.path
basedir = os.path.dirname(os.path.realpath(__file__))
if not os.path.exists(os.path.join(basedir, "morphin.py")):
    if os.path.exists(os.path.join(os.getcwd(), "morphin.py")):
        basedir = os.getcwd()
sys.path.insert(0, basedir)
os.chdir(basedir) # Change dir to the base dir

import gettext
gettext.install(__appName__, unicode=1)

sys_var = "HOME"

# Initialize some global variables
globals.appName = __appName__
globals.niceAppName = 'Morphin'
globals.version = '0.0.3'
globals.srcDir = os.path.join(basedir, 'src')
globals.gladePath = os.path.join(globals.srcDir, 'glade')
globals.gladeFile = os.path.join(globals.gladePath, globals.appName + '.glade')
#globals.confDir = "%s%s%s" % (os.getenv(sys_var), os.sep, ".morphine") 
globals.confDir = xdg.BaseDirectory.save_config_path(globals.appName)
# Get the config file path
globals.cfgFile = os.path.join(globals.confDir, 'config.ini')
globals.dataDir = os.path.join(basedir, 'data')
globals.imageDir = os.path.join(globals.dataDir, 'images')
#globals.logger = Logger()


# FIXME: Quick hack for enable kiwi to find the glade file
from kiwi.environ import environ 
environ.add_resource('glade', globals.gladePath)

# find out if they are asking for help
HELP = False
for val in sys.argv:
    if val == '-h' or val == '--help': HELP = True

import pygtk
pygtk.require('2.0')
import gtk

from src import main as morphin
from src.services import config
from optparse import OptionParser 


def main():
	"""
        Everything dispatches from this main function.
	"""
	usage = "usage: %prog [options] mediafile"	

	# Parse the command line
	(options, args) = config.clParser(OptionParser(usage=usage, version=globals.version)).parseArgs(HELP)
	if HELP:
		sys.exit(0)

	# Load the settings

	# Create the main window
	mainWindow = morphin.MorphinWindow(options, args)

    # Jump in the main gtk loop
	gtk.main()


if __name__ == "__main__": 
	try:
		main()
	except SystemExit:
		raise
	except: # BaseException doesn't exist in python2.4
		import traceback
		traceback.print_exc()

