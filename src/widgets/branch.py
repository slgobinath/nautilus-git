
class BranchWidget(Gtk.Window, GObject.GObject):
    __gsignals__ = {
        'refresh': (GObject.SIGNAL_RUN_FIRST, None, ())
    }

    def __init__(self, git, window):
        Gtk.Window.__init__(self, Gtk.WindowType.POPUP)
        GObject.GObject.__init__(self)
        self._git = git

        # Header Bar
        self._build_headerbar()
        self.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)
        self.set_titlebar(self.hb)
        self.set_default_size(350, 100)
        self.set_transient_for(window)
        self.set_modal(True)
        self.set_resizable(False)
        self.set_border_width(18)
        self._build_main_widget()

        self.show_all()

    def _build_headerbar(self):
        self.hb = Gtk.HeaderBar()
        self.hb.set_title(self._git.get_project_branch())
        # self.hb.set_show_close_button(True)

        self.apply = Gtk.Button()
        self.apply.set_label(_("Apply"))
        self.apply.get_style_context().add_class("suggested-action")
        self.apply.connect("clicked", self.update_branch)
        self.apply.set_sensitive(False)
        self.apply.show()
        self.hb.pack_end(self.apply)

        self.cancel = Gtk.Button()
        self.cancel.set_label(_("Cancel"))
        self.cancel.connect("clicked", self.close_window)
        self.cancel.show()
        self.hb.pack_start(self.cancel)

    def _build_main_widget(self):
        grid = Gtk.Grid()
        branches = self._git.get_branch_list()
        current_branch = self._git.get_branch()
        self.branch_entry = Gtk.ComboBoxText.new_with_entry()
        self.branch_entry.set_entry_text_column(0)
        i = 0
        for branch in branches:
            if branch == current_branch:
                active_id = i
            self.branch_entry.append_text(branch)
            i += 1
        self.branch_entry.set_active(active_id)
        self.branch_entry.connect("changed", self._validate_branch_name)
        self.branch_entry.show()
        grid.set_halign(Gtk.Align.CENTER)
        grid.add(self.branch_entry)
        grid.show()
        self.add(grid)

    def _validate_branch_name(self, entry):
        branch = entry.get_active_text().strip()
        valid = True
        if branch == self._git.get_branch() or not branch:
            valid = False
        else:
            valid = self._git.check_branch_name(branch)

        self.apply.set_sensitive(valid)
        if valid:
            entry.get_style_context().remove_class("error")
        else:
            entry.get_style_context().add_class("error")

    def update_branch(self, *args):
        branch = self.branch_entry.get_active_text().strip()
        self._git.update_branch(branch)
        self.emit("refresh")
        self.close_window()
        # Todo : refresh the window if possible?

    def close_window(self, *args):
        self.destroy()
