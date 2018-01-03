import subprocess

import sublime_plugin


class SubliMeldFilesCommand(sublime_plugin.WindowCommand):
    @staticmethod
    def run_meld_cmd(paths):
        cmd = ["meld"]
        cmd.extend([p for p in paths])
        print("cmd: ", cmd)
        subprocess.Popen(cmd)

    @staticmethod
    def get_active_views_paths(window):
        """Return list of path all visible views of the active window."""
        visible_views = []

        # Priority for the active view
        active_view = window.active_view()
        visible_views.append(active_view.file_name())

        num_groups = window.num_groups()
        for group_id in range(num_groups):
            view = window.active_view_in_group(group_id)
            if view != active_view and view.file_name():
                visible_views.append(view.file_name())

        return visible_views

    def run(self, *extra_paths):
        paths = self.get_active_views_paths(self.window)

        if extra_paths:
            paths.extend(extra_paths)

        if not paths:
            self.window.status_message("SubliMeld: No active view.")
        elif 1 <= len(paths) <= 3:
            self.run_meld_cmd(paths)
        else:
            self.window.status_message("SubliMeld: More than three views.")
