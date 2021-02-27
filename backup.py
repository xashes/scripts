#!/usr/bin/env python3

import subprocess

folders = ["configs", "data", "projects", "books", "plum"]

user = "pi"
host = "pizero"
target = "~/backup"


def backup():
    for f in folders:
        folder = f"~/{f}"
        cmd = f"rsync -av {folder} {user}@{host}:{target}"
        subprocess.run(cmd, shell=True)
    else:
        print(f"Backup complete for: {folders}")


if __name__ == "__main__":
    backup()
