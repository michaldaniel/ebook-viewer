import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Pango as pango

class ChaptesListItem(Gtk.ListBoxRow):
    def __init__(self, data, chapter):
        super(Gtk.ListBoxRow, self).__init__()
        self.data = data
        self.chapter = chapter
        label = Gtk.Label(xalign=0)
        label.set_text(data)
        label.set_justify(Gtk.Justification.LEFT)
        label.set_margin_start(10)
        label.set_width_chars(20)
        label.set_ellipsize(pango.EllipsizeMode.END)
        self.add(label)


class ChaptersListComponent(Gtk.ListBox):
    def __init__(self, window):
        super(Gtk.ListBox, self).__init__()
        self.__window = window
        self.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.connect('row-selected', self.__on_listbox_row_selected)
        self.__populate_listbox()

    def __populate_listbox(self):
        for i in range(len(self.__window.content_provider.titles)):
            self.add(ChaptesListItem(self.__window.content_provider.titles[i],i))
        self.show_all()


    def __on_listbox_row_selected(self, listbox, row):
        self.__window.load_chapter(row.chapter)

    def reload_listbox(self):
        children = self.get_children()
        for element in children:
            self.remove (element)
        self.__populate_listbox()
        self.show_all()