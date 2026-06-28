# File Integrity Checker

A Python tool that monitors a folder for unauthorised file changes using SHA-256 hashing. Built to understand how host-based intrusion detection systems like Tripwire and OSSEC work.

## How it works
Hashes every file in a target directory using SHA-256 and saves the results as a baseline. When run again it rehashes every file and compares against the baseline, flagging anything that has been modified, added or deleted.

## Usage
First create a baseline:
python3 integrity_checker.py --baseline

Then check for changes:
python3 integrity_checker.py --check

## Results
Tested by creating a baseline of 3 files then modifying one. The tool detected the change instantly by comparing the new SHA-256 hash against the stored baseline. SHA-256 means even a single character change produces a completely different hash, so nothing slips through.
