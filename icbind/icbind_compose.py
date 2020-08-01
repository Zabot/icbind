#!/usr/bin/env python
import os
import subprocess
import sys

import yaml


# Traverse the directory tree up until locating a docker compose file
def main():
    while os.getcwd() != '/':
        try:
            with open("./docker-compose.yml") as composefile:
                contexts = {}
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

                for context, images in contexts.items():
                    for image in images:
                        build = subprocess.Popen(['icbind',
                                                  context,
                                                  '-t',
                                                  image])
                        build.wait()
                        if build.returncode != 0:
                            sys.exit(build.returncode)
                break
        except FileNotFoundError:
            os.chdir('..')


if __name__ == '__main__':
    main()
