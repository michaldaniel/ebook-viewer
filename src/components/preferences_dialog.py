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
from gi.repository import Gtk, Gdk


class PreferencesDialog(Gtk.Window):
    def show_dialog(self, window):
        """
        Displays app preferences dialog
        """
        Gtk.Window.__init__(self)
        self.title = _("Properties")
        label = Gtk.Label("This is a dialog to display additional information")
        self.add(label)
        self.set_border_width(0)
        self.set_default_size(500, 600)
        self.header_bar_component = HeaderBarComponent(self)
        self.set_titlebar(self.header_bar_component)
        self.set_focus(self.header_bar_component.open_button)
        self.set_keep_above(True)
        self.show_all()

class HeaderBarComponent(Gtk.HeaderBar):
    def __init__(self, window):
        """
        Provides
        :param window: Main application window reference, serves as communication hub
        """
        super(Gtk.HeaderBar, self).__init__()
        self.set_show_close_button(False)
        self.set_has_subtitle(True)
        # Set default window title
        self.props.title = _("Preferences")
        self.__window = window
        self.__menu = Gtk.Menu()
        # Fill it with all the wigets
        self.__populate_headerbar()

    def __populate_headerbar(self):
         # Adds save preferences button
        self.open_button = Gtk.Button.new_with_label("Save")
        self.open_button.connect("clicked", self.__on_save_clicked)
        self.open_button.get_style_context().add_class(Gtk.STYLE_CLASS_SUGGESTED_ACTION)
        self.pack_end(self.open_button)

    def __on_save_clicked(self, wiget):
        self.__window.destroy()