import os
import re
import shutil
import subprocess
import sys

from icbind import directory_sync


def include(match, context, build_dir, ro=False, metadata={}):
    included_path = context + '/' + match[1]

    # If a destination path was specified, copy to it
    if match[2]:
        dest_path = build_dir + '/' + match[2]
    else:
        dest_path = build_dir

    metadata['depends'].add(included_path)
    if not ro:
        print("Including {} in build directory".format(included_path))
        directory_sync(included_path, dest_path)


def run(match, context, build_dir, ro=False, metadata={}):
    if match[2]:
        args = match[2].split()
    else:
        args = []

    # Get the absolute path of the command
    wd = os.getcwd()
    os.chdir(context)
    exe_path = os.path.abspath(shutil.which(match[1]))
    os.chdir(wd)

    metadata['depends'].add(exe_path)
    if not ro:
        print([exe_path, *args])
        run = subprocess.Popen([exe_path, *args],
                               cwd=build_dir)
        run.wait()
        if run.returncode != 0:
            sys.exit(run.returncode)


def set_flags(match, context, build_dir, ro=False, metadata={}):
    metadata['flags'].update(match[1].split(','))


regexes = [
    (re.compile('^\\s*#\\s*include\\s+(\\S+)\\s*(\\S+)?$'),  include),
    (re.compile('^\\s*#\\s*run\\s+(\\S+)\\s*(.+)?$'),        run),
    (re.compile('^\\s*#\\s*flags\\s+(\\S+(?:,\\S+)*)\\s*$'), set_flags),
]


def execute_macros(dockerfile_path,
                   dockerfile_context,
                   build_context,
                   read_only=False):
    metadata = {
            'flags': set(),
            'depends': set(),
    }

    # Search the dockerfile for any macros and execute them
    with open(dockerfile_path) as dockerfile:
        for line in dockerfile.readlines():
            for regex, parser in regexes:
                m = regex.match(line)
                if m:
                    parser(m,
                           dockerfile_context,
                           build_context,
                           read_only,
                           metadata)

    return metadata
