#!/usr/bin/env python3

import subprocess

folders = ["configs", "org", "scripts", ".emacs.d"]

def gitpull():
    for d in folders:
        folder = f"~/{d}"
        if d != '.emacs.d':
            cmd = f"cd {folder} && git pull"
        else:
            cmd = f"cd {folder} && git pull --rebase"
        subprocess.run(cmd, shell=True)
    else:
        print(f"git pull complete for: {folders}")

if __name__ == "__main__":
   gitpull()
