#!/usr/bin/env python3

import argparse
import json
import pathlib
import sys


def process_json(jsonobj):
    # not returning anything since args are mutable by reference
    if isinstance(jsonobj, list):
        process_list(jsonobj)
    elif isinstance(jsonobj, dict):
        process_dict(jsonobj)


def string_json(val):
    if isinstance(val, str):
        try:
            parsed = json.loads(val)
        except Exception:
            return None
        else:
            return parsed


def process_list(jsonobj):
    for index, item in enumerate(jsonobj):
        parse_attempt = string_json(item)
        if parse_attempt is not None:
            jsonobj[index] = parse_attempt
            process_json(parse_attempt)
        process_json(jsonobj[index])  # handles lists and dicts


def process_dict(jsonobj):
    for key in jsonobj:
        parse_attempt = string_json(jsonobj[key])
        if parse_attempt is not None:
            jsonobj[key] = parse_attempt
        process_json(jsonobj[key])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=pathlib.Path, help="Input JSON file")
    parser.add_argument(
        "-i",
        "--inplace",
        action="store_true",
        help="Modify the input file inplace instead of outputting to STDOUT",
    )
    args = parser.parse_args()

    try:
        loaded = json.loads(args.infile.read_text())
    except json.JSONDecodeError:
        sys.exit(f"Unable to parse JSON from {args.infile.name}\n")
    process_json(loaded)
    if args.inplace:
        print("Modifying", args.infile, "in place")
        args.infile.write_text(json.dumps(loaded, indent=2))
    else:
        print(json.dumps(loaded, indent=2))


if __name__ == "__main__":
    main()
