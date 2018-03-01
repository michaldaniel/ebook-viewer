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


import os, sys, gettext
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gio, Gtk, GObject, Gdk
from main_window import MainWindow
from components import about_dialog


class Application(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, application_id="apps.easy-ebook-viewer",
                         flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
                         **kwargs)
        self.window = None
        self.file_path = None
        GLib.set_application_name('Easy eBook Viewer')
        GLib.set_prgname('easy-ebook-viewer')
        GLib.setenv('PULSE_PROP_application.icon_name', 'easy-ebook-viewer', True)

    def do_startup(self):
        Gtk.Application.do_startup(self)

        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.on_about)
        self.add_action(action)

        action = Gio.SimpleAction.new("quit", None)
        action.connect("activate", self.on_quit)
        self.add_action(action)

    def do_activate(self):
        GObject.threads_init()
        gettext.install('easy-ebook-viewer', '/usr/share/easy-ebook-viewer/locale')
        # We only allow a single window and raise any existing ones
        if not self.window:
            # Windows are associated with the application
            # when the last one is closed the application shuts down
            self.window = MainWindow(file_path=self.file_path)
            self.window.connect("delete-event", self.on_quit)
            self.window.set_wmclass("easy-ebook-viewer", "easy-ebook-viewer")
        self.window.show_all()
        if not self.window.book_loaded:
            self.window.header_bar_component.hide_jumping_navigation()
        Gtk.main()

    def do_command_line(self, command_line):
        # If book came from arguments ie. was oppened using "Open with..." method etc.
        if len(sys.argv) > 1:
            # Check if that file really exists
            if os.path.exists(sys.argv[1]):
                self.file_path = sys.argv[1]
        self.activate()
        return 0

    def on_about(self, action, param):
        dialog = about_dialog.AboutDialog()
        dialog.show_all()

    def on_quit(self, action, param):
        Gdk.threads_leave()
        Gtk.main_quit()
        self.quit()

if __name__ == "__main__":
    app = Application()
    app.run(sys.argv)
