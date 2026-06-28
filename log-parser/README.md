# SSH Log Parser

A Python tool that parses SSH authentication logs and detects brute force login attempts. Built to understand how SOC analysts detect attacks from log data.

## How it works
Reads through an auth.log file line by line using regex to extract the timestamp, status, username and IP from each login event. Counts failed attempts per IP and flags any IP that fails 5 or more times as suspicious. Also flags IPs that had both failed and successful logins which could mean a successful attack after a brute force attempt.

## Usage
Put your auth.log file in the same folder then run:
python3 log_parser.py

## Results
Tested with a simulated auth.log containing brute force activity. Detected 2 suspicious IPs - one with 7 failed attempts trying multiple usernames, and one with 6 failed attempts. Also flagged an IP that had failures followed by a successful login, which in a real environment would trigger an immediate investigation.
