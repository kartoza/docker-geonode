from bootstrap import stdlib
import sys

def main():
    overlay_dir = sys.argv[0]
    sorted_overlays = stdlib.sort_overlays(overlay_dir)

    for dir in sorted_overlays:

if __name__ == '__main__':
