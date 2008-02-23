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

import pygtk
pygtk.require('2.0')
import gtk

from src.common import globals

class SettingsDialog:
    """
    This class shows the settings dialogue. Moreover, it handles the
    management of the settings.
    """
    def __init__(self, parent):
        """
        Constructor
        """
        # Create the dialogue
        windowName = 'SettingsDialog'
        self.xml = gtk.glade.XML(globals.gladeFile, windowName, globals.appName)
        
        self.dlg = self.xml.get_widget(windowName)
        self.dlg.set_transient_for(parent)
        
        # Connect the signals
        dic = { "on_bClose_activate" : self.closeDialog }
        self.xml.signal_autoconnect(dic)

        # Show the dialog
        self.dlg.run()
        self.dlg.destroy()


    def closeDialog(self, widget, event=None):
        """
        This method closes the dialogue.
        
        widget -- 
        event -- 
        """
        self.dlg.destroy()


    def loadSettings(self):
        """
        
        """
        pass
        
    def saveSettings(self):
        """
        
        """
        pass
        
        
 
