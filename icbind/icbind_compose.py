#!/usr/bin/env python
import argparse
import pathlib
import subprocess
import sys

import yaml


def up_find(target, start=()):
    p = pathlib.Path(*start).resolve()
    for d in (p / 'a').parents:
        if (d / target).exists():
            return d / target

    raise FileNotFoundError("Could not find {} in {} or any of its parents"
                            .format(target, p))


# Traverse the directory tree up until locating a docker compose file
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f',
                        dest='file',
                        nargs='*',
                        action='append',
                        default=[])
    parser.add_argument('--dry_run', action='store_true')

    args = parser.parse_args(sys.argv[1:])
    composefiles = [arg for opt in args.file for arg in opt]

    # If no files were specified, search the directory tree
    if not composefiles:
        try:
            composefiles = [up_find('docker-compose.yml')]
        except FileNotFoundError as e:
            print(e)
            sys.exit(1)

    # Parse all compose files for build contexts
    contexts = {}
    for f in composefiles:
        with open(f, 'r') as composefile:
            compose = yaml.load(composefile, Loader=yaml.FullLoader)
            for name, service in compose['services'].items():
                try:
                    context = service['build']
                    image = service['image']
                    try:
                        contexts[context].add(image)
                    except KeyError:
                        contexts[context] = set([image])
                except KeyError:
                    pass

    # Build all the discovered dockerfiles
    for context, images in contexts.items():
        for image in images:
            cmd = ['icbind', context, '-t', image]

            if args.dry_run:
                print(cmd)
            else:
                build = subprocess.Popen(cmd)
                build.wait()
                if build.returncode != 0:
                    sys.exit(build.returncode)


if __name__ == '__main__':
    main()
