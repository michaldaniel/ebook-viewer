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
from components import file_chooser
from components import about_dialog

class HeaderBarComponent:
    def __init__(self, window):
        self.header_bar = Gtk.HeaderBar()
        self.header_bar.set_show_close_button(True)
        self.header_bar.props.title = "Easy eBook Viewer"
        self.__window = window
        self.__menu = Gtk.Menu()

        self.__populate_headerbar()



    def __populate_headerbar(self):

        """
        Adds all default Header Bar content and connects handlers
        """

        # Adds open document button
        self.open_button = Gtk.Button()
        document_open_image = Gtk.Image.new_from_icon_name("document-open", Gtk.IconSize.LARGE_TOOLBAR)
        self.open_button.add(document_open_image)
        self.open_button.connect("clicked", self.__on_open_clicked)
        self.header_bar.pack_start(self.open_button)

        # Adds linked Gtk.Box to host chapter navigation buttons
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(box.get_style_context(), "linked")

        # Adds left arrow chapter navigation button
        self.left_arrow_button = Gtk.Button()
        self.left_arrow_button.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
        self.left_arrow_button.set_sensitive(False);
        self.left_arrow_button.connect("clicked", self.__on_left_arrow_clicked)
        box.add(self.left_arrow_button)

        # Adds right arrow chapter navigation button
        self.right_arrow_button = Gtk.Button()
        self.right_arrow_button.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
        self.right_arrow_button.set_sensitive(False);
        self.right_arrow_button.connect("clicked", self.__on_right_arrow_clicked)
        box.add(self.right_arrow_button)


        about_menu_item = Gtk.MenuItem("About")
        about_menu_item.connect("activate", self.__on_about_menu_item_clicked)
        self.__menu.append(about_menu_item)
        self.__menu.show_all()

        # Adds settings context menu button
        self.properties_button = Gtk.Button()
        document_properties_image = Gtk.Image.new_from_icon_name("document-properties", Gtk.IconSize.LARGE_TOOLBAR)
        self.properties_button.add(document_properties_image)
        self.properties_button.connect("clicked", self.__on_properties_clicked)
        self.header_bar.pack_end(self.properties_button)



        self.header_bar.pack_start(box)

    def __on_about_menu_item_clicked(self, widget):
        dialog = about_dialog.AboutDialog()
        dialog.show_dialog

    def __on_properties_clicked(self, button):
        self.__menu.popup(None, button, None, button, 0, Gtk.get_current_event_time())
        pass

    def __on_right_arrow_clicked(self, button):
        """
        Handles Right Arrow clicked navigation event
        :param button:
        """
        self.__window.load_chapter(self.__window.content_provider.current_chapter+1)

    def __on_left_arrow_clicked(self, button):
        """
        Handles Left Arrow clicked navigation event
        :param button:
        """
        self.__window.load_chapter(self.__window.content_provider.current_chapter-1)

    def __on_open_clicked(self, button):
        """
        Handles Open Document button clicked
        :param button:
        """

        # Loads file chooser component
        file_chooser_component = file_chooser.FileChooserWindow()
        (response, filename) = file_chooser_component.show_dialog

        # Check if Gtk.Response is OK, means user selected file
        if response == Gtk.ResponseType.OK:
            print("File selected: " + filename)  # Print selected file path to console

            # Save current book data
            self.__window.save_current_book_data()

            # Load new book
            self.__window.load_book_data(filename)

    def enable_navigation(self):
        """
        Enables all navigation, to use when book is loaded and in midsection
        """
        self.left_arrow_button.set_sensitive(True)
        self.right_arrow_button.set_sensitive(True)

    def disable_forward_navigation(self):
        """
        Disables navigation moving forward, to use when at the end of document
        """
        self.right_arrow_button.set_sensitive(False)

    def disable_backward_navigation(self):
        """
        Disables navigation moving backward, to use when at the beginning of document
        """
        self.left_arrow_button.set_sensitive(False)