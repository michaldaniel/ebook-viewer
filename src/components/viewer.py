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
from gi.repository import WebKit

gi.require_version('Gtk', '3.0')

class Viewer(WebKit.WebView): #Renders the book (webkit viewer)
    def __init__(self, window):
        WebKit.WebView.__init__(self)

        # Sets WebView settings for ebook display
        settings = self.get_settings()
        self.set_full_content_zoom(True)
        settings.props.enable_scripts = False
        settings.props.enable_plugins = False
        settings.props.enable_page_cache = False
        settings.props.enable_java_applet = False
        try:
            settings.props.enable_webgl = False
        except AttributeError:
            pass
        settings.props.enable_default_context_menu = False
        settings.props.enable_html5_local_storage = False
        self.__window = window

    def load_current_chapter(self):
        """
        Loads current chapter as pointed by content porvider
        """
        self.load_uri("file://"+self.__window.content_provider.get_chapter_file(self.__window.content_provider.current_chapter))

    def set_style_day(self):
        """
        Sets style to day CSS
        """
        settings = self.get_settings()
        settings.props.user_stylesheet_uri = "file://PREFIX/usr/share/ebook-viewer/css//day.css"

    def set_style_night(self):
        """
        Sets style to night CSS
        """
        settings = self.get_settings()
        settings.props.user_stylesheet_uri = "file://PREFIX/usr/share/ebook-viewer/css//night.css"