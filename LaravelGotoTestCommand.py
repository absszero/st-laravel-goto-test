import sublime
import sublime_plugin
import re
import os


class Meta:
    def __init__(self, basename, namespace):
        super().__init__()
        splited = basename.split('.')
        # get original class file
        if ('Test.' in basename):
            splited[0] = splited[0][:-4]
            self.classname = splited[0]
            self.target = '.'.join(splited)
            self.toTest = False
        # get test file
        else:
            splited[0] += 'Test'
            self.test_file = '.'.join(splited)
            self.classname = splited[0]
            self.target = '.'.join(splited)
            self.toTest = True

        self.namespace = namespace

        if (self.namespace):
            self.target = self.namespace + '/' + self.target


class LaravelGotoTestCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        super().__init__(view)

    def run(self, edit):
        self.window = sublime.active_window()
        meta = Meta(self.get_basename(), self.get_last_namespace())
        self.search(meta.target)
        return

    def is_visible(self):
        # find <?php
        regions = self.view.find_by_selector(
            'punctuation.section.embedded.begin.php'
        )
        return 0 != len(regions)

    def get_last_namespace(self):
        region = self.view.find_by_selector('entity.name.namespace')
        if (0 == len(region)):
            return
        namespaces = self.view.substr(region[0])
        splited = namespaces.split('\\')
        # do not include first namespace. EX: use App;
        if (1 < len(splited)):
            return splited[-1]

    def get_basename(self):
        filename = self.window.active_view().file_name()
        return os.path.basename(filename)

    def search(self, filename):
        args = {
            "overlay": "goto",
            "show_files": True,
            "text": filename
        }

        self.window.run_command("show_overlay", args)
        return
