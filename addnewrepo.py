#!/usr/bin/env python3

import sys
import subprocess


def addnewrepo(repo):
    addr = "git@github.com:xashes"
    ext = "git"
    uri = f"{addr}/{repo}.{ext}"
    subprocess.run("git init -b main", shell=True)
    subprocess.run(f"git remote add origin {uri}", shell=True)
    subprocess.run("git remote -v", shell=True)


if __name__ == "__main__":
    import sys

    repo = sys.argv[1]
    addnewrepo(repo)
