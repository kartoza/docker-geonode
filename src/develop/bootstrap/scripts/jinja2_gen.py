#!/usr/bin/env nix-shell
#!nix-shell -i python3 ../shell.nix
import dotenv
import os
import json
import yaml
import sys

import jinja2


def from_dotenv(value, dotenv_file, key):
    config = dotenv.dotenv_values(dotenv_file)
    # should fail if the key don't exists or provide default value
    return config.get(key, value)


def from_env(value, key):
    # should fail if the key don't exists or provide default value
    return os.getenv(key, value)


def from_yaml(value, yaml_file, key):
    with open(yaml_file) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        return config.get(key, value)
    raise FileNotFoundError(yaml_file)


def from_json(value, json_file, key):
    with open(json_file) as f:
        config = json.load(f)
        return config.get(key, value)


def main():
    template_name = sys.argv[1]
    output_name = sys.argv[2]
    try:
        context_file = sys.argv[3]
    except:
        context_file = None
    # extra args is the context file
    if context_file and context_file.endswith('.yaml'):
        with open(context_file) as f:
            context = yaml.load(f, Loader=yaml.FullLoader)
    elif context_file and context_file.endswith('.json'):
        with open(context_file) as f:
            context = json.load(f)
    else:
        context = {}

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.getcwd())
    )
    env.filters['from_dotenv'] = from_dotenv
    env.filters['from_env'] = from_env
    env.filters['from_yaml'] = from_yaml
    env.filters['from_json'] = from_json

    template = env.get_template(template_name)
    with open(output_name, mode='w') as f:
        f.write(template.render(
            env=os.environ,
            context=context
        ))


if __name__ == '__main__':
    main()
