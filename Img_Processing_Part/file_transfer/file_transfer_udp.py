#!/usr/bin/python
import sys
import time
import socket
import json
import argparse

# python file_transfer_udp.py --file ..\image_processing\output\json_output.json --ip 192.168.43.68 --port 5001                       

parser = argparse.ArgumentParser(description='Transfer JSON data through UDP')
parser.add_argument("--file",
                    dest="in_file",
                    required=True,
                    help="Path to file")
parser.add_argument("--ip",
                    dest="UDP_IP",
                    required=True,
                    help="destination IP")
parser.add_argument("--port",
                    dest="UDP_PORT",
                    required=True,
                    help="destination port")

p = parser.parse_args()

UDP_IP = p.UDP_IP
UDP_PORT = int(p.UDP_PORT)
in_file = p.in_file

my_ip = socket.gethostbyname(socket.getfqdn())

print("server has started")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:

    f = open(in_file)

    str_json = f.read()

    print(str_json)

    print("UDP target IP:", UDP_IP)
    print("UDP target port:", UDP_PORT)

    ret = sock.sendto(bytes(str_json, "utf-8"),(UDP_IP, UDP_PORT))

    print("Sended:", ret)

    print("_______________________________")

    time.sleep(0.5)