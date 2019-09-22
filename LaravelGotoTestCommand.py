import sublime
import sublime_plugin
import re
import os


class LaravelGotoTestCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        super().__init__(view)

    def run(self, edit):
        self.window = sublime.active_window()
        filename = self.get_test_filename()
        self.search(filename)
        return

    def get_test_filename(self):
        filename = self.window.active_view().file_name()
        splited = os.path.basename(filename).split('.')
        splited[0] += 'Test'
        return '.'.join(splited)

    def search(self, filename):
        args = {
            "overlay": "goto",
            "show_files": True,
            "text": filename
        }

        self.window.run_command("show_overlay", args)
        return
