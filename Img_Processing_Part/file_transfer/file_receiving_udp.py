import socket
import json
import argparse
from pathlib import Path

# python file_receiving_udp.py --ip 192.168.43.26 --port 5001 

parser = argparse.ArgumentParser(description='Receiving JSON data through UDP')
parser.add_argument("--file",
                    dest="out_file",
                    required=False,
                    default="json_rcv_output_file.json",
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
out_file = p.out_file

out_file = "json_output_GM.json" #for demo, using GM car park image

in_file_name = "json_output_"
in_file_ext = ".json"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(2048)
    data = str(data.decode('utf-8'))

    if data.startswith('{') :#json
        json_obj = json.loads(data)
        with open(out_file,'w+') as outfile:
            json.dump(json_obj,outfile)
            print("json file written")

    else: #app request
        file_name = in_file_name+data+in_file_ext

        t = file_name.maketrans("\n\t\r", "   ")
        file_name = file_name.translate(t)
        
        print(file_name)
        response = "["

        if Path(file_name).is_file():
            json_file = open(file_name)
            out = json.load(json_file)
            for i in range(len(out)):
                j = i+1
                info = out[str(j)]
                free = info['free']
                if free == 'True':
                    response = response + str(j) + ","
            response = response[:-1]
            json_file.close()
        
        response = response + "]"
        ret = sock.sendto(bytes(response, "utf-8"),addr)
