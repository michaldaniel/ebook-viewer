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
        Displays app about dialog
        """

        # TODO:  Migrate to custom About application dialog designed in line with elementary OS Human Interface Guidelines
        about_dialog = Gtk.AboutDialog()
        about_dialog.set_position(Gtk.WindowPosition.CENTER)

        software_license = _('''
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
''')

        authors = [_("Michał Daniel (developer, maintainer)"),
                   _("Nguyễn Ngọc Thanh Hà (contributor)")]

        # Thank you for the beautiful icon.
        artists = [_("Christian da Silva (www.christianda.com)")]

        logo_pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_size(
            '/usr/share/easy-ebook-viewer/misc/easy-ebook-viewer-scalable.svg', 128, 128)

        about_dialog.set_logo(logo_pixbuf)
        about_dialog.set_program_name(_("Easy eBook Viewer"))
        about_dialog.set_version("1.0")
        about_dialog.set_authors(authors)
        about_dialog.set_website("https://github.com/michaldaniel/Ebook-Viewer")
        about_dialog.set_website_label(_("Browse code at Github"))
        about_dialog.set_artists(artists)
        about_dialog.set_license(software_license)
        about_dialog.set_comments(
            _("Easy eBook Viewer is a simple and moder ePub files reader written in Python using GTK3 and WebKit."))

        about_dialog.set_title(_("About Easy eBook Viewer"))

        about_dialog.show_all()
        about_dialog.run()
        about_dialog.destroy()
