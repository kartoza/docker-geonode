import unittest
import os
import dotenv
import subprocess
import shutil

class TestPhases(unittest.TestCase):
    current_dir = os.path.abspath(__file__)

    def setUp(self):
        dotenv.load_dotenv()
        self.overlay_dir = os.getenv('OVERLAY_DIRECTORY')
        self.build_dir = os.getenv('BUILD_DIRECTORY')
        self.project_root = os.getenv('PROJECT_ROOT')
        self.bootstrap_dir = os.getenv('BOOTSTRAP_DIRECTORY')
        shutil.rmtree(self.build_dir)

    def test_overlay(self):
        # scripts path from overlay scripts must be in the shell already
        subprocess.run(['overlay.py', self.overlay_dir, self.build_dir])
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
        # scripts path from overlay scripts must be in the shell already
        subprocess.run(['overlay.py', self.overlay_dir, self.build_dir])
        subprocess.run(['generate.py', self.overlay_dir, self.build_dir])
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
            self.assertTrue(os.path.exists(full_path))
            with open(full_path) as f:
                generated_content = f.readlines()
            
            # compare with a control file
            self.assertEqual(control_content, generated_content)