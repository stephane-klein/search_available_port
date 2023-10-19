#!/usr/bin/env python3
import os
import json
import argparse
import fcntl

parser = argparse.ArgumentParser(description="Remove instance in state file")
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

    if args.name in state_dict:
        del state_dict[args.name]

        with open(args.state_file, "w") as writer:
            writer.write(json.dumps(state_dict, indent=4))

        print("state file updated")
    else:
        print("instance not found in state file, no change made")

    fcntl.flock(lock_file, fcntl.LOCK_UN)
