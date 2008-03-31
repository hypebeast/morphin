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

import datetime

from src.utils import utils


class MediaFile:
    """
    Class that describes one media file. It holds all import information for a
    media file.
    
    Each media file is uniquely identified by it's URI.
    """
    def __init__(self, uri, length=0, lastPlayed=""):
        """
        Constructor.
        
        @param uri: The URI of the media file. Must be unique.
        @type uri: string
        @param length: The total length of the media file (in s).
        @type length: int
        @param lastPlayed: The date the media file was last played.
        @type lastPlayed: string
        """
        self._uri = uri
        self._length = length
        self._lastPlayed = lastPlayed
        self._streamPosition = 0
        self._audioVolume = 100
        self._brightness = 0
        self._contrast = 0
        self._hue = 0
        self._saturation = 0
    
    
    def getURI(self):
        """
        """
        return self._uri
    
    
    def getLength(self):
        """
        """
        return self._length
    
    
    def getLastPlayed(self):
        """
        """
        return self._lastPlayed
    
    
    def getStreamPosition(self):
        """
        """
        return self._streamPosition
    
    
    def getAudioVolume(self):
        """
        """
        return self._audioVolume
    
    
    def getBrightness(self):
        """
        """
        return self._brightness
    
    
    def getHue(self):
        """
        """
        return self._hue
        
    
    def getContrast(self):
        """
        """
        return self._contrast
        
        
    def getSaturation(self):
        """
        """
        return self._saturation
        
    
    def setURI(self, uri):
        """
        """
        self._uri = uri
    
    
    def setLength(self, length):
        """
        """
        self._length = length
        
    
    def setLastPlayed(self, lastPlayed=None):
        """
        """
        if lastPlayed == None:
            self._lastPlayed = str(datetime.date.today())
        else:
            self._lastPlayed = lastPlayed
        
    
    def setStreamPosition(self, pos):
        """
        """
        self._streamPosition = pos
        
    
    def setAudioVolume(self, value):
        """
        """
        self._audioVolume = value
        
        
    def setBrightness(self, val):
        """
        """
        self._brightness = val
        
        
    def setContrast(self, val):
        """
        """
        self._contrast = val
        
        
    def setHue(self, val):
        """
        """
        self._hue = val
        
        
    def setSaturation(self, val):
        """
        """
        self._saturation = val
        
            
    def getFilename(self):
        """
        This method returns the filename for this media file.
        """
        return utils.getFilenameFromURI(self._uri)
    
    
    def getLengthSec(self):
        """
        """
        return utils.secToStr(self._length)
    
    
    def getVideoSettings(self):
        """
        """
        settings = []
        settings.append(self._brightness)
        settings.append(self._contrast)
        settings.append(self._hue)
        settings.append(self._saturation)
        
        return settings
    