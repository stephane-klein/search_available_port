#!/usr/bin/env python3
import os
import json
import argparse
import socket
import fcntl

parser = argparse.ArgumentParser(description="Search available port")
parser.add_argument(
    "--from",
    required=True,
    type=int,
    dest="_from",
    help="Search from this port"
)
parser.add_argument(
    "--name",
    required=True,
    type=str,
    dest="name",
    help="Instance name"
)

parser.add_argument(
    "--state",
    required=True,
    type=str,
    dest="state_file",
    help="State file"
)

args = parser.parse_args()

with open(args.state_file + ".lock", 'w') as lock_file:
    fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)

    state_dict = {}
    if os.path.exists(args.state_file):
        with open(args.state_file, "r") as reader:
            state_dict = json.loads(reader.read())

    available_port = None
    reserved_ports = state_dict.values()
    for port in range(int(args._from), int(args._from) + 400):
        if port not in reserved_ports:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                res = sock.connect_ex(("localhost", port))
                if res != 0:
                    print("Free port: %s" % port)
                    available_port = port
                    break

    state_dict[args.name] = available_port

    with open(args.state_file, "w") as writer:
        writer.write(json.dumps(state_dict, indent=4))

    fcntl.flock(lock_file, fcntl.LOCK_UN)

print("%s updated" % args.state_file)
