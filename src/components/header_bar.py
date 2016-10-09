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
from gi.repository import Gtk
from components import file_chooser
from components import about_dialog


class HeaderBarComponent(Gtk.HeaderBar):
    def __init__(self, window):
        """
        Provides
        :param window: Main application window reference, serves as communication hub
        """
        super(Gtk.HeaderBar, self).__init__()
        self.set_show_close_button(True)
        # Set default window title
        self.props.title = "Easy eBook Viewer"
        self.__window = window
        self.__menu = Gtk.Menu()
        # Fill it with all the wigets
        self.__populate_headerbar()

    def __populate_headerbar(self):

        """
        Adds all default Header Bar content and connects handlers
        """

        # Adds open eBook button
        self.open_button = Gtk.Button()
        document_open_image = Gtk.Image.new_from_icon_name("document-open", Gtk.IconSize.LARGE_TOOLBAR)
        self.open_button.add(document_open_image)
        self.open_button.connect("clicked", self.__on_open_clicked)
        self.pack_start(self.open_button)

        # Adds linked Gtk.Box to host chapter navigation Entries
        self.pages_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(self.pages_box.get_style_context(), "linked")

        # Left current page Entry
        self.current_page_entry = Gtk.Entry()
        self.current_page_entry.set_text("0")
        self.current_page_entry.set_max_width_chars(3)
        self.current_page_entry.set_width_chars(3)
        self.current_page_entry.connect("activate", self.__on_activate_current_page_entry)
        self.pages_box.add(self.current_page_entry)

        # Right of all pages Entry
        self.number_pages_entry = Gtk.Entry()
        self.number_pages_entry.set_placeholder_text("of 0")
        self.number_pages_entry.set_editable(False)
        self.number_pages_entry.set_max_width_chars(5)
        self.number_pages_entry.set_width_chars(5)
        self.number_pages_entry.set_can_focus(False)
        self.pages_box.add(self.number_pages_entry)

        self.pack_start(self.pages_box)

        # Adds linked Gtk.Box to host chapter navigation buttons
        navigation_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(navigation_box.get_style_context(), "linked")

        # Adds left arrow chapter navigation button
        self.left_arrow_button = Gtk.Button()
        self.left_arrow_button.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
        self.left_arrow_button.set_sensitive(False);
        self.left_arrow_button.connect("clicked", self.__on_left_arrow_clicked)
        navigation_box.add(self.left_arrow_button)

        # Adds right arrow chapter navigation button
        self.right_arrow_button = Gtk.Button()
        self.right_arrow_button.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
        self.right_arrow_button.set_sensitive(False);
        self.right_arrow_button.connect("clicked", self.__on_right_arrow_clicked)
        navigation_box.add(self.right_arrow_button)

        self.pack_start(navigation_box)

        # Adds show chapters index toggle button
        self.show_index_button = Gtk.ToggleButton()
        index_icon = Gtk.Image.new_from_icon_name("view-list-symbolic", Gtk.IconSize.SMALL_TOOLBAR)
        self.show_index_button.add(index_icon)
        self.show_index_button.connect("clicked", self.__on_show_index_clicked)
        self.pack_start(self.show_index_button)

        # Adds About context settings menu item
        about_menu_item = Gtk.MenuItem("About")
        about_menu_item.connect("activate", self.__on_about_menu_item_clicked)
        self.__menu.append(about_menu_item)
        self.__menu.show_all()

        # Adds settings menu button
        self.properties_button = Gtk.Button()
        document_properties_image = Gtk.Image.new_from_icon_name("open-menu", Gtk.IconSize.LARGE_TOOLBAR)
        self.properties_button.add(document_properties_image)
        self.properties_button.connect("clicked", self.__on_properties_clicked)
        self.pack_end(self.properties_button)

    def __on_about_menu_item_clicked(self, widget):
        """
        Handles About context menu item clicked event, displays manu popup
        :param widget:
        """
        dialog = about_dialog.AboutDialog()
        dialog.show_dialog

    def __on_properties_clicked(self, button):
        """
        Handles settings button clicked event and displays context menu
        :param button:
        """
        self.__menu.popup(None, button, None, button, 0, Gtk.get_current_event_time())
        pass

    def __on_right_arrow_clicked(self, button):
        """
        Handles Right Arrow clicked navigation event, moves one chapter to the right
        :param button:
        """
        self.__window.load_chapter(self.__window.content_provider.current_chapter + 1)

    def __on_left_arrow_clicked(self, button):
        """
        Handles Left Arrow clicked navigation event, moves one chapter to the left
        :param button:
        """
        self.__window.load_chapter(self.__window.content_provider.current_chapter - 1)

    def __on_show_index_clicked(self, button):
        """
        Handles show chapters index toggle button clicked event, hides or displays chapters index list
        :param button:
        """
        self.__window.toggle_left_paned()

    def __on_open_clicked(self, button):
        """
        Handles Open Document button clicked, shows file selector, saves book data and loads new book
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

    def __on_activate_current_page_entry(self, wiget):
        """
        Handles enter key on current page entry and validates what user set and loads that chapter
        :param wiget:
        :param data:
        """
        try:
            if self.__window.content_provider.chapter_count >= int(wiget.get_text()) - 1 >= 0:
                self.__window.load_chapter(int(wiget.get_text()) - 1)
            else:
                self.current_page_entry.set_text(str(self.__window.content_provider.current_chapter + 1))
        except ValueError:
            self.current_page_entry.set_text(str(self.__window.content_provider.current_chapter + 1))

    def set_current_chapter(self, i):
        """
        Updates current chapter in entry if navigation came from somewhere else
        :param i:
        """
        self.current_page_entry.set_text(str(i))

    def set_maximum_chapter(self, i):
        """
        Sets text of "maximum" chapter entry ie. of X
        :param i:
        """
        self.number_pages_entry.set_placeholder_text("of " + str(i))

    def show_jumping_navigation(self):
        """
        Enables entry based navigation, to be used when book is loaded
        """
        self.pages_box.show()

    def hide_jumping_navigation(self):
        """
        Disables entry based navigation, to be used when no book is loaded
        """
        self.pages_box.hide()

    def enable_navigation(self):
        """
        Enables arrow based navigation, to use when book is loaded and in midsection
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
