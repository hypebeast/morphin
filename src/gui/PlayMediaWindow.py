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

import os
import pygtk
pygtk.require('2.0')
import gtk

from kiwi.ui.objectlist import ObjectList, Column
from kiwi.ui.views import BaseView, SlaveView
from kiwi.ui.gadgets import quit_if_last
from kiwi.controllers import BaseController
from kiwi.ui.delegates import Delegate, SlaveDelegate

from src.common import globals
from src.utils import utils


class MediaFile:
    """
    This class describes a media file for the listview entry..
    """
    def __init__(self, name, length='0:00', uri=""):
        """
        Constructor        
        
        name -- The name of the media file.
        length -- The length of the media file.
        """
        self.name = name
        self.length = length
        self.uri = uri
        self.lastPlayed = ""


media_list_columns = [Column('name', 'Name', data_type=str),
                      Column('length', 'Length', data_type=str),
                      Column('lastPlayed', 'Last Played', data_type=str, sorted=True, order=gtk.SORT_DESCENDING)]


class PlayMediaWindow(Delegate):
    widgets = ["imgAddMediaFile"]

    def __init__(self, parent, recentPlayed=None):
        windowName = "PlayMediaWindow"

        Delegate.__init__(self, gladefile=globals.gladeFile,
                          toplevel_name=windowName,  
                          delete_handler=self.quit_if_last)

        # Create the delegate and set it up
        self.buildObjectList(recentPlayed)
        self.mediaList.grab_focus()
        slave = SlaveDelegate(toplevel=self.mediaList)

        self.attach_slave("labelX", slave)
        slave.focus_toplevel() # Must be done after attach

        self.slave = slave

        self.set_transient_for(parent)

        # Set the image
        image = self.get_widget("imgAddMediaFile")
        image.set_from_file(os.path.join(globals.imageDir, "movie_track_add.png"))


    def buildObjectList(self, mediaList):
        """
        This method builds and initialize the ObjectList.
        """
        self.mediaList = ObjectList(media_list_columns)
        self.mediaList.connect('selection_changed', self.media_selected)
        self.mediaList.connect('double-click', self.double_click)

        for media in mediaList:
            mf = MediaFile(media.getFilename(), uri=media.getURI(), length=media.getLengthSec())
            mf.lastPlayed = media.getLastPlayed()
            self.mediaList.append(mf)
            
        # FIXME: Remove it. Only for testing
        #for i in [('test1.wmv', "2.34"),
         #         ('test2.wmv', "2.59"),
          #        ('test3.wmv', "2.59"),
          #        ('test4.wmv', "2.59")]:
          #  self.mediaList.append(MediaFile(i[0], i[1]))


    def media_selected(self, the_list, item):
        pass


    def double_click(self, the_list, selected_object):
        self.emit('result', selected_object.uri)
        self.hide_and_quit()


    def on_bCancel__clicked(self, *args):
        self.hide_and_quit()


    def on_bQuit__clicked(self, *args):
        self.emit('result', 'quit')
        self.hide_and_quit()


    def on_bPlayMedia__clicked(self, *args):
        # TODO: Add open file dialog and start playing the selected
        # file.
        # Open the file chooser dialog

        dialog = gtk.FileChooserDialog("Open Media...",
                                        None,
                                        gtk.FILE_CHOOSER_ACTION_OPEN,
                                        (gtk.STOCK_CANCEL,
                                         gtk.RESPONSE_CANCEL,
                                         gtk.STOCK_OPEN,
                                         gtk.RESPONSE_OK))

        dialog.set_default_response(gtk.RESPONSE_OK)

        filter = gtk.FileFilter()
        filter.set_name("Media files")
        for pattern in globals.compatibleFiles:
            filter.add_mime_type(pattern)
        dialog.add_filter(filter)    
    
        filter = gtk.FileFilter()
        filter.set_name("All files")
        filter.add_pattern("*")
        dialog.add_filter(filter)


        response = dialog.run()
        if response == gtk.RESPONSE_OK:
            self.emit('result', dialog.get_filename())
            self.hide_and_quit()
        elif response == gtk.RESPONSE_CANCEL:
            pass

        dialog.destroy()


    def on_bPlayDisk__clicked(self, *args):
        """
        """
        pass
    
    
    def onKeyPressEvent(self, widget=None, event=None):
        """
        """
        pass
    

