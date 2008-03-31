# -*- coding: utf-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=90:

# Copyright (C) 2007 Sebastian Ruml <sebastian.ruml@gmail.com>
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

import os.path


IDLE_TIMEOUT = 3000

## A list of video-sinks, (in order of preference).
vsinkTypes = [ 'xvimagesink', 'ximagesink', 'glimagesink', 'directdrawsink', 'fakesink' ]

# List of video sinks which support color and aspect settings
vsinkColour = ['xvimagesink']
vsinkAspect = ['xvimagesink', 'ximagesink']

# Default settings
defaultConfig = { 'video/brightness' : 0,
                  'video/contrast' : 0,
                  'video/hue' : 0,
                  'video/saturation' : 0,
                  'video/force-aspect-ration' : True,
                  'video/videosink' : 'default' }

# Default configuration
DEFAULT_CONFIG = """\
[general]
appWidth = 480
appHeight = 320
recentMedia = []
lastOpenedFolder = ""

[video]
brightness = 0
contrast = 0
hue = 0
saturation = 0
force-aspect-ration = True
videosink = 'default'"""


## The mime type list of compatable files, for open dialogue.
compatibleFiles = ['application/ogg', 'application/ram', 'application/smil',
                   'application/vnd.rn-realmedia', 'application/x-extension-m4a',
                   'application/x-extension-mp4', 'application/x-flac',
                   'application/x-flash-video', 'application/x-matroska',
                   'application/x-ogg', 'application/x-quicktime-media-link',
                   'application/x-quicktimeplayer', 'application/x-shockwave-flash',
                   'text/google-video-pointer', 'text/x-google-video-pointer', 'video/3gpp',
                   'video/dv', 'video/fli', 'video/flv', 'video/mp4', 'video/mp4v-es',
                   'video/mpeg', 'video/msvideo', 'video/quicktime', 'video/vivo',
                   'video/vnd.divx', 'video/vnd.rn-realvideo', 'video/vnd.vivo', 'video/x-anim',
                   'video/x-avi', 'video/x-flc', 'video/x-fli', 'video/x-flic', 'video/x-m4v',
                   'video/x-matroska', 'video/x-mpeg', 'video/x-ms-asf', 'video/x-msvideo',
                   'video/x-ms-wm', 'video/x-ms-wmv', 'video/x-ms-wmx', 'video/x-ms-wvx',
                   'video/x-nsv', 'video/x-ogm+ogg', 'video/x-theora+ogg', 'text/uri-list']


# This list contains all widgets that should be hidden in fullscreen mode
hiddenFSWidgets = ['menubar', 'bTogglePlay', 'hScaleProgress', 'bFullscreen', 'statusbar', 'hbox3']

# List of widgets to reshow, in fullscreen mode, when the mouse is moved 
showFSWidgets = ['bFullscreen', 'hScaleProgress', 'bTogglePlay', 'hbox3']

# Pix data for hidden cursors.
hiddenCursorPix = """/* XPM */
                     static char * invisible_xpm[] = {
                     "1 1 1 1",
                     "       c None",
                     " "};"""

