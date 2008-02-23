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

import os, sys, signal

import gobject
import gtk, gtk.glade

from src.common import globals
from src.gui import dialogues, SettingsDialog, PlayMediaWindow
from src.gstreamer import gstPlayer as player
from src.gstreamer import tools as gstTools
from src.services import log 
from src.utils import utils
from src.services import config


class MorphinWindow(gobject.GObject): 
    """
        The main interface class. Everything starts from here.
    """
    __single = None

    def __init__(self, options, args):
        windowName = "MainWindow"
        self.options = options

        self.currentFile = ""

        # Logger
        self._logger = log.Logger()
        
        # Gstreamer video player
        self._player = player.Player()
        
        # Configuration
        self._config = config.Config(globals.cfgFile, globals.DEFAULT_CONFIG)
        
        # The xml glade file object
        self.xml = gtk.glade.XML(globals.gladeFile, windowName, globals.appName)
        
        # Connect all signals
        signals = { "on_MainWindow_destroy" : self.quit,
                    "on_mnuiQuit_activate" : self.quit,
                    "on_mnuiOpen_activate" : self.showOpenMedia,
                    "on_mnuiAbout_activate" : self.showAboutDlg,
                    "on_mnuiPlay_activate" : self.mnuiPlayClicked,
                    "on_mnuiStop_activate" : self.mnuiStopClicked,
                    "on_mnuiSettings_activate" : self.showSettingsDlg,
                    "on_videoDrawingArea_expose_event" : self.videoWindowExpose,
                    "on_videoDrawingArea_configure_event" : self.videoWindowConfigure,
                    "on_videoDrawingArea_motion_notify_event" : self.videoWindowMotion,
                    "on_videoDrawingArea_leave_notify_event" : self.videoWindowLeave,
                    "on_videoDrawingArea_enter_notify_event" : self.videoWindowEnter,
                    "on_MainWindow_key_press_event" : self.mainWindowKeyPressed,
                    "on_bTogglePlay_clicked" : self.playPauseToggle,
                    "on_btnPlay_clicked" : self.playFile,
                    "on_hScaleProgress_button_press_event" : self.progressClicked,
                    "on_hScaleProgress_button_release_event" : self.progressSeekEnd,
                    "on_hScaleProgress_value_changed" : self.progressValueChanged,
                    "on_MainWindow_window_state_event" : self.onMainStateEvent,
                    "on_videoDrawingArea_key_press_event" : self.videoWindowClicked }
        self.xml.signal_autoconnect(signals)

        # Get all needed widgets
        self.window = self.xml.get_widget(windowName)
        self.videoWindow = self.xml.get_widget('videoDrawingArea')
        self.progressScale = self.xml.get_widget('hScaleProgress')
        self.statusBar = self.xml.get_widget('statusbar')
        
        # This member holds the context_id for the statusbar
        self.contextIdTime = self.statusBar.get_context_id("time")
        self.contextIdTitle = self.statusBar.get_context_id("title")
        
        # Set the icon
        image = os.path.join(globals.imageDir, 'morphin_icon.png')
        bgPixbuf = gtk.gdk.pixbuf_new_from_file_at_size(image, 32, 32)
        self.window.set_icon(bgPixbuf)
        
        # Some status variables
        
        # Defines if we are seeking
        self.seeking = False
        
        # This member indicates if the controls are show or not
        self.controlsShown = True
        
        # Creates and prepares the player
        self.preparePlayer()

        # Connect to the sigterm signal
        signal.signal(signal.SIGTERM, self.sigterm)
    
        # TODO: Add singleton check here
        #self.__single = self

        # Show the main window
        self.window.show()

        # Load the configuration
        self.loadConfig()
        
        #
        # Setting various states
        #

        # Set the play/pause toggle button
        self.playPauseChanged(False)

        # Sets the video window for the state stop
        self.videoWindowOnStop()

        # Update the progress
        self.progressUpdate()

        # Play a video, if it was given on the command line
        if len(args) > 0:
            # TODO: Add handling for more than one file (implement a
            # queue for handling the media files)
            self.currentFile = args[0]
            self.playFile(self.currentFile)
        else:
            self.showOpenMedia()

        # Check for fullscreen
        if options.fullscreen:
            self.activateFullscreen()


    # Checks if we should allow fullscreen functions (It's 1 when is's
    # hidden)
    videoWindowShown = lambda self: self.videoWindow.get_size_request() > (1, 1)

    # Stop the player
    stopPlayer = lambda self, widget: self._player.stop()
        

    def loadConfig(self):
        """
        This method loads all configuration settings.
        """
        pass
    
    def saveConfig(self):
        """
        This method saves all config options.
        """
        self._config.write()
        
    
    def quit(self, widget=None, event=None):
        # Shut down the GST
        self._player.stopCompletely()
        
        # Save all settings
        self.saveConfig()
        
        # Quit the app
        gtk.main_quit()

            
    def showOpenMedia(self, widget=None, event=None):
        """
        This method shows the PlayMedia dialog.
        """
        dlg = PlayMediaWindow.PlayMediaWindow(self.window)
        dlg.show_all()
        dlg.connect('result', self.get_media_url)


    def showAboutDlg(self, widget=None, event=None):
        """
        This method shows the about dialog.
        """
        dialogues.AboutDialog(self.window) 


    def mnuiPlayClicked(self, widget=None, event=None):
        """
        This method is called when the user clicks the play/pause menu item.
        """
        self.playPauseToggle(widget, event)


    def mnuiStopClicked(self, widget=None, event=None):
        """
        
        """
        self._player.stop()


    def showSettingsDlg(self,widget=None, event=None):
        """
        
        """
        SettingsDialog.SettingsDialog(self.window)
        

    def preparePlayer(self):
        """
        This method prepares the player
        """
        bus = self._player.getBus()
        bus.connect('message', self.onPlayerMessage)
        bus.connect('sync-message::element', self.onPlayerSyncMessage)
        
        self._logger.debug("Entered preparePlayer()")

        # Set audio and video sink
        self._player.setAudioSink(None)
        self._player.setVideoSink(gstTools.vsinkDef())
       

    def onPlayerMessage(self, bus, message):
        """
        
        """
        self._logger.debug("Entered onPlayerMessage()") 

        t = gstTools.messageType(message)
        if t == 'eos':
            # At the end of a stream, play next item from queue.
            #self.playNext()
            # TODO: Handle the end of a video file
            self._player.stop() 
        elif t == 'error':
			# On an error, empty the currently playing file (also stops it).
			self.playFile(None)
			# Show an error about the failure.
			msg = message.parse_error()
			dialogues.ErrorMsgBox("Error", str(msg[0]) + '\n\n' + str(msg[1]))
        elif t == 'state_changed' and message.src == self._player.player:
		    self.onPlayerStateChange(message)
        #elif t == 'tag':
         #   self.setPlayingTitle(True)

        
    def onPlayerSyncMessage(self, bus, message):
        """
        
        """
        self._logger.debug("Entered onPlayerSyncMessage") 
        
        if message.structure is None:
            return

        if message.structure.get_name() == 'prepare-xwindow-id':
            self.showVideoWindow()

            h = 0
            b = 0
            c = 0
            s = 0
            far = True
            self._player.prepareImgSink(bus, message, far, b, c, h, s)

            self.setImageSink()


    def onPlayerStateChange(self, message):
        """
        This method is called on a state change of the player
        (message: state_changed).

        message -- 
        """
        msg = message.parse_state_changed()
        if (gstTools.isNull2ReadyMsg(msg)):
			# Enable the visualisation if requested.
			#if (cfg.getBool('gui/enablevisualisation')):
			#	player.enableVisualisation()
			#else:
			#	player.disableVisualisation()
            pass
        elif (gstTools.isStop2PauseMsg(msg)):
			# The player has gone from stopped to paused.
			# Get the array of audio tracks.
			#self.audioTracks = gstTools.getAudioLangArray(player)
			# Only enable the audio track menu item if there's more than one audio track.
			#self.wTree.get_widget('mnuiAudioTrack').set_sensitive(len(self.audioTracks) > 1)
			# Enable the visualisation if requested.
			#if (cfg.getBool('gui/enablevisualisation')):
			#	player.enableVisualisation()
			#else:
		#		player.disableVisualisation()
			# Set the title accordingly.
			self.setPlayingTitle(True)
        elif (gstTools.isPlayMsg(msg)):
			# The player has just started.
			# Set the play/pause image to pause.
            self.playPauseChanged(True)
			
            # Create the timers.
            self.createPlayTimers()
            
            # Set up the progress scale
            self.setProgressRange()

            # Set the title
            self.setPlayingTitle(True)
        elif (gstTools.isPlay2PauseMsg(msg)):
            # It's just been paused or stopped.
            self.playPauseChanged(False)
            
            # Destroy the play timers.
            self.destroyPlayTimers()
            
            # Update the progress bar.
            self.progressUpdate()
        elif (gstTools.isStopMsg(msg)):
			#if ((not player.isPlaying()) and self.wTree.get_widget("mnuiQuitOnStop").get_active()): self.quit()
			# Draw the background image.
            self.videoWindowOnStop()
			
            # Deactivate fullscreen.
            if (self.fsActive()):
                self.deactivateFullscreen()
			
            # Reset the progress bar.
            self.progressUpdate()
			
            # Clear the title.
            self.setPlayingTitle(False)
            pass


    def videoWindowExpose(self, widget, event):
        """
        This method is called when the expose event is fired
        """
        # Pull the dimensions
        x, y, w, h = event.area

        # Let the whole thing drawn upon
        color = widget.get_style().black_gc if self.videoWindowShown() else widget.get_style().bg_gc[0]
        widget.window.draw_drawable(color, self.pixmap, x, y, x, y, w, h) 

        # If we we are not playing, configure the player accordingly
        if self.videoWindowShown():
            self.videoWindowOnStop()


    def videoWindowConfigure(self, widget, event=None):
        """
        This method configures the video window
        
        widget -- 
        event -- 
        """
        # Get the windows allocation
        x, y, w, h = widget.get_allocation()

        self.pixmap = gtk.gdk.Pixmap(widget.window, w, h)

        # Fill the hole thing with black
        color = widget.get_style().black_gc if self.videoWindowShown() else widget.get_style().bg_gc[0]
        self.pixmap.draw_rectangle(color, True, 0, 0, w, h)

        # Queue the drawing area
        widget.queue_draw()


    def onMainStateEvent(self, widget=None, event=None):
        """This method is called when a state event occurs on the main
        window. It's used for handling the changes between fullscreen
        and normal state."""
        fs = event.new_window_state & gtk.gdk.WINDOW_STATE_FULLSCREEN
        if fs:
            # Hide all the widgets other than the video window.
            for item in globals.hiddenFSWidgets:
                self.xml.get_widget(item).hide()
                
            self.controlsShown = False
        else:
			# Re-show all the widgets that aren't meant to be hidden.
            for item in globals.hiddenFSWidgets:
                self.xml.get_widget(item).show()
                
            self.controlsShown = True


    def setImageSink(self, widget=None):
        """
        This method sets the image sink to 'widget' or the default
        one, if none passed.
        """
        self._logger.debug("setImageSink called") 
        
        # If no widget is given, set it to the default
        if not widget:
            widget = self.videoWindow

        self.videoWindowConfigure(widget)
        
        # Set the image sink
        self._player.setImgSink(widget)

        return False


    def playPauseToggle(self, widget=None, event=None):
        """
        This method toggles the player play/pause.
        """
        if not self._player.getURI():
            # If there is no currently playing track open the PlayMedia window.
            PlayMediaWindow.PlayMediaWindow(self.window)
        elif self._player.isPlaying():
            self._player.pause()
        else:
            self._player.play()
             

    def videoWindowOnStop(self):
        """
        This method is called when the player stops
        """
        if self._player.playingVideo():
            return

        self.showVideoWindow()
        self.drawVideoWindowImage()
        

    def showVideoWindow(self):
        """
        This method shows the video window.
        """
        self.videoWindow.set_size_request(480, 320)


    def hideVideoWindow(self, force=False):
        """This method hides the video window."""
        if not self.fsActive() or force:
            # Hide the video window
            self.videoWindow.set_size_request(1, 1)
            # Make the hight of the window as small as possible
            w = self.window().get_size()[0]
            self.window.resize(w, 1)


    def drawVideoWindowImage(self):
        """
        This method draws the background image for the video image.
        """
        ## Draws the background image.
        if (sys.platform == 'win32'):
            return

        # Get the width & height of the videoWindow.
        alloc = self.videoWindow.get_allocation()
        w = alloc.width
        h = alloc.height
        if (w < h):
            # It's wider than it is high, use the width as the size
            # & find where the image should start.
            size = w
            x1 = 0
            y1 = (h - w) / 2
        else:
            # Do the opposite.
            size = h
            x1 = (w - h) / 2
            y1 = 0
		
        # Get the image's path, chuck it into a pixbuf, then draw it!
        image = os.path.join(globals.imageDir, 'morphin_icon.svg')
        bgPixbuf = gtk.gdk.pixbuf_new_from_file_at_size(image, size, size)
        self.videoWindow.window.draw_pixbuf(self.videoWindow.get_style().black_gc,bgPixbuf.scale_simple(size, size, gtk.gdk.INTERP_NEAREST), 0, 0, x1, y1)


    def activateFullscreen(self):
        """
        This method activates the fullscreen mode of the player.
        """
        if not self.videoWindowShown():
            return

        self.window.fullscreen()


    def deactivateFullscreen(self):
        """
        This method deactivates the fullscreen.
        """
        # TODO: Hide all widgtes, before we unfullscreen

        gobject.idle_add(self.window.unfullscreen)

    
    def toggleFullscreen(self):
        if self.fsActive():
            self.deactivateFullscreen()
        else:
            self.activateFullscreen()


    def fsActive(self):
        """
        This method returns true if fullscreen is active, otherwise false.
        """
        return self.window.window.get_state() & gtk.gdk.WINDOW_STATE_FULLSCREEN


    def playFile(self, filename):
        """
        This method plays the given file. The filename could also be
        a URI.
        """
        self._player.stop()

        self._player.setAudioTrack(0)
        
        # If no file is to be played, set the URI to None, and the
        # file too.
        if filename == None:
            filename = ""
            self._player.setURI(filename)

        if '://' not in filename:
            filename = os.path.abspath(filename)
 
        if os.path.exists(filename) or '://' in filename:
            # If it's not already a URI, make it one
            if '://' not in filename:
                filename = 'file://' + filename

            self._player.setURI(filename)

            self._player.play()
        elif filename != "":
            print "Something strange happens, no such file: %s" % filename
            self.playFile(None)


    def playNextMedia(self):
        """
        This method plays the next media in the queue.
        """
        pass


    def createPlayTimers(self):
        """
        This method creates the play timers.
        """
        # Destroy all old timers
        self.destroyPlayTimers()

        # Create the timers
        self.timSec = gobject.timeout_add_seconds(1, self.secondTimer)


    def destroyPlayTimers(self):
        """
        This method destroys all play timers.
        """
        try:
            gobject.source_remove(self.timSec)
        except:
            pass


    def secondTimer(self):
        """
        This method is called when the gui-update timer ist called.
        """
        if not self.seeking:
            self.progressUpdate()

        return self._player.isPlaying()


    def playPauseChanged(self, playing):
        """This method changes the toggle button for playing/pause the
        video according to the argument."""
        # Set the icon accordingly to the argument 
        img = gtk.image_new_from_stock('gtk-media-play' if (not playing) else 'gtk-media-pause', 1)

        btn = self.xml.get_widget("bTogglePlay")
        btn.set_image(img)
        # Set the text accordingly to the argument
        btn.set_label('Play' if not playing else 'Pause')

        # TODO: Change menu item, too
        mui = self.xml.get_widget("mnuiPlay")
        #mui.set_label('Play' if not playing else 'Pause')

    
    def mainWindowKeyPressed(self, widget, event):
        """
        This method is responsible for handling the key events on the
        main window.

        widget -- 
        event -- 
        """
        if event.string == ' ':
            # Toggle play/pause
            #self.playPauseToggle()
            pass
        elif event.string == 'f':
            # Toggle fullscreen
            self.toggleFullscreen()
        elif event.string == 's':
            # Stop playing
            self._player.stop()


    def videoWindowClicked(self, widget, event):
        """
        This method is called when the user clicks on the video
        window.
        """
        # Get all information
        x, y, state = event.window.get_pointer()

        if event.type == gtk.gdk._2BUTTON_PRESS and state & gtk.gdk.BUTTON1_MASK:
            # Video window was double clicked, toggle fullscreen
            self.toggleFullscreen()
        elif event.type == gtk.gdk.BUTTON_PRESS and state & gtk.gdk.BUTTON2_MASK:
            # On a middle click, toggle play/pause
            self.togglePlayPause()


    def videoWindowMotion(self, widget, event):
        """
        This method is called when the motion event is fired
        """
        pass


    def videoWindowEnter(self, widget, event):
        """
        This method is called when the video window is entered
        """
        pass


    def videoWindowLeave(self, widget, event):
        """
        This method ist called when the video window is leaved
        """
        pass


    def setPlayingTitle(self, show):
        """This method sets the title of the window and the status bar to the
        current playing URI."""
        if show:
            title = globals.niceAppName + ' - ' + utils.getFilenameFromURI(self._player.getURI())
        else:
            title = globals.niceAppName
        
        self.window.set_title(title)
        #self.statusBar.push(self.contextIdTitle, utils.getFilenameFromURI(self.player.getURI()))


    def setProgressRange(self):
        """
        This method sets the range of the scale widget in dependece to the media
        length.
        """
        if self._player.isStopped():
            pass
        else:
            pld, tot = self._player.getTimesSec()
            
            # Convert to int
            p, t = int(pld), int(tot)
            
            # Set the range
            self.progressScale.set_range(0, t if t > 0 else 0)
            
            # Status bar
            id = self.statusBar.push(self.contextIdTime, utils.buildStatusBarStr(t, p))
    
    
    def progressUpdate(self, pld=None, tot=None):
        """
        This method updates the progress bar.
        
        pld -- Time played (in s)
        tot -- Totall length (ins s)
        """
        if self._player.isStopped():
            # Player is stopped
            pld = 0
            tot = 0
            #self.progressScale.set_range(0, tot)
        else:    
            # Otherwise (playing or paused), get the track time data and set the
            # progress scale fraction.
            if pld == None or tot == None:
                pld, tot = self._player.getTimesSec()

            # Convert to int
            p, t = int(pld), int(tot)

            self.progressScale.set_value(p)
            
            # Update the status bar
            id = self.statusBar.push(self.contextIdTime, utils.buildStatusBarStr(t, p))


    def progressClicked(self, widget=None, event=None):
        """
        This method is called when the user clicks on the progress scale.
        """
        self._logger.debug("Scale clicked")
        
        x, y, state = event.window.get_pointer()
        if state & gtk.gdk.BUTTON1_MASK and not self._player.isStopped() and self._player.getDuration():
            # If the user presses Button 1 and player is not stopped and the duration
            # exists: start seeking.
            self.seeking = True
            self.progressValueChanged(widget, event)
        else:
            # Otherwise do what would happen when the video window was clicked
            self.videoWindowClicked(widget, event)


    def progressSeekEnd(self, widget=None, event=None):
        """
        This method is called when seeking has ended (user releases the button).
        then it seeks to that position.
        """
        if self.seeking:
            self.seekFromProgress(widget, event)
            self.seeking = False
        
            
    def seekFromProgress(self, widget, event):
        """
        This method seeks to the given position in the stream.
        """
        x, y, state = event.window.get_pointer()
        
        # Get the value from the scale
        val = self.progressScale.get_value()
        
        self._logger.debug("Scale val: " + str(val))
        
        if val > 0:
            self._player.seekFrac(val)
        
        # Update the progress scale
        self.progressUpdate()


    def progressValueChanged(self, widget=None, event=None):
        """
        This method is called when the user moves the progress scale.
        """
        # If we are not seeking, return.
        if not self.seeking:
            return

    
    def get_media_url(self, view, result):
        self.playFile(result)


    def quit_app(self, view, result):
        self.quit()


    def sigterm(self, num, frame):
        """
        Quit when the sigterm signal caught.
        """
        self.quit()
        