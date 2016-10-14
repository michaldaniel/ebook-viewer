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
import os
import constants
import gi

gi.require_version('Gtk', '3.0')
from os import path
from gi.repository import Gtk


class FileChooserWindow(Gtk.Window):
    def show_dialog(self, importing=False):
        """
        Displays FileChooserDialog with ePub file filters and returns Gtk.ResponseType and filename string
        :return (response, filename):
        """
        dialog = Gtk.FileChooserDialog(_("Please choose a file"), self, Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        # Always start in user dir
        dialog.set_current_folder(path.expanduser("~"))

        # Add filters so only .epub files show
        # TODO: Filter list for all conversion supported ebooks
        self.__add_filters(dialog, importing)

        response = dialog.run()
        filename = dialog.get_filename()
        dialog.destroy()

        return response, filename

    def __add_filters(self, dialog, importing):
        """
        Adds filters to indicate opening only .epub files.
        :param dialog:
        """
        if not importing:
            self.__add_native(dialog)
            if os.path.exists("/usr/bin/ebook-convert"):
                self.__add_imports(dialog)
        else:
            self.__add_imports(dialog)

        filter_any = Gtk.FileFilter()
        filter_any.set_name(_("Any files"))
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)

    def __add_native(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name(_("ePub files"))
        for extension in constants.NATIVE:
            filter_text.add_pattern("*" + extension.upper())
            filter_text.add_pattern("*" + extension.lower())
        dialog.add_filter(filter_text)

    def __add_imports(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name(_("Importable files"))
        for extension in constants.IMPORTABLES:
            filter_text.add_pattern("*" + extension.upper())
            filter_text.add_pattern("*" + extension.lower())
        dialog.add_filter(filter_text)