

class NautilusGitCompare(Gtk.Window):
    """Nautilus diff window."""

    def __init__(self, git):
        self._git = git
        Gtk.Window.__init__(self)
        title = _("Comparing commits of {0}").format(
            self._git.get_project_name())
        self.set_title(title)
        self.set_default_size(600, 400)
        self._build_headerbar(title)
        GObject.type_register(GtkSource.View)
        self._build_main()
        self.show_all()

    def _build_headerbar(self, title):
        """Generate the headerbar."""
        self._hb = Gtk.HeaderBar()
        self._hb.set_show_close_button(True)
        self._hb.set_title(title)
        # Build list of modified files
        files = self._git.get_modified()
        files.sort()
        self._store = Gtk.ListStore(str)
        for filename in files:
            self._store.append([filename])
        self._files = Gtk.ComboBox.new_with_model(self._store)
        renderer_text = Gtk.CellRendererText()
        self._files.pack_start(renderer_text, True)
        self._files.add_attribute(renderer_text, "text", 0)
        self._files.set_active(0)
        self._files.connect("changed", self._on_file_changed)
        self._hb.pack_start(self._files)
        self.set_titlebar(self._hb)

    def _on_file_changed(self, combobox):
        """File selection changed signal handler."""
        tree_iter = combobox.get_active_iter()
        if tree_iter:
            model = combobox.get_model()
            _file = model[tree_iter][0]
            self.set_buffer(_file)

    def set_buffer(self, file_name):
        """Set the current content to the buffer of the file."""
        lang_manager = GtkSource.LanguageManager()
        language = lang_manager.guess_language(file_name, None)
        diff = self._git.get_diff(file_name)
        buff = GtkSource.Buffer()
        buff.set_highlight_syntax(True)
        buff.set_highlight_matching_brackets(True)
        buff.set_language(language)
        buff.props.text = diff
        self._source.set_buffer(buff)
        stat = self._git.get_stat(file_name)
        if stat:
            self._label.set_text(stat)
            self._label.show()

    def _build_main(self):
        """Build main widgets."""
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        scrolled = Gtk.ScrolledWindow()
        self._source = GtkSource.View()
        scrolled.add_with_viewport(self._source)
        self._label = Gtk.Label()
        self._label.set_halign(Gtk.Align.START)
        self._label.props.margin = 6
        self._source.set_highlight_current_line(True)
        self._source.set_show_line_marks(True)
        self._source.set_background_pattern(
            GtkSource.BackgroundPatternType.GRID)
        self._source.set_draw_spaces(GtkSource.DrawSpacesFlags.TRAILING)

        _file = self._files.get_model()[0][0]
        self.set_buffer(_file)

        self._source.show()
        box.pack_start(self._label, False, False, 0)
        box.pack_start(scrolled, True, True, 0)
        box.show()
        self.add(box)
