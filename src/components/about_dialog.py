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
from gi.repository import Gtk, GdkPixbuf



class AboutDialog(Gtk.Window):

    @property
    def show_dialog(self):
        """
        Displays FileChooserDialog with ePub file filters and returns Gtk.ResponseType and filename string
        :return (response, filename):
        """
        aboutdialog = Gtk.AboutDialog()
        aboutdialog.set_position(Gtk.WindowPosition.CENTER)

        license = '''
This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License
as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

        authors = ["Michał Daniel (developer, maintainer)", "Nguyễn Ngọc Thanh Hà (contributor)"]

        #Thank you for the beautiful icon.
        artists = ["Christian da Silva (www.christianda.com)"]

        logo_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size('/usr/share/easy-ebook-viewer/misc/easy-ebook-viewer-scalable.svg', 128, 128)

        aboutdialog.set_logo(logo_pixbuf)
        aboutdialog.set_program_name("Easy eBook Viewer")
        aboutdialog.set_version("1.0")
        aboutdialog.set_authors(authors)
        aboutdialog.set_website("https://github.com/michaldaniel/Ebook-Viewer")
        aboutdialog.set_website_label("Browse code at Github")
        aboutdialog.set_artists(artists);
        aboutdialog.set_license(license)
        aboutdialog.set_comments("Easy eBook Viewer is a simple and moder ePub files reader written in Python using GTK3 and WebKit.")

        aboutdialog.set_title("About Easy eBook Viewer")

        aboutdialog.show_all()
        aboutdialog.run()
        aboutdialog.destroy()
