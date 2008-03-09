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


class GoToDialog(Delegate):
    """
    """
    def __init__(self, parent):
        """
        Constructor.
        """
        # Create the dialogue
        windowName = 'GoToDialog'

        Delegate.__init__(self, gladefile=globals.gladeFile,
                          toplevel_name=windowName,  
                          delete_handler=self.quit_if_last)
        
        self.set_transient_for(parent)
        
        
    def on_bCancel__clicked(self, *args):
        """
        """
        self.hide_and_quit()
        
        
    def on_bOk__clicked(self, *args):
        """
        """
        self.hide_and_quit()
        #self.emit('result')