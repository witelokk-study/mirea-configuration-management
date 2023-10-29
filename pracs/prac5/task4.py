import subprocess
import os
import sys
from pathlib import Path

path = Path(os.getcwd())
while ".git" not in [Path(x).name for x in path.glob("*")] and path.root:
    if path == path.parent:
        print("This is not a git repository!")
        sys.exit()
    path = path.parent

path /= ".git/objects"

for object_path in path.glob("*/*"):
    object_name = object_path.parent.name + object_path.name
    subprocess.call(["git", "cat-file", "-p", object_name])
