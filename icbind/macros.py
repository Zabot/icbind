import re

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


regexes = [
    (re.compile('^\\s*#\\s*include\\s+(\\S+)\\s*(\\S+)?$'), include),
]
