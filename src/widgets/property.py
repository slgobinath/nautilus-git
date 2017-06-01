
GIT_FILES_STATUS = {
    "added": {
        "icon": "list-add-symbolic",
        "tooltip": _("Added files"),
        "properties": _("Added :")
    },
    "removed": {
        "icon": "list-remove-symbolic",
        "tooltip": _("Removed files"),
        "properties": _("Removed :")
    },
    "modified": {
        "icon": "document-edit-symbolic",
        "tooltip": _("Modified files"),
        "properties": _("Modified :")
    }
}



class NautilusPropertyPage(Gtk.Grid):
    """Property page main widget class."""

    def __init__(self, git):
        Gtk.Grid.__init__(self)
        self._git = git
        self._watchdog = WatchDog(self._git.dir)
        self._watchdog.connect("refresh", self.refresh)
        self.set_border_width(18)
        self.set_vexpand(True)
        self.set_row_spacing(6)
        self.set_column_spacing(18)
        self._build_widgets()
        self.show()

    def _build_widgets(self):
        """Build needed widgets."""
        branch = Gtk.Label(_('Branch:'))
        branch.set_halign(Gtk.Align.END)
        branch.show()

        self.attach(branch, 0, 0, 1, 1)

        self.branch_value = Gtk.Label()
        self.branch_value.set_text(self._git.get_branch())
        self.branch_value.set_halign(Gtk.Align.END)
        self.branch_value.show()

        self.attach(self.branch_value, 1, 0, 1, 1)
        status = self._git.get_status()
        i = 2
        for _status in status:
            if len(status[_status]) > 0:
                label = Gtk.Label()
                label.set_text(GIT_FILES_STATUS[_status]["properties"])
                label.set_halign(Gtk.Align.END)
                label.show()
                self.attach(label, 0, i, 1, 1)

                label_value = Gtk.Label()
                label_value.set_text(str(len(status[_status])))
                label_value.set_halign(Gtk.Align.END)
                label_value.show()
                self.attach(label_value, 1, i, 1, 1)
                i += 1

    def refresh(self, event):
        self.branch_value.set_text(self._git.get_branch())
        self.branch_value.show()
