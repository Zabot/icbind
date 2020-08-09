# I Can't Belive its not Docker
I can't belive its not Docker adds annotations to docker files that allow
features not possible with docker alone.

## Features
### Including directories not in the build context
Add a `#include <path_to_directory> <path_in_build_context>` to a dockerfile 
to include the referenced directory in the build context at build time. The
included directory _does not_ have to be inside the main build context, it is
copied into the build context at build time

### Running scripts on the host machine prior to a build
Add `#run <command>` to run a script on the host machine in the build context
before executing the dockerfile

### Flags
Add `#flags <list_of_flags>` to provide modifiers to icbind. Supported flags
are:

* `nocontext` -- Don't automatically copy the path into the build directory.
