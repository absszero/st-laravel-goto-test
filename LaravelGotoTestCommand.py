import sublime
import sublime_plugin
import re
import os


class LaravelGotoTestCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        super().__init__(view)

    def run(self, edit):
        self.window = sublime.active_window()
        filename = self.get_filename()
        namespace = self.get_last_namespace()
        if (namespace):
            filename = namespace + '/' + filename
        self.search(filename)
        return

    def get_last_namespace(self):
        region = self.view.find_by_selector('entity.name.namespace')
        if (0 == len(region)):
            return
        namespaces = self.view.substr(region[0])
        splited = namespaces.split('\\')
        # do not include first namespace. EX: use App;
        if (1 < len(splited)):
            return splited[-1]

    def get_filename(self):
        filename = self.window.active_view().file_name()
        basename = os.path.basename(filename)
        splited = basename.split('.')
        # get original class file
        if ('Test.' in basename):
            splited[0] = splited[0][:-4]
        # get test file
        else:
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
