#!/usr/bin/env python3
"""Run PAML programs for all available tests"""

import glob
import os
import platform
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

## [[ SET GLOBAL PATHS ]] ##

# Set up working directory
REPO_ROOT = Path.cwd().resolve().parent 
BIN_DIR = REPO_ROOT/"bin"
TEST_DIR = REPO_ROOT/"test"
print('\n[[ PATHS]]\n')
print(f'Path to root: {REPO_ROOT}\n')
print(f'Path to \"bin\" directory: {REPO_ROOT}\n')
print(f'Path to \"test\" directoryt: {TEST_DIR}\n')

# Set suffix "exe" for Windows binaries
if platform.system() == "Windows":
    EXE_SUFFIX = ".exe"
else:
    EXE_SUFFIX = ""

# Collect failures
failures = []

## [[ FUNCTIONS ]]

def binary_for(program: str) -> Path:
    """Extract full path to PAML program"""
    exe = BIN_DIR/(program + EXE_SUFFIX)
    # When not on Windows, give executable permissions 
    if EXE_SUFFIX == "" and exe.exists():
        os.chmod(exe, 0o755)
    return exe

def run(program: str, args, cwd: Path) -> None:
    """Run one program invocation, print a header, record failure on non-zero exit."""
    # Get path to PAML program
    exe = binary_for(program)
    # Check which files exist before running the program
    before = set(cwd.iterdir())
    # Launch PAML program using `subprocess.run()`
    result = subprocess.run(
        [str(exe), *args],   # List with the command and arguments; `args` must be a list too
        check=False,
        cwd=str(cwd),        # Run in the directory passed to the function
        capture_output=True, # Get sdout and stderr and save as `result.stdout` and `result.stderr`
        text=True,           # Get readable output
    )
    # Show output for debugging
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    # Clean after a successful run
    if result.returncode == 0:
        after = set(cwd.iterdir())
        print(f"## [TEST PASSED]: cleaning after {program} completed successfully\n")
        for new_file in after - before:
            if new_file.is_file():
                new_file.unlink()
    # If something failed, object `results` will tell
    if result.returncode != 0:
        print(f"## [FAILED]: {program} (exit {result.returncode})\n")
        failures.append(program)
    # NOTE: this only catches failures PAML reports via exit code
    # If PAML exits 0 on bad runs, further inspect result.stdout/stderr here

# Returns 0 (pass) or 1 (fail)
def main() -> int:
    # Start counter
    print(f'\nAnalyses start on {datetime.now().strftime("%Y-%m-%d at %H:%M:%S")}')
    start = time.perf_counter()
    for program_dir in sorted(TEST_DIR.iterdir()):
        # Make sure this is a directory
        if not program_dir.is_dir():
            continue
        program = program_dir.name
        print(f"\nTests with PAML program {program}")
        # Options for different programs
        # NOTE: `args` must be a list!
        if program == "ds":
            for ds_f in glob.glob(program + "/*.txt"):
                print(f"~~> Test with PAML program {program}: summarising MCMC file")
                run(program = program, args = [ds_f.rsplit("/")[1]], cwd = TEST_DIR/program)
        elif program == "evolver":
            if not glob.glob(program + "/*dat" ):
                sys.exit( "No DAT files to run evolver")
            print(f"~~> Test with PAML program {program}: simulating with nucleotide data")
            run(program = program, args = ["5", "MCbase.dat"], cwd = TEST_DIR/program)
            print(f"~~> Test with PAML program {program}: simulating with codon data")
            run(program = program, args = ["6", "MCcodon.dat"], cwd = TEST_DIR/program)
            print(f"~~> Test with PAML program {program}: simulating with amino acid data")
            run(program = program, args = ["7", "MCaa.dat"], cwd = TEST_DIR/program)
        else:
            if not glob.glob(program + "/*ctl" ):
                sys.exit(f"No control files to run PAML program {program}")
            for ctl_f in glob.glob(program+"/*.ctl"):
                test_name = re.sub(pattern = r'\.ctl', repl = '', string = re.sub(pattern = '..*_', repl = '', string = ctl_f))
                print(f"~~> Test with PAML program {program}: {test_name}")
                run(program = program, args = [ctl_f.rsplit("/")[1]], cwd = TEST_DIR/program)
    # If a program/s has/have failed...
    end = time.perf_counter()
    elapsed = end - start
    if failures:
        print(f"\n{len(failures)} test(s) failed | Total time: {elapsed}\n")
        return 1
    print(f"\nAll PAML tests passed | Total time: {elapsed}\n")
    print(f'\nAnalyses finish on {datetime.now().strftime("%Y-%m-%d at %H:%M:%S")}\n')
    return 0

if __name__ == "__main__":
    sys.exit(main())