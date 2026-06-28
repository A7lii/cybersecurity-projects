import hashlib
import os
import json
from datetime import datetime

WATCH_DIR = "./watched_folder"
BASELINE = "baseline.json"

def hash_file(filepath):
    sha256 = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    except (IOError, PermissionError):
        return None

def scan_directory(directory):
    hashes = {}
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_hash = hash_file(filepath)
            if file_hash:
                rel_path = os.path.relpath(filepath, directory)
                hashes[rel_path] = file_hash
    return hashes

def create_baseline():
    if not os.path.exists(WATCH_DIR):
        os.makedirs(WATCH_DIR)
        print(f"Created watch directory: {WATCH_DIR}")
        print("Add some files to it then run again to create baseline.")
        return

    print(f"Scanning {WATCH_DIR}...")
    hashes = scan_directory(WATCH_DIR)

    baseline_data = {
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "directory": WATCH_DIR,
        "file_count": len(hashes),
        "hashes": hashes
    }

    with open(BASELINE, "w") as f:
        json.dump(baseline_data, f, indent=2)

    print(f"Baseline created - {len(hashes)} files hashed.")
    print(f"Saved to {BASELINE}")

def check_integrity():
    if not os.path.exists(BASELINE):
        print("No baseline found. Run with --baseline first.")
        return

    with open(BASELINE, "r") as f:
        baseline_data = json.load(f)

    baseline_hashes = baseline_data["hashes"]
    current_hashes = scan_directory(WATCH_DIR)

    modified = []
    added = []
    deleted = []

    for filepath, old_hash in baseline_hashes.items():
        if filepath not in current_hashes:
            deleted.append(filepath)
        elif current_hashes[filepath] != old_hash:
            modified.append(filepath)

    for filepath in current_hashes:
        if filepath not in baseline_hashes:
            added.append(filepath)

    print(f"File Integrity Check - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Directory: {WATCH_DIR}")
    print(f"Baseline created: {baseline_data['created']}")
    print("-" * 50)

    if not any([modified, added, deleted]):
        print("All files intact. No changes detected.")
    else:
        print("Changes detected!\n")
        if modified:
            print(f"Modified ({len(modified)}):")
            for f in modified:
                print(f"  - {f}")
        if added:
            print(f"\nNew files ({len(added)}):")
            for f in added:
                print(f"  + {f}")
        if deleted:
            print(f"\nDeleted ({len(deleted)}):")
            for f in deleted:
                print(f"  x {f}")

    print(f"\nFiles monitored: {len(baseline_hashes)}")

def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 integrity_checker.py --baseline")
        print("  python3 integrity_checker.py --check")
        return

    if sys.argv[1] == "--baseline":
        create_baseline()
    elif sys.argv[1] == "--check":
        check_integrity()
    else:
        print("Unknown option. Use --baseline or --check")

if __name__ == "__main__":
    main()
