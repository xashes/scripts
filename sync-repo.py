#!/usr/bin/env python3

import subprocess

folders = ["configs", "org", "scripts", ".emacs.d", "fork/mind-wave"]

def gitpull():
    for d in folders:
        folder = f"~/{d}"
        cmd = f"cd {folder} && git pull"
        subprocess.run(cmd, shell=True)
    else:
        print(f"git pull complete for: {folders}")

if __name__ == "__main__":
   gitpull()
