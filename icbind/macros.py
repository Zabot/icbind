import os
import re
import shutil
import subprocess
import sys

from icbind import directory_sync


def include(match, context, build_dir):
    included_path = context + '/' + match[1]

    # If a destination path was specified, copy to it
    if match[2]:
        dest_path = build_dir + '/' + match[2]
    else:
        dest_path = build_dir

    print("Including {} in build directory".format(included_path))
    directory_sync(included_path, dest_path)


def run(match, context, build_dir):
    if match[2]:
        args = match[2].split()
    else:
        args = []

    # Get the absolute path of the command
    wd = os.getcwd()
    os.chdir(context)
    exe_path = os.path.abspath(shutil.which(match[1]))
    os.chdir(wd)

    run = subprocess.Popen([exe_path, *args],
                           cwd=build_dir)
    run.wait()
    if run.returncode != 0:
        sys.exit(run.returncode)


regexes = [
    (re.compile('^\\s*#\\s*include\\s+(\\S+)\\s*(\\S+)?$'), include),
    (re.compile('^\\s*#\\s*run\\s+(\\S+)\\s*(.+)?$'), run),
]
