import re
from collections import defaultdict
from datetime import datetime

LOG_FILE = "auth.log"
THRESHOLD = 5
OUTPUT = "log_report.txt"

LOG_PATTERN = re.compile(
    r"(\w+ \d+ \d+:\d+:\d+).*?(Failed|Accepted) password for (\S+) from (\d+\.\d+\.\d+\.\d+)"
)

def parse_log(filepath):
    failed = defaultdict(list)
    success = defaultdict(list)

    try:
        with open(filepath, "r") as f:
            for line in f:
                match = LOG_PATTERN.search(line)
                if match:
                    timestamp, status, user, ip = match.groups()
                    if status == "Failed":
                        failed[ip].append((timestamp, user))
                    else:
                        success[ip].append((timestamp, user))
    except FileNotFoundError:
        print(f"Could not find log file: {filepath}")
        return None, None

    return failed, success

def generate_report(failed, success):
    suspicious = {ip: entries for ip, entries in failed.items() if len(entries) >= THRESHOLD}

    print(f"SSH Log Analysis - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Log file: {LOG_FILE}")
    print("-" * 50)
    print(f"IPs with failed logins: {len(failed)}")
    print(f"Successful logins: {sum(len(v) for v in success.values())}")
    print(f"Suspicious IPs (5+ failures): {len(suspicious)}")
    print()

    if suspicious:
        print("Possible brute force attempts:")
        for ip, entries in sorted(suspicious.items(), key=lambda x: -len(x[1])):
            usernames = list(set(u for _, u in entries))
            print(f"\n  IP: {ip}")
            print(f"  Failed attempts: {len(entries)}")
            print(f"  Usernames tried: {', '.join(usernames)}")
            print(f"  First seen: {entries[0][0]}")
            print(f"  Last seen: {entries[-1][0]}")
            if ip in success:
                print(f"  WARNING: This IP also had a successful login")
    else:
        print("No suspicious activity detected.")

    print("\nAll failed login activity:")
    for ip, entries in sorted(failed.items(), key=lambda x: -len(x[1])):
        print(f"  {ip} - {len(entries)} failure(s)")

    with open(OUTPUT, "w") as f:
        f.write(f"SSH Log Analysis Report\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"Suspicious IPs:\n")
        for ip, entries in suspicious.items():
            usernames = list(set(u for _, u in entries))
            f.write(f"  {ip} - {len(entries)} failures - users tried: {', '.join(usernames)}\n")
            if ip in success:
                f.write(f"  WARNING: also had successful login\n")
        f.write("\nAll failed logins:\n")
        for ip, entries in failed.items():
            f.write(f"  {ip}: {len(entries)} failure(s)\n")

    print(f"\nReport saved to {OUTPUT}")

def main():
    failed, success = parse_log(LOG_FILE)
    if failed is not None:
        generate_report(failed, success)

if __name__ == "__main__":
    main()
