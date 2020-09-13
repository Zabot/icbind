import argparse
import os
import pathlib
import subprocess
import sys

from icbind.macros import execute_macros, flags
from icbind import directory_sync


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest='file', default=None)
    parser.add_argument(
            '-o',
            dest='outfile',
            default=None,
            help='Leave an output file with a timestamp of the last build')
    parser.add_argument('-d', dest='build_dir', default=None)
    parser.add_argument('PATH')
    parser.add_argument('DOCKER_OPTS', nargs=argparse.REMAINDER)
    parser.add_argument('--dry_run', action='store_true')

    args = parser.parse_args(sys.argv[1:])

    args.PATH = os.path.abspath(args.PATH)

    # If no custom build directory, generate temporary file
    if not args.build_dir:
        args.build_dir = '/tmp/icbind/builds/' + args.PATH

    # If no file argument, assume dockerfile is in root of build context
    if not args.file:
        args.file = args.PATH + '/Dockerfile'

    # Execute read only macros to get any metadata from dockerfile
    execute_macros(args.file, args.PATH, args.build_dir, True)

    # Don't copy the dockerfile context into the build directory automatically
    if 'nocontext' not in flags:
        print("Synchronizing default context to build directory")
        directory_sync(args.PATH + '/', args.build_dir)

    # Now execute all macros
    execute_macros(args.file, args.PATH, args.build_dir, False)

    # Build the image in the build directory
    print("Building in {}".format(args.build_dir))
    cmd = ['docker',
            'build',
            '-f',
            args.file,
            *args.DOCKER_OPTS,
            args.build_dir
            ]

    if args.dry_run:
        print(cmd)
    else:
        build = subprocess.Popen(cmd)
        build.wait()
        if build.returncode != 0:
            sys.exit(build.returncode)

        # Touch the output file to update the modified timestamp
        if args.outfile:
            pathlib.Path(args.outfile).touch()


if __name__ == '__main__':
    main()
