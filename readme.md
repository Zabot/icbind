# I Can't Belive its not Docker
I can't belive its not Docker adds annotations to docker files that allow
features not possible with docker alone.

## Features
### Including directories not in the build context
Add a `#include <path_to_directory> <path_in_build_context>` to a dockerfile 
to include the referenced directory in the build context at build time. The
included directory _does not_ have to be inside the main build context, it is
copied into the build context at build time

