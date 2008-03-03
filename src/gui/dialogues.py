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

import os

import pygtk
pygtk.require('2.0')
import gtk

from kiwi.ui.objectlist import ObjectList, Column
from kiwi.ui.views import BaseView, SlaveView
from kiwi.ui.gadgets import quit_if_last
from kiwi.ui.dialogs import error

from src.common import globals


class AboutDialog:
    """
    About dialog.
    """
    def __init__(self, parent):
        windowName = 'AboutDialog'
        self.xml = gtk.glade.XML(globals.gladeFile, windowName, globals.appName)
        
        self.dlg = self.xml.get_widget(windowName)

        self.dlg.set_transient_for(parent)
        self.dlg.set_name(globals.niceAppName)
        self.dlg.set_version(globals.version)
        self.dlg.set_comments("Simple video player based on Python, Gtk+ and Gstreamer.")
        self.dlg.set_logo(gtk.gdk.pixbuf_new_from_file_at_size(os.path.join(globals.imageDir, "morphin_icon.svg"), 300, 200))
        #self.dlg.set_license(gpl)
        self.dlg.set_authors(["Sebastian Ruml <sebastian.ruml@gmail.com>"])
        self.dlg.set_website("http://code.google.com/p/morphin/")

        # Show the dialog
        self.dlg.run()
        self.dlg.destroy()



class ErrMsgBox:
    """
    This class shows an error message box.
    """
    def __init__(self, msg1, msg2):
        """
        
        """
        error(msg1, msg2)       
        
