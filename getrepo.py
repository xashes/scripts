#!/usr/bin/env python3

import subprocess

uri = "git@github.com:xashes/scripts.git"


def getrepo(repo):
    addr = "git@github.com:xashes"
    ext = "git"
    uri = f"{addr}/{repo}.{ext}"
    cmd = f"git clone {uri}"
    subprocess.run(cmd, shell=True)


if __name__ == "__main__":
    import sys

    repo = sys.argv[1]
    getrepo(repo)
