import sublime
import sublime_plugin

import subprocess
from os.path import sep as separator


class NinjaBuildCommand(sublime_plugin.WindowCommand):

    def directory_of_file(self, file):
        return separator.join(file.split(separator)[:-1])

    def read_configurations(self):
        config = {}
        try:
            project_file_name = self.window.project_file_name()
            config["working_dir"] = self.directory_of_file(project_file_name)
        except (AttributeError, KeyError):
            current_file_name = self.window.active_view().file_name()
            config["working_dir"] = self.directory_of_file(current_file_name)
        except:
            sublime.error_message(
                "Unexpected error happened in the NinjaBuild plugin!")
            raise
        return config

    def build(self, settings):
        build_system = {
            "shell_cmd": "ninja",
            "working_dir": settings["working_dir"]
        }
        self.window.run_command("show_panel",
                                {"panel": "output.exec"})
        output_panel = self.window.get_output_panel("exec")
        output_panel.settings().set(
            "result_base_dir", build_system["working_dir"])
        print("Cmd: \"{Cmd}\"".format(Cmd=build_system))
        print("Result: {0}", self.window.run_command("exec", build_system))

    def run(self):
        settings = self.read_configurations()
        if settings:
            self.build(settings)
