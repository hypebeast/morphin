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

from src.utils import utils
from src.MediaManagement import MediaFile


class MediaManager:
    """
    This class handles all media files.
    """
    def __init__(self):
        """
        """
        self._mediaList = []
        
        self._activeMediaFile = None

        
    def getMediaList(self):
        """
        """
        return self._mediaList
    
    
    def AddMedia(self, uri):
        """
        """
        if not self.MediaExits(uri):
            mediaFile = MediaFile.MediaFile(uri)
            self._mediaList.append(mediaFile)
            
            #self._mediaList.append(str(uri))
            
            
    def AddMediaList(self, uris):
        """
        """
        for uri in uris:
            mediaFile = MediaFile.MediaFile(uri)
    
    
    def AddMediaFromURIList(self, uris, config):
        """
        This method builds the media list from the given list. The list contains
        one or more URIs.
        
        @param uris: List that holds one or more URIs
        @type uris: list
        """
        if len(uris) < 1:
            return
        
        for uri in uris:
            mediaFile = MediaFile.MediaFile(uri)
            
            # Get all options from the config file
            dur = config.get_option('duration', uri)
            if dur == None:
                dur = 0
            mediaFile.setLength(dur)
            
            lp = config.get_option('lastPlayed', uri)
            if lp == None:
                lp = ""
            mediaFile.setLastPlayed(lp)
            
            sp = config.get_option('streamPosition', uri)
            if sp == None:
                sp = 0
            mediaFile.setStreamPosition(sp)
            
            val = config.get_option('brightness', uri)
            if val == None:
                val = 0
            mediaFile.setBrightness(val)
            
            val = config.get_option('contrast', uri)
            if val == None:
                val = 0
            mediaFile.setContrast(val)
            
            val = config.get_option('hue', uri)
            if val == None:
                val = 0
            mediaFile.setHue(val)
            
            val = config.get_option('saturation', uri)
            if val == None:
                val = 0
            mediaFile.setSaturation(val)
            
            # Add the MediaFile object to the list.
            self._mediaList.append(mediaFile)
    
    
    def GetURIs(self):
        """
        This method returns all URIs.
        """
        uriList = []
        for mf in self._mediaList:
            uriList.append(mf.getURI())
            
        return uriList
    
    
    def GetActiveMediaFile(self):
        """
        This method return the currently playing media file.
        """
        pass
    
    
    def GetMediaFile(self, uri):
        """
        """
        for mf in self._mediaList:
            if mf.getURI() == uri:
                return mf
            
        return None
    
    
    def SaveMediaLengthToConf(self, uri, dur, config):
        """
        """
        #if not self.MediaExits(uri):
        # Save the media length to the appropriate config section
        self.WriteDurationToConf(config, uri, dur)
        
        
        
    def MediaExits(self, uri):
        """
        """
        for mf in self._mediaList:
            if mf.getURI() == uri:
                return True
            
        return False
    
    
    def RecentPlayedToConf(self):
        """
        """
        uris = ""
        
        for i in self._mediaList:
            uris = i + ', '
            
        return uris
    
    
    def WriteDurationToConf(self, config, uri, dur):
        """
        """
        config.set_option('duration', dur, uri)
        
        mf = self.GetMediaFile(uri)
        mf.setLength(dur)
        
        
    def SaveMediaPosition(self, config, uri, position):
        """
        """
        config.set_option('streamPosition', position, uri)
        
        # TODO: The saving of the position should be done at the closing of the
        # application.
        mf = self.GetMediaFile(uri)
        mf.setStreamPosition(position)
    
    
    def SaveLastPlayed(self, config, uri, lastPlayed):
        """
        """
        config.set_option('lastPlayed', lastPlayed, uri)
        
        mf = self.GetMediaFile(uri)
        mf.setLastPlayed(lastPlayed)
    
        
    def SaveVideoSettings(self, config, uri, settings):
        """
        This method saves all video settings.
        
        @param config: The config object.
        @param uri: The URI of the media file.
        @param settings: A list that contains all video settings (brightness,
        contrast, hue, saturation).
        """
        config.set_option('brightness', settings[0], uri)
        config.set_option('contrast', settings[1], uri)
        config.set_option('hue', settings[2], uri)
        config.set_option('saturation', settings[3], uri)
        
        mf = self.GetMediaFile(uri)
        mf.setBrightness(settings[0])
        mf.setContrast(settings[1])
        mf.setHue(settings[2])
        mf.setSaturation(settings[3])
        