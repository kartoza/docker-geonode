import unittest
from unittest.mock import patch
import os
import sys
import dotenv
import subprocess
import shutil

class TestPhases(unittest.TestCase):
    current_dir = os.path.abspath(__file__)

    def setUp(self):
        dotenv.load_dotenv(override=True)
        self.overlay_dir = os.path.abspath(os.getenv('OVERLAY_DIRECTORY'))
        self.build_dir = os.path.abspath(os.getenv('BUILD_DIRECTORY'))
        self.project_root = os.path.abspath(os.getenv('PROJECT_ROOT'))
        self.bootstrap_dir = os.path.abspath(os.getenv('BOOTSTRAP_DIRECTORY'))
        sys.path.append(os.path.join(self.bootstrap_dir, 'scripts'))
        try:
            shutil.rmtree(self.build_dir)
        except FileNotFoundError:
            pass

    def test_overlay(self):
        # scripts path from overlay scripts must be in the shell already
        with patch('sys.argv', ['', self.overlay_dir, self.build_dir]):
            import overlay
            overlay.main()
        self.assertTrue(os.path.exists(self.build_dir))
        # check some files exists
        files = [
            'source_config.yaml',
            'b.txt',
            'a.txt'
        ]
        for f in files:
            full_path = os.path.abspath(os.path.join(self.build_dir, f))
            self.assertTrue(os.path.exists(full_path))

    def test_generate(self):
        def _shellrun(command_array, cwd=None, capture_ouput=None):
            """mock function to debug jinja2_gen"""
            script = command_array[0]
            if script == 'jinja2_gen.py':
                import jinja2_gen
                with patch('sys.argv', command_array):
                    curcwd = os.getcwd()
                    os.chdir(cwd)
                    try:
                        jinja2_gen.main()
                    except:
                        pass
                    os.chdir(curcwd)
            else:
                return subprocess.run(command_array, cwd=cwd, capture_ouput=True)
        
        # scripts path from overlay scripts must be in the shell already
        with patch('sys.argv', ['', self.overlay_dir, self.build_dir]):
            import overlay
            overlay.main()
            import generate
            # Uncomment the following 2 lines to mock subprocess and debug it
            # inside a python debugger
            # with patch('subprocess.run', _shellrun):
            #     generate.main()
            generate.main()
        # check generated files

        files = [
            'templates/example-from-json.yaml',
            'templates/example-from-yaml.yaml',
        ]

        control_file = os.path.abspath(os.path.join(
            self.build_dir, 'templates/control.yaml'))
        with open(control_file) as f:
            control_content = f.readlines()

        for f in files:
            full_path = os.path.abspath(os.path.join(self.build_dir, f))
            self.assertTrue(os.path.exists(full_path), msg=full_path)
            with open(full_path) as f:
                generated_content = f.readlines()
            
            # compare with a control file
            self.assertEqual(control_content, generated_content)