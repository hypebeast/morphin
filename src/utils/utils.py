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

import sys
import re
from urlparse import urlparse, urlsplit


# Converts nanoseconds to seconds.
nsTos = lambda ns: float(ns) / 1000000000
# Seconds to miliseconds.
sToms = lambda s: 1000 * s


def secToStr(s):
    """
    This method converts the given seconds (int) to a human readable
    format (H:M:S).
    """
    # Converts seconds into a string of H:M:S
    h = s / 3600
    m = (s % 3600) / 60
    s = s % 60
    # Only print hours if it doesn't equal 0.
    if (h != 0):
       return '%d:%02d:%02d' % (h, m, s)
    else:
        return '%d:%02d' % (m, s)
    
    
def getFilenameFromURI(uri):
    """
    This method extracts the filename from the given URI. 
    """
    o = urlsplit(uri)
    
    pattern = '^(.*)/(.*)$'

    prog = re.compile(pattern)
    result = prog.search(o.path)
        
    if result:
        return result.group(2)
    
    
def buildStatusBarStr(tot, pld):
    """
    This method builds a nice looking string for the status bar.
    
    tot -- Total length
    pld -- Played time
    """
    str = secToStr(pld) + " / " + secToStr(tot)
    
    return str
