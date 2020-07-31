import shutil


# Synchronize the contents of two directories, creating parent directories as
# nedded
def directory_sync(src, dest):
    shutil.copytree(src, dest, dirs_exist_ok=True)
