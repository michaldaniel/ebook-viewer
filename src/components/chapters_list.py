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
from gi.repository import Pango


class ChaptersListItem(Gtk.ListBoxRow):
    def __init__(self, data, chapter):
        """
        Holds data that is chapter name and chapter_link that is link to chapter file. For use as ListBox element.
        :param data:
        :param chapter:
        """
        super(Gtk.ListBoxRow, self).__init__()

        # Remember chapter name and file link
        self.data = data
        self.chapter_link = chapter

        # Just a bunch of label styling
        label = Gtk.Label(xalign=0)
        label.set_text(data)
        label.set_justify(Gtk.Justification.LEFT)
        label.set_margin_start(10)
        label.set_width_chars(20)
        label.set_ellipsize(Pango.EllipsizeMode.END)

        self.add(label)


class ChaptersListComponent(Gtk.ListBox):
    def __init__(self, window):
        """
        Provides the List Box with chapters index and navigation based around them
        :param window: Main application window reference, serves as communication hub
        """
        super(Gtk.ListBox, self).__init__()
        self.__window = window
        # Only one chapter can be selected at a time
        # set_current_chapter() method relies on this
        self.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.connect('row_activated', self.__on_listbox_row_activated)
        self.__populate_listbox()

    def __populate_listbox(self):
        """
        Fills List Box with chapter titles
        """
        for i in range(len(self.__window.content_provider.titles)):
            self.add(ChaptersListItem(self.__window.content_provider.titles[i][0],
                                      self.__window.content_provider.titles[i][1]))
        self.show_all()

    def __on_listbox_row_activated(self, listbox, row):
        """
        Handles activated event and loads selected chapter
        :param listbox:
        :param row:
        """
        self.__window.load_chapter(self.__window.content_provider.chapter_links.index(row.chapter_link))

    def reload_listbox(self):
        """
        Reloads all List Box element by first removing them and then calling __populate_listbox()
        """
        children = self.get_children()
        for element in children:
            self.remove(element)
        self.__populate_listbox()
        self.show_all()

    def set_current_chapter(self, chapter):
        """
        Called during navigation sets current chapter based on reader position
        :param chapter: integer with chapter number
        """
        children = self.get_children()
        found = False
        # Loop all List Box elements
        for i in range(len(children)):
            # If chapter number greater is greater then chapter number of
            # current list box entry set that element as selected
            # It will fire multiple times selecting all elements up to last
            # that satisfies that condition, but since List Box selection mode
            # allows only one item to be selected user will see only last "current" chapter selected
            if chapter - 1 >= self.__window.content_provider.chapter_links.index(children[i].chapter_link):
                self.select_row(children[i])
                found = True
        if not found:
            # If there were no result just un-select everything
            # this means current chapter is before first that is indexed
            self.unselect_all()
