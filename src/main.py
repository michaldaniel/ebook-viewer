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
import gettext
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from main_window import MainWindow

# Let the fun begin...
if __name__ == "__main__":
    gettext.install('easy-ebook-viewer', '/usr/share/easy-ebook-viewer/locale')
    #lang = gettext.translation('easy-ebook-viewer', '/usr/share/easy-ebook-viewer/locale', languages=['pl'])
    #lang.install()
    win = MainWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    # If no book was loaded we need to tell it to hide navigation
    # TODO: Include chapters index list here
    if not win.book_loaded:
        win.header_bar_component.hide_jumping_navigation()
    Gtk.main()
