# -*- coding: utf-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:

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

import pygst
pygst.require('0.10')
import gst

from src.services import log
from src.common import globals
from src.utils import utils


class Player:
    def __init__(self):
        """
        Constructor
        """
        self.aspectSettings = False
        self.colorSettings = False

        self.player = gst.element_factory_make("playbin", "player")

        self.logger = log.Logger()
    
        self.bus = self.getBus()
        self.bus.add_signal_watch()
        self.bus.enable_sync_message_emission()
        
    # Returns true if the player is playing, false if not.
    isPlaying = lambda self: self.getState() == gst.STATE_PLAYING

    # Returns true if the player is stopped, false if not.
    isStopped = lambda self: (self.getState() in [ gst.STATE_NULL, gst.STATE_READY ])
	
    # Returns true if the player is paused, false if not.
    isPaused = lambda self: self.getState() == gst.STATE_PAUSED
	
    # Returns the bus of the player
    getBus = lambda self: self.player.get_bus()
    
    # Returns the state of the player
    getState = lambda self: self.player.get_state()[1]
    
    # Returns the current URI
    getURI = lambda self: self.player.get_property('uri')
    
    # Returns an array of stream information
    getStreamsInfo = lambda self: self.player.get_property('stream-info-value-array')

    # Returns the times, played seconds and duration.
    getTimesSec = lambda self: (self.getPlayedSec(), self.getDurationSec())
    
    # Returns the played seconds.
    getPlayedSec = lambda self: utils.nsTos(self.getPlayed())
    
    # Returns the total duration seconds.
    getDurationSec = lambda self: utils.nsTos(self.getDuration())
    
    # Returns the played time (in nanoseconds).
    getPlayed = lambda self: self.player.query_position(gst.FORMAT_TIME)[0]


    def getDuration(self):
        # Returns the duration (nanoseconds).
        try:
            return self.player.query_duration(gst.FORMAT_TIME)[0]
        except:
            return 0


    def setVideoSink(self, sinkName):
        """
        This method sets the video sink for the player
        """
        self.logger.debug("Entered setVideoSink")

        sink = gst.element_factory_make(sinkName, 'video-sink') if sinkName else None
        self.player.set_property('video-sink', sink)

        # Flag the aspect and color settings accordingly
        self.aspectSettings = (sinkName in globals.vsinkAspect)
        self.colorSettings = (sinkName in globals.vsinkColour)
        
        
    def setAudioSink(self, sinkName):
        """
        This method sets the audio sink for the player
        """
        self.logger.debug("Entered setAudioSink")
        
        sink = gst.element_factory_make(sinkName, 'audio-sink') if sinkName else None
        self.player.set_property('audio-sink', sink)
 
 
    def prepareImgSink(self, bus, message, far, b, c, h, s):
        """
        This method sets the img sink. 
        
        bus -- 
        message -- 
        far -- 
        b -- 
        c -- 
        h -- 
        s -- 
        """
        self.imagesink = message.src

        self.setForceAspectRatio(far)
        self.setBrightness(b)
        self.setContrast(c)
        self.setHue(h)
        self.setSaturation(s)
        
        
    def setImgSink(self, widget):
        """
        This method sets the video output to the desired widget.
        """
        self.logger.debug("Entered setImgSink()")

        try:
            id = widget.window.xid
        except AttributeError:
            id = widget.window.handle # win32
        
        self.imagesink.set_xwindow_id(id)
        
        
    def seekFrac(self, pos):
        """
        This method seeks from a fraction.
        """
        dur = self.getDuration()
        
        if dur != 0:
            self.seek(int(dur * pos))
    
            
    def seek(self, loc):
        """
        This method seeks to a set location in the filestream.
        """
        # Seek to the requested position.
        self.player.seek(1.0, gst.FORMAT_TIME,
            gst.SEEK_FLAG_FLUSH | gst.SEEK_FLAG_ACCURATE,
            gst.SEEK_TYPE_SET, loc,
            gst.SEEK_TYPE_NONE, 0)    
        
        
    def playingVideo(self):
        """
        
        """
        return (self.player.get_property('current-video') != -1 or
                self.player.get_property('vis-plugin') != None)
        

    def play(self):
        """
        Starts the playback of the video
        """
        # Starts the player only if the player has a URI
        if self.getURI():
            self.player.set_state(gst.STATE_PLAYING)
            return True
       
        return False
           

    def togglePlayPause(self):
        """
        This method toggles play/pause.
        """
        if not self.getURI():
            # No file is opened, return an error
            return False
        
        if self.isPlaying():
            self.pause()
        else:
            self.play()

        return True    

        
    def stop(self):
        """
        Stops the playback of the video
        """
        self.player.set_state(gst.STATE_READY)
        

    def stopCompletely(self):
        """
        This method stops the player completely.
        """
        self.player.set_state(gst.STATE_NULL)
        
        
    def pause(self):
        """
        Pauses the playback of the video
        """
        self.player.set_state(gst.STATE_PAUSED)


    def setForceAspectRatio(self, val):
        """
        This method toggles force aspect ratio on or off.
        """
        if (self.aspectSettings):
			self.imagesink.set_property('force-aspect-ratio', val)
	
    
    def setAspectRatio(self, val):
        """
        This method sets the aspect ratio for the video.
        """
        pass
    
    def setBrightness(self, val):
        ## Sets the brightness of the video.
        if (self.colorSettings):
            self.imagesink.set_property('brightness', val)
	
    
    def setContrast(self, val):
        """
        This method sets the contrast of the video.
        """
        if (self.colorSettings):
	        self.imagesink.set_property('contrast', val)
	
    
    def setHue(self, val):
        """
        This method sets the hue of the video. 
        """
        if (self.colorSettings):
            self.imagesink.set_property('hue', val)
	
    
    def setSaturation(self, val):
        """
        This method sets the saturation of the video. 
        """
        if (self.colorSettings):
            self.imagesink.set_property('saturation', val)

       
    def setURI(self, uri):
        """
        This method sets the URI for the player
        """
        self.player.set_property('uri', uri)


    def setAudioTrack(self, track):
        """
        This method sets the audio track to the given track
        """
        self.player.set_property('current-audio', track)
    