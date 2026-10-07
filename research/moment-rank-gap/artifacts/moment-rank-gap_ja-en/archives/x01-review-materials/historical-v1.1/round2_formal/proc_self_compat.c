/* Runtime compatibility only. Lean 4.19 asks for /proc/<getpid()>/exe;
   this host virtualizes getpid independently of procfs. Resolve that one
   spelling through /proc/self/exe, the same process's executable.
   No Lean source, proof checker, mathematical primitive, or other pathname
   is changed. */
#define _GNU_SOURCE
#include <dlfcn.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

ssize_t readlink(const char *path, char *buf, size_t bufsiz) {
    static ssize_t (*real_readlink)(const char *, char *, size_t) = NULL;
    if (!real_readlink) real_readlink = dlsym(RTLD_NEXT, "readlink");
    char current[64];
    snprintf(current, sizeof(current), "/proc/%d/exe", (int)getpid());
    if (strcmp(path, current) == 0)
        return real_readlink("/proc/self/exe", buf, bufsiz);
    return real_readlink(path, buf, bufsiz);
}
