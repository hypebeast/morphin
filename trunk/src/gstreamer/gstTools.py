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

import pygst
pygst.require('0.10')
import gst

from src.common import globals
from src.utils import utils
from gst.extend import discoverer


def vsinkDef():
    """
    The method returns the first videosink that is available on the system.
    """
    for x in globals.vsinkTypes:
        if gst.element_factory_find(x):
            return x

    return None    


def messageType(message):
	## Returns the message type as a string.
	types = { gst.MESSAGE_EOS : 'eos',
	          gst.MESSAGE_ERROR : 'error',
	          gst.MESSAGE_STATE_CHANGED : 'state_changed' }
	# Try and return the corresponding sting, if it's not listed, return 'other'.
	try:
		return types[message.type]
	except KeyError:
		return 'other'


## State change checkers, msg[0] is old, [1] is new, [2] is pending.
def isNull2ReadyMsg(msg):
    """
    Checks if the player was just initialised from NULL to READY.
    """
    return (msg[0] == gst.STATE_NULL and msg[1] == gst.STATE_READY)


def isPlayMsg(msg):
    """
    Checks if the player has just started playing.
    """
    # (Always goes via PAUSED)
    return (msg[0] == gst.STATE_PAUSED and msg[1] == gst.STATE_PLAYING)


def isPlay2PauseMsg(msg):
    """
    Checks if the player has just paused from playing.
    """
    # (Goes via this on it's way to stop too)
    return (msg[0] == gst.STATE_PLAYING and msg[1] == gst.STATE_PAUSED)


def isStop2PauseMsg(msg):
    """
    Checks if the player has just paused from stopped.
    """
    # (Does this on it's way to playing too)
    return (msg[0] == gst.STATE_READY and msg[1] == gst.STATE_PAUSED)


def isStopMsg(msg):
    """
    Checks if the player has just stopped playing.
    """
    # (Goes via paused when stopping even if it was playing)
    return (msg[0] == gst.STATE_PAUSED and msg[1] == gst.STATE_READY)


def getDuration(uri):
    def on_discovered(d, is_media, infile):
        print "Infile: %s" % infile
        d.print_info()
        if is_media:
            print "Video length: %s" % d.videolength
            return utils.nsTos(d.videolength)
        else:
            pass
            
    d = discoverer.Discoverer(uri)
    d.connect('discovered', on_discovered, uri)
    d.discover()
    


class DefaultPlayer:
    def __init__(self):
        self.createPlayer()
        
    
    def createPlayer(self):
        """
        """
        self.player = gst.element_factory_make("playbin", "player")
        
        
    # Returns the total duration seconds.
    getDurationSec = lambda self: utils.nsTos(self.getDuration())


    def getDuration(self):
        # Returns the duration (nanoseconds).
        try:
            return self.player.query_duration(gst.FORMAT_TIME)[0]
        except:
            return 0
    
        
    def setURI(self, uri):
        """
        This method sets the URI for the player
        """
        self.player.set_property('uri', uri)

