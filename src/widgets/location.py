
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



class NautilusLocation(Gtk.InfoBar):
    """Location bar main widget."""
    _popover = None
    _diff_button = None
    _watchdog = None

    def __init__(self, git, window):
        Gtk.InfoBar.__init__(self)
        self._window = window
        self._git = git
        self._watchdog = WatchDog(self._git.dir)
        self._watchdog.connect("refresh", self.refresh)
        self.set_message_type(Gtk.MessageType.QUESTION)
        self.show()
        self._build_widgets()

    def _build_widgets(self):
        """Build needed widgets."""
        container = Gtk.Grid()
        container.set_row_spacing(6)
        container.set_column_spacing(6)
        container.set_valign(Gtk.Align.CENTER)
        container.show()

        icon = Gio.ThemedIcon(name="nautilus-git-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.SMALL_TOOLBAR)
        image.show()
        container.attach(image, 0, 0, 1, 1)

        branch_button = Gtk.Button()
        branch_button.set_label(self._git.get_project_branch())
        branch_button.connect("clicked", self._update_branch)
        branch_button.show()
        container.attach(branch_button, 1, 0, 1, 1)
        self.get_content_area().add(container)

        status = self._git.get_status()
        container.attach(self._build_status_widget(status), 2, 0, 1, 1)

        button = Gtk.Button()
        button.set_label(_("More..."))
        button.show()
        self._generate_popover(button)
        button.connect("clicked", self._trigger_popover, self._popover)

        self.get_action_area().pack_end(button, False, False, 0)

    def _update_branch(self, button):
        branch = BranchWidget(self._git, self._window)
        branch.connect("refresh", self.refresh)

    def refresh(self, event):
        action = self._window.lookup_action("reload")
        action.emit("activate", None)

    def _build_status_widget(self, status):
        """Build a widget, contains a counter of modified/added/removed files."""
        i = 0
        grid = Gtk.Grid()
        grid.set_row_spacing(3)
        grid.set_column_spacing(3)
        grid.set_valign(Gtk.Align.CENTER)
        grid.show()
        for _status in status:
            if len(status[_status]) > 0:
                button = Gtk.Button()
                popover = self._create_status_popover(status[_status], _status)
                popover.set_relative_to(button)
                button.connect("clicked", self._trigger_popover, popover)
                icon = Gio.ThemedIcon(name=GIT_FILES_STATUS[_status]["icon"])
                image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.MENU)
                image.set_tooltip_text(GIT_FILES_STATUS[_status]["tooltip"])
                image.show()
                button.set_image(image)
                button.set_label(str(len(status[_status])))
                button.set_always_show_image(True)
                button.show()
                grid.attach(button, i, 0, 1, 1)
                i += 1
        return grid

    def _create_status_popover(self, files, status):
          popover = Gtk.Popover()
          popover.set_border_width(12)
          box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
          for _file in files:
                button = Gtk.Button()
                button.set_label(_file)
                if status != "removed":
                    button.connect("clicked", self._open_default_app, _file)
                button.get_style_context().add_class("flat")
                button.set_halign(Gtk.Align.START)
                button.show()
                box.add(button)
          box.show()
          popover.add(box)
          return popover

    def _open_default_app(self, button, _file):
        file_path = "file://" + path.join(self._git.dir, _file)
        Gio.app_info_launch_default_for_uri(file_path)

    def _trigger_popover(self, button, popover):
        """Show/hide popover."""
        if popover.get_visible():
            popover.hide()
        else:
           popover.show()

    def _generate_popover(self, widget):
        """Create the popover."""
        self._popover = Gtk.Popover()
        self._popover.set_border_width(12)
        self._popover.set_relative_to(widget)
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        box.show()
        remote_button = Gtk.Button()
        remote_button.set_halign(Gtk.Align.START)
        remote_button.set_label(_("Open remote URL"))
        remote_button.get_style_context().add_class("flat")
        remote_url = self._git.get_remote_url()
        remote_button.connect("clicked", self._open_remote_browser, remote_url)
        if remote_url.lower().startswith(("http://", "https://", "wwww")):
            remote_button.show()
        box.add(remote_button)

        files = self._git.get_modified()

        self._diff_button = Gtk.Button()
        self._diff_button.set_halign(Gtk.Align.START)
        self._diff_button.get_style_context().add_class("flat")
        self._diff_button.set_label(_("Compare commits"))
        self._diff_button.connect("clicked", self._compare_commits)
        if len(files) > 0:
            self._diff_button.show()
            box.add(self._diff_button)

        self._popover.add(box)

    def _compare_commits(self, *args):
        """Compare commits widget creation."""
        widget = NautilusGitCompare(self._git)
        self._popover.hide()
        widget.show()

    def _open_remote_browser(self, button, remote_url):
        """Open the remote url on the default browser."""
        Gio.app_info_launch_default_for_uri(remote_url)
        self._popover.hide()
