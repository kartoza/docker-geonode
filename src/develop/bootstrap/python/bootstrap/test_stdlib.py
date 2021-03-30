import bootstrap
from bootstrap import stdlib
import unittest
import os

class TestStdlib(unittest.TestCase):

    package_dir = os.path.dirname(bootstrap.__file__)

    def test_sort_overlays(self):
        overlay_dir = os.path.join(self.package_dir, 'test_fixtures/src')
        result = stdlib.sort_overlays(overlay_dir)
        self.assertTrue(result)
        self.assertEqual(2, len(result))
        self.assertEqual(['main', 'develop'], [e['name'] for e in result])
        

    def test_overlay_paths_list(self):
        overlay_dir = os.path.join(self.package_dir, 'test_fixtures/src')
        overlays = ['main', 'develop']
        overlays = [os.path.join(overlay_dir, o) for o in overlays]
        result = [stdlib.overlay_path_list(o) for o in overlays]

        self.assertTrue(result)
        self.assertEqual(2, len(result))
        self.assertEqual([
            {
                'overlay': overlays[0],
                'files': [
                    '.git-repo/a.idx',
                    '.git-repo/b.idx',
                    '.git-repo/c.idx',
                    '.gitignore',
                    'a.txt',
                    'b.txt',
                    'source_config.yaml',
                    'subdir/a.txt',
                    'subdir/b.txt',
                    'subdir/nested/a.txt',
                    'subdir_2/a.txt'
                ],
                'dirs': [
                    '.git-repo',
                    'subdir',
                    'subdir/nested',
                    'subdir_2',
                ],
                'ignore_patterns': []
            },
            {
                'overlay': overlays[1],
                'files': [
                    '.git-repo/a.idx',
                    '.git-repo/b.idx',
                    '.git-repo/c.idx',
                    '.git-repo/d.idx',
                    '.overlayignore',
                    'b.txt',
                    'c.txt',
                    'source_config.yaml',
                    'subdir/b.txt',
                    'subdir_3/nested/b.txt',
                    'templates/.env', 
                    'templates/context.json', 
                    'templates/context.yaml', 
                    'templates/control.yaml', 
                    'templates/example-from-json.template.jinja2-json.yaml', 
                    'templates/example-from-yaml.template.jinja2-yaml.yaml',
                ],
                'dirs': [
                    '.git-repo',
                    'subdir',
                    'subdir_3/nested',
                    'subdir_4',
                    'templates',
                ],
                'ignore_patterns': [
                    '.gitignore',
                    '.git-repo/*.idx'
                ]
            }
        ],
        result, f'Result:\n{result}')

    def test_merge_overlays(self):
        
        overlay_dir = os.path.join(self.package_dir, 'test_fixtures/src')
        overlays = ['main', 'develop']
        overlays = [os.path.join(overlay_dir, o) for o in overlays]
        result = stdlib.overlays_merge(overlay_dir)

        self.assertTrue(result)
        self.assertEqual({
            'dir_sources': [
                {
                    'overlay': overlays[0],
                    'sources': [
                        'subdir/nested',
                        'subdir_2'
                    ]
                },
                {
                    'overlay': overlays[1],
                    'sources': [
                        '.git-repo',
                        'subdir',
                        'subdir_3/nested',
                        'subdir_4',
                        'templates'
                    ]
                }
            ],
            'file_sources': [
                {
                    'overlay': overlays[0],
                    'sources': [
                        'a.txt',
                        'subdir/a.txt',
                        'subdir/nested/a.txt',
                        'subdir_2/a.txt'
                    ]
                },
                {
                    'overlay': overlays[1],
                    'sources': [
                        '.git-repo/a.idx',
                        '.git-repo/b.idx',
                        '.git-repo/c.idx',
                        '.git-repo/d.idx',
                        '.overlayignore',
                        'b.txt',
                        'c.txt',
                        'source_config.yaml',
                        'subdir/b.txt',
                        'subdir_3/nested/b.txt',
                        'templates/.env', 
                        'templates/context.json', 
                        'templates/context.yaml', 
                        'templates/control.yaml', 
                        'templates/example-from-json.template.jinja2-json.yaml', 
                        'templates/example-from-yaml.template.jinja2-yaml.yaml',
                    ]
                }
            ]
        },
        result, f'Result: \n{result}')
        