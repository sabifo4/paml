#!/usr/bin/env python3
"""Specify global PAML paths and binary type"""

import os
import platform
from pathlib import Path

## [[ SET GLOBAL PATHS ]] ##

# Set working directory
REPO_ROOT = Path.cwd().resolve().parent 
BIN_DIR = REPO_ROOT/"bin"
TEST_DIR = REPO_ROOT/"test/inputs"

## [[ SET FUNCTION TO DEFINE BINARY TYPE ]] ##

# Set suffix "exe" for Windows binaries
if platform.system() == "Windows":
    EXE_SUFFIX = ".exe"
else:
    EXE_SUFFIX = ""

def binary_for(program: str) -> Path:
    """Extract full path to PAML program"""
    exe = BIN_DIR/(program + EXE_SUFFIX)
    # When not on Windows, give executable permissions 
    if EXE_SUFFIX == "" and exe.exists():
        os.chmod(exe, 0o755)
    return exe
