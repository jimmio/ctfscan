#!/usr/bin/env python3

import argparse

import subprocess

import time

from typing import TextIO


PARSER = argparse.ArgumentParser(description='Run basic enumeration scans on a target.')

PARSER.add_argument('--target', type=str, help='IP or hostname', required=True)

ARGS = PARSER.parse_args()

TARGET = str(ARGS.host)


def nmap_tcp_scan() -> TextIO: # TODO - note return file object

    nmap_filename = 'nmap-tcp-all-ports'
    nmap_tee_file = nmap_filename + '.tee'
    nmap_cmd = 'nmap -v -p- -sC -sV -oA ' + nmap_filename + ' ' + TARGET
    tee_cmd = 'tee ' + nmap_tee_file
    stuff_cmd = nmap_cmd + ' | ' + tee_cmd + '\n'
    window_title = 'nmap_tcp'
    
    # Ensure the tee file exists and is empty before trying to read it
    subprocess.run(['rm', nmap_tee_file])
    subprocess.run(['touch', nmap_tee_file])
    
    new_window(window_title)
    
    cmd_to_window(stuff_cmd, window_title)

    return open(nmap_tee_file, 'r', encoding='utf-8')


def gobuster_scan(http_port: str) -> list: 

    target_with_port = TARGET + ':' + http_port
    window_title = 'gobuster-' + http_port
    gobuster_output_file = 'gobuster-common-txt-port' + http_port
    gobuster_cmd = 'gobuster dir -x txt -w /usr/share/wordlists/seclists/Discovery/Web-Content/common.txt -u ' + target_with_port
    tee_cmd = 'tee ' + gobuster_output_file
    stuff_cmd = gobuster_cmd + ' | ' + tee_cmd + '\n'

    new_window(window_title)

    cmd_to_window(stuff_cmd, window_title)


def new_window(window_title: str):

    subprocess.run(['screen', '-t', window_title])


def cmd_to_window(cmd: str, window_title: str):

    subprocess.run(['screen', '-p', window_title, '-X', 'stuff', cmd])


def is_open_port(line: str) -> bool:
    
    return ('tcp' in line or 'udp' in line) and \
        'open' in line and \
        'Discovered' not in line


def is_http_service(line: bytes) -> bool:
    
    return 'http' in line


def open_port_handler(line: str):

    if is_http_service(line):
        
        http_service_handler(line)

        
def http_service_handler(line: str):

    http_port = get_port_number(line)

    gobuster_scan(http_port)
    

def get_port_number(line: str) -> str:

    return str(line.split('/')[0])


def follow_file(file_obj):

    file_obj.seek(0,2)
    while True:
        line = file_obj.readline()
        if not line:
            time.sleep(0.1)
            continue
        if is_open_port(line):
            open_port_handler(line)
            continue
        if 'Nmap done' in line:
            break

        
follow_file(nmap_tcp_scan())
