

class WatchDog(Thread, GObject.GObject):
    __gsignals__ = {
        'refresh': (GObject.SIGNAL_RUN_FIRST, None, ())
    }

    def __init__(self, git_path):
        Thread.__init__(self)
        GObject.GObject.__init__(self)
        self.daemon = True
        self.name = git_path
        self._to_watch = path.join(git_path, ".git", "HEAD")
        self.alive = path.exists(self._to_watch)
        self._modified_time = None
        self.start()

    def emit(self, *args):
        GLib.idle_add(GObject.GObject.emit, self, *args)

    def run(self):
        while self.alive:
            fstat = stat(self._to_watch)
            modified = fstat.st_mtime
            if modified and modified != self._modified_time:
                if self._modified_time is not None:
                    self.emit("refresh")
                self._modified_time = modified
            sleep(1)

    def kill(self):
        self.alive = False
