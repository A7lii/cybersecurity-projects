# Port Scanner

A Python port scanner I built to learn network reconnaissance. It scans a target machine for open ports and tries to grab the service banner from each open port to identify what software is running and what version.

## How it works
Sends a TCP connection attempt to each port. If it connects, it sends a basic HTTP request and reads whatever the service sends back. Uses threading so it scans 100 ports at a time instead of one by one, which makes it much faster.

## Usage
Change the TARGET variable to your target IP then run:
python3 port_scanner.py

## Results
Tested against Metasploitable 2 in my home lab. Found 12 open ports including vsftpd 2.3.4 which has a known backdoor (CVE-2011-2523), an outdated Apache 2.2.8 web server, and Telnet running in plain text. Used the results to identify and then exploit vulnerabilities on the target.
