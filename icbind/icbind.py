import argparse
import subprocess
import sys
import tempfile

from icbind.macros import regexes
from icbind import directory_sync


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest='file', default=None)
    parser.add_argument('-d', dest='build_dir', default=None)
    parser.add_argument('PATH')
    parser.add_argument('DOCKER OPTIONS', nargs=argparse.REMAINDER)

    args = parser.parse_args(sys.argv[1:])

    # If no custom build directory, generate temporary file
    if not args.build_dir:
        args.build_dir = tempfile.mkdtemp()

    # If no file argument, assume dockerfile is in root of build context
    if not args.file:
        args.file = args.PATH + '/Dockerfile'

    print("Synchronizing default context to build directory")
    directory_sync(args.PATH, args.build_dir)

    # Search the dockerfile for any macros and execute them
    with open(args.file) as dockerfile:
        for line in dockerfile.readlines():
            for regex, parser in regexes:
                m = regex.match(line)
                if m:
                    parser(m, args.PATH, args.build_dir)

    # Build the image in the build directory
    print("Building in {}".format(args.build_dir))
    build = subprocess.Popen(['docker',
                              'build',
                              '-f',
                              args.file,
                              args.build_dir
                              ])
    build.wait()


if __name__ == '__main__':
    main()
