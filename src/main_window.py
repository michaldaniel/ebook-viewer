#!/usr/bin/env python3

# eBook Viewer by Michal Daniel

# eBook Viewer is free software; you can redistribute it and/or modify it under the terms
# of the GNU General Public Licence as published by the Free Software Foundation.

# eBook Viewer is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public Licence for more details.

# You should have received a copy of the GNU General Public Licence along with
# eBook Viewer; if not, write to the Free Software Foundation, Inc., 51 Franklin Street,
# Fifth Floor, Boston, MA 02110-1301, USA.

import gi
from gi.repository import Gtk, Gdk

from components import header_bar, viewer
from workers import config_provider as config_provider_module, content_provider as content_provider_module

gi.require_version('Gtk', '3.0')


class MainWindow(Gtk.Window):

    def __init__(self):
        # Creates Gtk.Window and sets parameters
        Gtk.Window.__init__(self, title="eBook Viewer")
        self.set_border_width(0)
        self.set_default_size(800, 800)
        self.connect("destroy", self.__on_exit)
        # Gets application config from ConfigProvider
        try:
            self.config_provider = config_provider_module.ConfigProvider()
        except:
            # Could not save configuration file
            # TODO: Migrate to custom dialog designed in line with elementary OS Human Interface Guidelines
            error_dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK,
                                             "Could not write configuration file.")
            error_dialog.format_secondary_text("Make sure ~/.ebook-viewer is accessible and try again.")
            error_dialog.run()
            exit()

        # Gets application content from ContentProvider
        self.content_provider = content_provider_module.ContentProvider(self)

        # Creates and sets HeaderBarComponent that handles and populates Gtk.HeaderBar
        self.header_bar_component = header_bar.HeaderBarComponent(self)
        self.set_titlebar(self.header_bar_component.header_bar)

        # Prepares scollable window to host WebKit Viewer
        self.scrollable_window = Gtk.ScrolledWindow()
        self.scrollable_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.scrollable_window.get_vscrollbar().connect("show", self.__ajust_scroll_position)
        self.add(self.scrollable_window)

        # Adds WebKit viewer component from Viewer component
        self.viewer = viewer.Viewer(self)
        self.viewer.load_uri("about:blank")  # Display a blank page
        self.viewer.connect("key-press-event", self.__on_keypress_viewer)
        self.viewer.connect("load-finished", self.__ajust_scroll_position)
        self.scrollable_window.add(self.viewer)

        # Update WebView and light / dark GTK style theme according to settings
        self.__update_night_day_style()

        # No initial scroll offset
        self.scroll_to_set = 0.0

    @property
    def __scroll_position(self):
        """
        Returns position of scroll in Scrollable Window
        :return:
        """
        return self.scrollable_window.get_vadjustment().get_value()

    @property
    def __get_saved_scroll(self):
        """
        Returns saved scroll position obtained from config provider
        :return:
        """
        return float(self.config_provider.config[self.content_provider.book_md5]["position"])

    def save_current_book_data(self):
        """
        Saves to book config current chapter and scroll position
        """

        # Save only if book was loaded before
        if self.content_provider.status:
            self.config_provider.save_chapter_position(self.content_provider.book_md5,
                                                       self.content_provider.current_chapter,
                                                       self.__scroll_position)

    def load_book_data(self, filename):
        """
        Loads book to Viwer and moves to correct chapter and scroll position
        :param filename:
        """

        # Try to load book, returns true when book loaded without errors
        if self.content_provider.prepare_book(filename):
            # If book loaded without errors

            # Load chapter position
            self.__load_chapter_pos()

            # Enable navigation
            self.header_bar_component.enable_navigation()

            # Open book on viewer
            self.viewer.load_current_chapter()
            self.set_title(self.content_provider.book_name + " by " + self.content_provider.book_author)

            # Load scroll offset
            self.__load_scroll_pos()
        else:
            # If book could not be loaded display dialog
            # TODO: Migrate to custom dialog designed in line with elementary OS Human Interface Guidelines
            error_dialog = Gtk.MessageDialog(self.__window, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK,
                                             "Could not open the book.")
            error_dialog.format_secondary_text("Make sure you can read the file and the book you are trying to open is in supported format and try again.")
            error_dialog.run()
            error_dialog.destroy()

    def __load_chapter_pos(self):
        """
        Return chapter position obtained from config provider
        """
        self.content_provider.current_chapter = int(self.config_provider.config[self.content_provider.book_md5]["chapter"])

    def __load_scroll_pos(self):
        """
        Sets scroll offset to be loaded by Scrollable Window and WebView when they finish loading
        """
        self.scroll_to_set = self.__get_saved_scroll

    def __on_exit(self, window, data=None):
        """
        Handles application exit and saves all unsaved config data to file
        :param window:
        :param data:
        """
        self.save_current_book_data()

    def __ajust_scroll_position(self, widget, data):
        """
        Handles Scrollable Window and WebView loaded events and attempts to set scroll if scroll offset is loaded
        :param widget:
        :param data:
        """
        if self.scroll_to_set != 0.0:
            self.scrollable_window.get_vadjustment().set_value(self.scroll_to_set)
            if self.scrollable_window.get_vadjustment().get_value() != 0.0:
                self.scroll_to_set = 0.0

    def load_chapter(self, chapter):
        """
        Loads chapter and manages navigation UI accordingly
        :param chapter:
        """
        if self.content_provider.chapter_count >= chapter >= 0:
            self.content_provider.current_chapter = chapter
            self.viewer.load_current_chapter()
        if chapter >= self.content_provider.chapter_count:
            self.header_bar_component.disable_forward_navigation()
        elif chapter <= 0:
            self.header_bar_component.disable_backward_navigation()
        else:
            self.header_bar_component.enable_navigation()

    def __on_keypress_viewer(self, wiget, data):
        """
        Handles Left and Right arrow key presses
        :param wiget:
        :param data:
        """
        key_value = Gdk.keyval_name(data.keyval)
        if key_value == "Right":
            self.load_chapter(self.content_provider.current_chapter+1)
        elif key_value == "Left":
            self.load_chapter(self.content_provider.current_chapter-1)

    def __update_night_day_style(self):
        """
        Sets GTK theme and Viwer CSS according to application settings
        """
        settings = Gtk.Settings.get_default()
        if self.config_provider.config["Application"]["stylesheet"] == "Day":
            self.viewer.set_style_day()
            settings.set_property("gtk-application-prefer-dark-theme", False)
        else:
            self.viewer.set_style_night()
            settings.set_property("gtk-application-prefer-dark-theme", True)