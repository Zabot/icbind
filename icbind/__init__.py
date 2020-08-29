import os
import subprocess
import sys


def directory_sync(src, dest):
    os.makedirs(dest, exist_ok=True)
    cmd = ['rsync', '-av', '--progress', src, dest]

    rsync = subprocess.Popen(cmd)
    rsync.wait()
    if rsync.returncode != 0:
        sys.exit(rsync.returncode)
