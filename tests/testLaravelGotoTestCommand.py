import sublime
import sys
import os
from unittest import TestCase


class TestLaravelGotoTestCommand(TestCase):
    def setUp(self):
        self.window = sublime.active_window()
        sample = os.path.dirname(__file__) + '/HelloController.php'
        self.view = self.window.open_file(sample)
        while self.view.is_loading():
            pass
        # make sure we have a window to work with
        s = sublime.load_settings("Preferences.sublime-settings")
        s.set("close_windows_when_empty", False)

    def tearDown(self):
        if (self.window.active_view() != self.view):
            try:
                self.window.active_view().window().run_command("close_file")
            except Exception as e:
                pass

        if self.view:
            self.view.set_scratch(True)
            self.view.window().focus_view(self.view)
            self.view.window().run_command("close_file")

    def test_controller(self):
        self.assert_file('HelloControllerTest.php')

    def assert_file(self, expectation):
        self.view.run_command("laravel_goto_test")
        filename = self.window.active_view().file_name()
        self.assertEqual(os.path.basename(filename), expectation)
