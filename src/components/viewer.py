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
from gi.repository import Gdk

class Viewer():
    def __init__(self, window):
        """
        Provides Webkit WebView element to display ebook content
        :param window: Main application window reference, serves as communication hub
        """
        self.manager = WebKit.UserContentManager.new()
        self.view = WebKit.WebView.new_with_user_content_manager(self.manager)

        # Allow transparency so we can use GTK theme as background
        # Can be overridden by CSS background property, needs to be rgba(0,0,0,0)
        color = Gdk.RGBA()
        color.parse("rgba(0,0,0,0)")
        self.view.set_background_color(color)

        # Sets WebView settings for ebook display
        # No java script etc.
        #self.set_full_content_zoom(True)
        settings = self.view.get_settings()
        settings.props.enable_javascript = False
        settings.props.enable_plugins = False
        settings.props.enable_page_cache = False
        settings.props.enable_java = False
        try:
            settings.props.enable_webgl = False
        except AttributeError:
            pass

        # Disable default menu: contains copy and reload options
        # Reload messes with custom styling, doesn't reload CSS
        # App is using own "copy" right click hack
        # It will allow in future to add more options on right click
        #settings.props.enable_default_context_menu = False
	
        settings.props.enable_html5_local_storage = False

        self.view.connect('context-menu', self.callback)

        self.__window = window

    def load_current_chapter(self):
        """
        Loads current chapter as pointed by content porvider
        """
        file_url = self.__window.content_provider.get_chapter_file(self.__window.content_provider.current_chapter)
        # Using WebView.load_html_string since WebView.load_uri files for some html files
        # while load_html_string works just fine
        # It's a bug that needs to be resolved upstream

        try:
            with open(file_url) as file_open:
                self.view.load_html(file_open.read(), "file://" + file_url)
                print("Loaded: " + file_url)
        except IOError:
            print("Could not read: ", file_url)

    def set_style_sheet(self, _int):
        """
        Sets style sheet
        """
        if _int == 1:
            _file = open("/usr/share/easy-ebook-viewer/css/night.css")
        else:
            _file = open("/usr/share/easy-ebook-viewer/css/day.css")
        css_str = _file.read()
        _file.close()
        style_sheet = WebKit.UserStyleSheet.new(css_str, WebKit.UserContentInjectedFrames.ALL_FRAMES, WebKit.UserStyleLevel.USER, None, None)
        self.manager.add_style_sheet(style_sheet)

    def callback(self, webview, context_menu, hit_result_event, event):
        self.__window.show_menu()
        return True

