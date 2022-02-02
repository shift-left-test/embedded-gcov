GCC/gcov code coverage data extraction from the actual embedded system, without requiring a file system, or an operating system, or standard C libraries.

See the PDF slide file in the repo for an overview, and see the github wiki for more information about customization options for your embedded system. Also see the simple Linux-compilable example in the repo.

Embedded gcov: Insert in your code
```
#include "gcov_public.h"
…
        // want this as early as possible,
        // but cannot call this until after
        // the trap table and system stuff are set up
        // may not be needed in all systems, depending on startup code
        __gcov_call_constructors();
…
                                case 9: // a command in my system
                                        __gcov_exit(); // dumps the data
                                        break;
…
```
Add the embedded gcov source files gcov\_public.c and gcov\_gcc.c to your build.

You likely want a separate gcov build target, with preprocessor flags.

May need a separate linker file for gnu ld, defining symbols for \_\_gcov\_call\_constructors().

Then compile with gcc and usual coverage flags -ftest-coverage -fprofile-arcs 

NOTE: There is an open source version of embedded-gcov at https://github.com/nasa-jpl/embedded-gcov
but the JPL-github hosted version MAY have changes and additions that are NOT approved for release.
 * This software may be subject to U.S. export control laws and
 * regulations.  By accepting this document, the user agrees to comply
 * with all applicable U.S. export laws and regulations.  User has the
 * responsibility to obtain export licenses, or other export authority
 * as may be required before exporting such information to foreign
 * countries or providing access to foreign persons.
