#!/usr/bin/env python3

# Easy eBook Viewer by Michal Daniel

# Easy eBook Viewer is free software; you can redistribute it and/or modify it under the terms
# of the GNU General Public Licence as published by the Free Software Foundation.

# Easy eBook Viewer is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public Licence for more details.

# You should have received a copy of the GNU General Public Licence along with
# Easy eBook Viewer; if not, write to the Free Software Foundation, Inc., 51 Franklin Street,
# Fifth Floor, Boston, MA 02110-1301, USA.

import gi

gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')
from gi.repository import WebKit2 as WebKit
from gi.repository import Gdk, Gtk

class Viewer(WebKit.WebView):
    def __init__(self, window):
        """
        Provides Webkit WebView element to display ebook content
        :param window: Main application window reference, serves as communication hub
        """
        self.__window = window

        self.manager = WebKit.UserContentManager.new()
        WebKit.WebView.__init__(self, user_content_manager=self.manager)

        color = self.__window.get_style_context().get_background_color(Gtk.StateType.NORMAL)
        self.set_background_color(color)

        # Sets WebView settings for ebook display
        # No java script etc.
        settings = self.get_settings()
        settings.props.enable_javascript = False
        settings.props.enable_plugins = False
        settings.props.enable_page_cache = False
        settings.props.enable_java = False
        settings.props.enable_html5_local_storage = False
        try:
            settings.props.enable_webgl = False
        except AttributeError:
            pass

        self.connect('context-menu', self.callback)

    def load_current_chapter(self):
        """
        Loads current chapter as pointed by content porvider
        """
        file_url = self.__window.content_provider.get_chapter_file(self.__window.content_provider.current_chapter)
        try:
            with open(file_url) as file_open:
                self.load_html(file_open.read(), "file://" + file_url)
                print("Loaded: " + file_url)
        except IOError:
            print("Could not read: ", file_url)

    def set_style_day(self):
        """
        Sets style to day CSS
        """
        _file = open("/usr/share/easy-ebook-viewer/css/day.css")
        css_str = _file.read()
        _file.close()
        style_sheet = WebKit.UserStyleSheet.new(css_str, WebKit.UserContentInjectedFrames.ALL_FRAMES,
                                                WebKit.UserStyleLevel.USER, None, None)
        self.manager.add_style_sheet(style_sheet)
        # TODO: Prefix location of day.css so it can be set during install

    def set_style_night(self):
        """
        Sets style to night CSS
        """
        _file = open("/usr/share/easy-ebook-viewer/css/night.css")
        css_str = _file.read()
        _file.close()
        style_sheet = WebKit.UserStyleSheet.new(css_str, WebKit.UserContentInjectedFrames.ALL_FRAMES,
                                                WebKit.UserStyleLevel.USER, None, None)
        self.manager.add_style_sheet(style_sheet)
        # TODO: Prefix location of night.css so it can be set during install

    def update_background(self):
        color = self.__window.get_style_context().get_background_color(Gtk.StateType.NORMAL)
        self.set_background_color(color)

    def callback(self, webview, context_menu, hit_result_event, event):
        self.__window.show_menu()
        return True
