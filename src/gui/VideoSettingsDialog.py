# -*- coding: utf-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:

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

import pygtk
pygtk.require('2.0')
import gtk

from kiwi.ui.gadgets import quit_if_last
from kiwi.controllers import BaseController
from kiwi.ui.delegates import Delegate, SlaveDelegate

from src.common import globals


class VideoSettingsDialog(Delegate):
    """
    This class shows the settings dialogue. Moreover, it handles the
    management of the settings.
    """
    widgets = ["bClose", "hsBrightness", "hsHue", "hsSaturation",
               "hsContrast"]
    
    def __init__(self, parent, player, mediaFile):
        """
        Constructor
        """
        # Create the dialogue
        windowName = 'VideoSettingsDialog'

        Delegate.__init__(self, gladefile=globals.gladeFile,
                          toplevel_name=windowName,  
                          delete_handler=self.quit_if_last)
        
        self.set_transient_for(parent)
        
        self._player = player
        
        self._mediaFile = mediaFile
        
        settings = self._mediaFile.getVideoSettings()
        
        # Set default values
        self.hsBrightness.set_value(settings[0])
        self.hsHue.set_value(settings[2])
        self.hsContrast.set_value(settings[1])
        self.hsSaturation.set_value(settings[3])
        

    def on_bClose__clicked(self, *args):
        self.emit('result', self._mediaFile)
        self.hide_and_quit()
        
        
    def on_bDefault__clicked(self, *args):
        self._player.setHue(0)
        self._mediaFile.setHue(0)
        self.hsHue.set_value(0)
        
        self._player.setContrast(0)
        self._mediaFile.setContrast(0)
        self.hsContrast.set_value(0)
        
        self._player.setBrightness(0)
        self._mediaFile.setBrightness(0)
        self.hsBrightness.set_value(0)
        
        self._player.setSaturation(0)
        self._mediaFile.setSaturation(0)
        self.hsSaturation.set_value(0)
        
        
    def on_hsHue__value_changed(self, *args):
        """
        """
        val = self.hsHue.get_value()
        self._player.setHue(val)
        
        self._mediaFile.setHue(val)


    def on_hsContrast__value_changed(self, *args):
        """
        """
        val = self.hsContrast.get_value()
        self._player.setContrast(val)
        
        self._mediaFile.setContrast(val)
    
    
    def on_hsSaturation__value_changed(self, *args):
        """
        """
        val = self.hsSaturation.get_value()
        self._player.setSaturation(val)
        
        self._mediaFile.setSaturation(val)


    def on_hsBrightness__value_changed(self, *args):
        """
        """
        val = self.hsBrightness.get_value()
        self._player.setBrightness(val)
        
        self._mediaFile.setBrightness(val)
