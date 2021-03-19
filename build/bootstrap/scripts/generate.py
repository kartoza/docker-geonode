#!/usr/bin/env nix-shell
#!nix-shell -i python3 ../shell.nix
"""
Generate phase

Generate phase can use any templating language.
We generally do this to generate configuration files or file constructs
or even documentations.

This particular phase will collect possible templates and provide context
to generate the resulting file.

Auto detected template should have extension .template.<generator>.<ext-type>
For example, some-file.template.jinja2.yaml

The generator phase use the template from inside the build directory,
provide contexts, then render it as a file with the template.<generator> part
omitted. So above example will result in some-file.yaml

Since usually user will have their own templating language. The hook works
by providing a way to register template extension with user generator script.
This happens before the generator is executed.

At the end of the phase, we execute generate.sh hooks so that user
can further customize the post process. For example to chain it with linting
tools.

The generate.sh is a script with a given stdin input in the form of JSON:
[
    {
        'template': <the original template name>
        'output': <the target output name>
    }
"""
import json
import os
import re
import shutil
import subprocess
import sys
from shutil import SameFileError

from bootstrap import stdlib


def main():
    overlay_dir = sys.argv[1]
    build_dir = sys.argv[2]
    overlay_config = stdlib.load_overlay_config(build_dir)
    generator_args = overlay_config.get('generator_args')
    patterns_list = []
    if generator_args:
        # register generator defined in source_config.yaml
        for arg in generator_args:
            file_types = arg.get('file_types')
            command = arg.get('command')
            name = arg.get('name')
            extra_args = arg.get('extra_args')
            for f_type in file_types:
                pattern = f'^(?P<filename>.*)\.template\.{name}\.(?P<extension>{f_type})$'
                patterns_list.append({
                    'pattern': pattern,
                    'command': command,
                    'extra_args': extra_args
                })

        path_lists = stdlib.overlay_path_list(build_dir)
        template_file_lists = []
        output_file_lists = []
        input_for_hook = []
        for f in path_lists['files']:
            for p in patterns_list:
                pattern = p['pattern']
                command = p['command']
                extra_args = p['command']
                match = re.match(pattern, f)
                if match:
                    template_file_lists.append(f)
                    filename = match.group('filename')
                    extension = match.group('extension')
                    output_filename = f'{filename}.{extension}'
                    command_array = [command, f, output_filename]
                    if isinstance(extra_args, list):
                        command_array += extra_args
                    else:
                        command_array.append(extra_args)

                    input_for_hook.append({
                        'template': f,
                        'output': output_filename
                    })
                    result = subprocess.run(command_array, cwd=build_dir)
                    if result.returncode == 0:
                        output_file_lists.append(output_filename)

        # run generator hooks (from the build dir)
        # pass on the template file lists as json, to the stdin
        try:
            subprocess.run(
                ["bash", "-c", ".overlay-hooks/generate.sh"],
                stdin=json.dumps(input_for_hook),
                text=True,
                cwd=build_dir)
        except:
            pass


if __name__ == '__main__':
    main()
