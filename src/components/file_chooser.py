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
from os import path
from gi.repository import Gtk

gi.require_version('Gtk', '3.0')


class FileChooserWindow(Gtk.Window):

    @property
    def show_dialog(self):
        """
        Displays FileChooserDialog with ePub file filters and returns Gtk.ResponseType and filename string
        :return (response, filename):
        """
        dialog = Gtk.FileChooserDialog("Please choose a file", self, Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        dialog.set_current_folder(path.expanduser("~"))

        # Add filters so only .epub files show
        self.__add_filters(dialog)

        response = dialog.run()
        filename = dialog.get_filename()
        dialog.destroy()

        return response, filename

    def __add_filters(self, dialog):

        """
        Adds filters to indicate opening only .epub files.
        :param dialog:
        """
        filter_text = Gtk.FileFilter()
        filter_text.set_name("ePub files")
        filter_text.add_pattern("*.epub")
        dialog.add_filter(filter_text)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)


