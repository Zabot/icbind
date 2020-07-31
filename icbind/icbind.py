import argparse
import subprocess
import sys
import tempfile

from icbind.macros import regexes
from icbind import directory_sync


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest='file', default='./Dockerfile')
    parser.add_argument('-d', dest='build_dir', default=None)
    parser.add_argument('PATH')
    parser.add_argument('DOCKER OPTIONS', nargs=argparse.REMAINDER)

    args = parser.parse_args(sys.argv[1:])

    if not args.build_dir:
        args.build_dir = tempfile.mkdtemp()

    print("Synchronizing default context to build directory")
    directory_sync(args.PATH, args.build_dir)

    # Search the dockerfile for any macros and execute them
    with open(args.PATH + '/' + args.file) as dockerfile:
        for line in dockerfile.readlines():
            for regex, parser in regexes:
                m = regex.match(line)
                if m:
                    parser(m, args.PATH, args.build_dir)

    # Build the image in the build directory
    print("Building in {}".format(args.build_dir))
    build = subprocess.Popen(['docker',
                              'build',
                              args.build_dir,
                              '-f',
                              args.file])
    build.wait()


if __name__ == '__main__':
    main()
