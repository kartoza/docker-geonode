# Python stdlib for bootstrap process
import os
import yaml
import fnmatch
import datetime


def load_overlay_config(overlay):
    """Load overlay config file as dict
    """
    try:
        config_file = os.path.join(overlay, 'source_config.yaml')
        config = {}
        with open(config_file) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
    except BaseException as e:
        pass
    return config


def sort_overlays(overlay_dir):
    """
    Sort overlays in increasing depth
    """
    ordered_overlays = []
    for overlay in os.listdir(overlay_dir):
        try:
            overlay_target = os.path.join(overlay_dir, overlay)
            config = load_overlay_config(overlay_target)
            ordered_overlays.append({
                'dir': overlay_target,
                'name': overlay,
                'config': config
            })
        except BaseException as e:
            pass
    return [
        entry for entry 
        in sorted(ordered_overlays, key=lambda item: item['config']['depth'])
    ]


def overlay_path_list(overlay):
    """
    Search for path lists inside an overlay
    """
    ignore_patterns = []
    try:
        overlay_ignore_file = os.path.join(overlay, '.overlayignore')
        with open(overlay_ignore_file) as f:
            ignore_patterns = f.readlines()

        def _pattern_filter_fn(p):
            # strip
            p = p.strip()
            # ignore comment
            is_comment = p.startswith('#')
            if not is_comment and p:
                return p
            else:
                return None

        ignore_patterns = [_pattern_filter_fn(p) for p in ignore_patterns]
        ignore_patterns = [p for p in ignore_patterns if p]

    except BaseException:
        pass

    overlay_files = []
    overlay_dirs = set()
    for root, dirs, files in os.walk(overlay, topdown=True):
        if files:
            relative_root = os.path.relpath(root, overlay)
            relative_root = '' if relative_root == '.' else relative_root
            files = [os.path.join(relative_root, f) for f in files]
            files_set = set(files)
            def _file_filter_fn(f, p):
                return fnmatch.fnmatch(f, p)
            if files_set:
                for ignore_pattern in ignore_patterns:
                    excluded_set = set(fnmatch.filter(files_set, ignore_pattern))
                    files_set = files_set - excluded_set
            
            if files_set:
                overlay_files += list(files_set)
                # also add the root as directories
        
        if files_set and relative_root:
            overlay_dirs.add(relative_root)

    overlay_files.sort()
    overlay_dirs = list(overlay_dirs)
    overlay_dirs.sort()

    return {
        'overlay': overlay,
        'files': overlay_files,
        'dirs': overlay_dirs,
        'ignore_patterns': ignore_patterns
    }


def _overlay_filters(item_sources,):
    complete_item_set = set()
    for item_source in reversed(item_sources):
        if not complete_item_set:
            # Add the whole thing if it's the last/top overlay
            complete_item_set.update(set(item_source['sources']))

            top_overlay = item_source['overlay_paths_object']
        else:
            # only calculate difference
            current_item_set = set(item_source['sources'])
            # exclude items that already in the complete_item_set
            current_item_set.difference_update(complete_item_set)
            # process overlay ignore from previous top overlay
            ignore_patterns = top_overlay['ignore_patterns']
            if current_item_set:
                for ignore_pattern in ignore_patterns:
                    excluded_set = set(fnmatch.filter(current_item_set, ignore_pattern))
                    current_item_set = current_item_set - excluded_set
            # add remaining items to the complete set
            complete_item_set.update(current_item_set)
            # set the current_item_set to current sources, sorted
            current_item_list = sorted(list(current_item_set))
            item_source['sources'] = current_item_list

            top_overlay = item_source['overlay_paths_object']
    # make sure to do it as pure function do, return the edited entry
    return item_sources


def overlays_merge(overlay_dir):
    """
    Merge multiple overlays in overlay_dir, according to the source_config.yaml and
    overlay rules

    The result is the final merged lists of files and dirs relative to the overlay_dir.
    """
    
    overlays = sort_overlays(overlay_dir)
    overlays_full_path = [o['dir'] for o in overlays]
    overlay_paths = [overlay_path_list(o) for o in overlays_full_path]
    result = {
        'dir_sources': [
            {
                'overlay': o['overlay'],
                'overlay_paths_object': o,
                'sources': o['dirs']
            }
            for o in overlay_paths
        ],
        'file_sources': [
            {
                'overlay': o['overlay'],
                'overlay_paths_object': o,
                'sources': o['files']
            }
            for o in overlay_paths
        ],
    }
    # Do priority overlay filters
    # dirs filters:
    ret = _overlay_filters(result['dir_sources'])
    for r in ret:
        del r['overlay_paths_object']
    result['dir_sources'] = ret

    # Do priority overlay filters
    # files filters:
    ret = _overlay_filters(result['file_sources'])
    for r in ret:
        del r['overlay_paths_object']
    result['file_sources'] = ret
    
    return result


def current_calendar_version(time_format=None, with_hour=False):
    """Return calendar version for now, in this moment.

    This function can be used to generate realtime calendar versions.
    """
    # use utc time
    now = datetime.datetime.utcnow()
    if not time_format:
        time_format = 'v%Y.%m.%d'
        if with_hour:
            time_format += '.%H'
    else:
        time_format = ''
    return now.strftime(time_format)
