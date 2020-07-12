# ctfscan

Wrapper for my usual enumeration scans for CTFs, Hackthebox, OSCP

## Usage

Within a `screen` session:
```
./ctfscan.py --target IP_OR_HOSTNAME
```

## What it does

 - Runs `nmap` scan against target in a new `screen` window
 - Parses `nmap` output for open ports running HTTP services
 - Runs `gobuster` in a separate `screen` window for each open HTTP service

## Requirements

 - `bash`
 - `screen`
 - `nmap`
 - `gobuster`

## Eventually...

 - Run more commands based on more services parsed from `nmap` output
 - Some sort of "fast" mode which will assume an open port is running the service it is traditionally known for (whereas currently the `nmap` output parsing is more conservative, waiting for confirmation)