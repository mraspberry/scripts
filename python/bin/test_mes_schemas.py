#!/usr/bin/env python3

import argparse
import json
import logging
import pathlib
import random
import string
from datetime import datetime

import exrex
import requests


def load_schema(schema_path):
    return json.loads(schema_path.read_text())


def get_enum_val(definition):
    return random.choice(definition["enum"])


def get_pattern_val(definition):
    return exrex.getone(definition["pattern"])


def get_int_val(*unused):
    return random.randint(1, 1000000)


def get_str_val(definition):
    if definition.get("enum"):
        val = get_enum_val(definition)
    elif definition.get("pattern"):
        val = get_pattern_val(definition)
    else:
        val = "".join(
            [
                random.choice(string.ascii_letters)
                for i in range(int(definition["minLength"]))
            ]
        )
    return val


def get_val(definition):
    val_type = definition["type"].lower()
    mapper = {
        "string": get_str_val,
        "integer": get_int_val,
    }
    if val_type not in mapper.keys():
        raise ValueError(f"Can't handle type: {val_type}")
    return mapper[val_type](definition)


def get_email(*unused):
    return "test_mes_schema@notarealaddress.com"


def get_occurred_at(*unused):
    return f"{datetime.utcnow():%Y-%m-%dT%H:%M:%S.%f}Z"


def add_vals_to_payload(payload, keys, properties):
    mapper = {
        "email": get_email,
        "occurred_at": get_occurred_at,
    }
    for key in keys:
        if "datetime" in key:
            payload[key] = get_occurred_at()
            continue
        func = mapper.get(key.lower(), get_val)
        payload[key] = func(properties[key])


def gen_test_payloads(schema):
    required = frozenset(schema["required"])
    payload = dict()
    not_required = required.difference(schema["properties"].keys())
    add_vals_to_payload(payload, required, schema["properties"])
    yield (payload, "required_fields_only")
    if not_required:
        add_vals_to_payload(payload, not_required, schema["properties"])
    yield (payload, "not-required_fields_included")


def test_schema(schema_path, env_prefix, show_payload, dry_run):
    schema = load_schema(schema_path)
    data = dict()
    schema_noext = schema_path.name.rstrip(".json")
    uri_dir = "{}/{}".format(schema_path.absolute().parent.name, schema_noext)
    uri_fn = f"{schema_noext}-{schema['$version']}.json"
    data["event_type"] = get_val(schema["properties"]["event_name"])
    data["schema_uri"] = f"schemas/{uri_dir}/{uri_fn}"
    headers = {
        "X-Request-Id": "TXID+01234567890123456789",
        "Content-Type": "application/json",
    }
    for (payload, name) in gen_test_payloads(schema):
        data["payload"] = payload
        if show_payload:
            print(json.dumps(data, indent=2))
        if dry_run:
            continue
        resp = requests.post(
            f"https://service.{env_prefix}lampogroup.net/marketing-event/events",
            json=data,
            headers=headers,
        )
        try:
            resp.raise_for_status()
        except Exception as err:  # pylint: disable=broad-except
            print(f"{schema_path} ... FAILED: {err}")
        print(f"{schema_path.name}::{name:30} ... OK")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "env",
        metavar="ENVIRONMENT",
        choices=("test", "qa"),
        help="Domain prefix for the environment",
    )
    parser.add_argument(
        "schemas", metavar="SCHEMA_FILE", nargs="+", help="Schemas to test"
    )
    parser.add_argument(
        "-s", "--show-payload", action="store_true", help="Print the generated payload"
    )
    parser.add_argument(
        "-d", "--dry-run", action="store_true", help="Don't actually make a request"
    )
    parser.add_argument("--debug", action="store_true", help="Turn on debugging")
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    for fn in args.schemas:  # pylint: disable=invalid-name
        prefix = args.env + "."
        try:
            test_schema(pathlib.Path(fn), prefix, args.show_payload, args.dry_run)
        except Exception as err:  # pylint: disable=broad-except
            print(f"{fn} ... ERROR: {err}")
            continue


if __name__ == "__main__":
    main()
