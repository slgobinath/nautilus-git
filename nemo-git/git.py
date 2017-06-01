#!/usr/bin/python3
"""
Nemo git pluging to show useful information under any
git directory

Author : Bilal Elmoussaoui (bil.elmoussaoui@gmail.com)
Version : 1.0
Website : https://github.com/bil-elmoussaoui/nautilus-git
Licence : GPL3
nautilus-git is free software: you can redistribute it and/or
modify it under the terms of the GNU General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
nautilus-git is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with nautilus-git. If not, see <http://www.gnu.org/licenses/>.
"""
import gettext
from gi import require_version
require_version("Gtk", "3.0")
require_version('Nemo', '3.0')
from gi.repository import Gtk, Nemo, GObject

_ = gettext.gettext
gettext.textdomain('nautilus-git')


class NemoGitLocationWidget(GObject.GObject, Nemo.LocationWidgetProvider):
    """Location widget extension."""
    def __init__(self):
        self.window = None
        self.uri = None

    def get_widget(self, uri, window):
        """Overwrite get_widget method."""
        self.uri = uri
        self.window = window
        if is_git(uri):
            git = Git(uri)
            widget = NemoLocation(git, self.window)
            return widget
        else:
            return None


class NemoGitColumnExtension(GObject.GObject, Nemo.PropertyPageProvider):
    """Property widget extension."""
    def __init__(self):
        pass

    @staticmethod
    def get_property_pages(files):
        """Overwrite default method."""
        if len(files) != 1:
            return

        _file = files[0]
        if _file.is_directory():
            uri = _file.get_uri()
            if is_git(uri):
                git = Git(uri)
                property_label = Gtk.Label(_('Git'))
                property_label.show()

                nautilus_property = NemoPropertyPage(git)

                return Nemo.PropertyPage(name="NemoPython::git",
                                             label=property_label,
                                             page=nautilus_property),
