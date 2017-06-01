
def get_file_path(uri):
    """Return file path from an uri."""
    url = urlsplit(uri)
    if url.scheme.lower() == "file":
        return url.path
    return None


def is_git(folder_path):
    """Verify if the current folder_path is a git directory."""
    folder_path = get_file_path(folder_path)
    if folder_path:
        output = execute('git rev-parse --is-inside-work-tree',
                         folder_path).lower()
        return output == "true"
    return None


def get_real_git_dir(directory):
    """Return the absolute path of the .git folder."""
    dirs = directory.split("/")
    current_path = ""
    for i in range(len(dirs) - 1, 0, -1):
        current_path = "/".join(dirs[0:i])
        git_folder = path.join(current_path, ".git")
        if path.exists(git_folder):
            return current_path
    return None


def execute(cmd, working_dir=None):
    """Execute a shell command."""
    if working_dir:
        command = Popen(cmd, shell=True, stdout=PIPE,
                        stderr=PIPE, cwd=working_dir)
    else:
        command = Popen(cmd, stdout=PIPE, stderr=PIPE)
    output = command.communicate()[0]
    return output.decode("utf-8").strip()
