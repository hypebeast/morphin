# -*- coding: utf-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=90:

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

from src.gstreamer import tools
from src.utils import utils
from src.gstreamer import tools


class MediaManager:
    def __init__(self):
        """
        """
        self._recentPlayed = []

        
    def getRecentPlayed(self):
        """
        """
        return self._recentPlayed
    
    
    def setRecentPlayed(self, uris):
        """
        """
        self._recentPlayed = uris
        
    
    def AddRecentPlayedMedia(self, uri, config):
        """
        """
        if not self.CheckMediaRecentPlayed(uri):
            self._recentPlayed.append(str(uri))
            
            # TODO: Get the length of the media and create a new config section
            dur = tools.getDuration(uri)
            
            print "duration: " + str(dur)
            
            #self.CreateConfSection(config, uri, dur)
    
    
    def CheckMediaRecentPlayed(self, uri):
        """
        """
        for i in self._recentPlayed:
            if i == uri:
                return True
            
        return False
    
    def RecentPlayedToConf(self):
        """
        """
        uris = ""
        
        for i in self._recentPlayed:
            uris = i + ', '
            
        return uris
    
    
    def CreateConfSection(self, config, uri, dur):
        """
        """
        config.set_option('duration', utils.secToStr(dur), uri)
    