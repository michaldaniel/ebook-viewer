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
        self.window = window
        self.title = _("Properties")
        self.set_border_width(0)
        self.set_resizable(False)
        self.set_size_request(370, 500)
        self.header_bar_component = HeaderBarComponent(self)
        self.set_titlebar(self.header_bar_component)
        self.set_keep_above(True)
        self.__populate_preferences()
        self.show_all()

    def __populate_preferences(self):
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        hbox_theme = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        themes = ["Day (light)", "Night (dark)"]
        self.themes_combo = Gtk.ComboBoxText()
        self.themes_combo.set_entry_text_column(0)
        self.themes_combo.connect("changed", self.__on_themes_combo_changed)
        for theme in themes:
            self.themes_combo.append_text(theme)
        if self.window.config_provider.config["Application"]["stylesheet"] == "Day":
            self.themes_combo.set_active(0)
        else:
            self.themes_combo.set_active(1)
        hbox_theme.pack_end(self.themes_combo, False, True, 0)
        theme_label = Gtk.Label(_("Application theme") ,xalign=0)
        hbox_theme.pack_start(theme_label, False, True, 0)
        vbox.pack_start(hbox_theme, False, True, 0)
        try:
            vbox.set_margin_start(20)
            vbox.set_margin_end(20)
        except AttributeError:
            vbox.set_margin_left(20)
            vbox.set_margin_right(20)
        vbox.set_margin_top(20)
        self.add(vbox)


    def __on_themes_combo_changed(self, combo):
        text = combo.get_active_text()
        if text != None:
            print("Selected: theme=%s" % text)

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
        self.save_button = Gtk.Button.new_with_label("Save")
        self.save_button.connect("clicked", self.__on_save_button_clicked)
        self.save_button.get_style_context().add_class(Gtk.STYLE_CLASS_SUGGESTED_ACTION)
        self.pack_end(self.save_button)

         # Adds close preferences button
        self.close_button = Gtk.Button.new_with_label("Close")
        self.close_button.connect("clicked", self.__on_close_button_clicked)
        self.pack_end(self.close_button)

    def __on_save_button_clicked(self, wiget):
        if self.__window.window.config_provider.config["Application"]["stylesheet"] == "Day" and self.__window.themes_combo.get_active_text() == "Night (dark)":
            self.__window.window.config_provider.config["Application"]["stylesheet"] = "Night"
            self.__window.window.config_provider.save_configuration()
            self.__window.window.viewer.set_style_night()
            self.__window.window.settings.set_property("gtk-application-prefer-dark-theme", True)
            self.__window.window.show_all()
        elif self.__window.window.config_provider.config["Application"]["stylesheet"] == "Night" and self.__window.themes_combo.get_active_text() == "Day (light)":
            self.__window.window.config_provider.config["Application"]["stylesheet"] = "Day"
            self.__window.window.config_provider.save_configuration()
            self.__window.window.viewer.set_style_day()
            self.__window.window.settings.set_property("gtk-application-prefer-dark-theme", False)
            self.__window.window.show_all()
        self.__window.destroy()



    def __on_close_button_clicked(self, wiget):
        self.__window.destroy()