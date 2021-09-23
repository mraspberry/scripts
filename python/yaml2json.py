#!/usr/bin/env python

import argparse
import json
import yaml


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "yamlfp",
        metavar="FILENAME",
        type=argparse.FileType(),
        help="YAML file to convert to JSON. Can be '-' for STDIN",
    )
    parser.add_argument(
        "jsonfp",
        metavar="FILENAME",
        type=argparse.FileType("w"),
        help="File to output JSON to. Can be '-' for STDOUT",
    )
    args = parser.parse_args()

    with args.yamlfp, args.jsonfp:
        json.dump(yaml.safe_load(args.yamlfp), args.jsonfp, indent=2)


if __name__ == "__main__":
    main()
