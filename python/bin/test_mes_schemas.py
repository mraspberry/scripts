#!/usr/bin/env python3

import argparse
import json
import pathlib
import random
import string

import exrex
import requests


def load_schema(schema_path):
    return json.loads(schema_path.read_text())


def get_enum_val(definition):
    return random.choice(definition["enum"])


def get_pattern_val(definition):
    return exrex.getone(definition["pattern"])


def get_val(definition):
    if definition["type"] != "string":
        raise ValueError(f"Can't handle type: {definition['type']}")
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


def add_vals_to_payload(payload, keys, properties):
    for key in keys:
        payload[key] = get_val(properties[key])


def gen_test_payloads(schema):
    required = frozenset(schema["required"])
    payload = dict()
    not_required = required.difference(schema["properties"].keys())
    add_vals_to_payload(payload, required, schema["properties"])
    yield (payload, "required_fields_only")
    if not_required:
        add_vals_to_payload(payload, not_required, schema["properties"])
    yield (payload, "not-required_fields_included")


def test_schema(schema_path, env_prefix):
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
        resp = requests.post(
            f"https://service.{env_prefix}lampogroup.net/marketing-event/events",
            json=data,
            headers=headers,
        )
        try:
            resp.raise_for_status()
        except Exception as err:  # pylint: disable=broad-except
            print(f"{schema_path} ... FAILED: {err}")
        else:
            if resp.json().get("kinesis_sequence_number"):
                msg = f"{schema_path.name}::{name:30} ... OK"
            else:
                msg = f"{schema_path.name}::{name:30} .. FAILED: No kinesis_sequence_number"
            print(msg)


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
    args = parser.parse_args()

    for fn in args.schemas:  # pylint: disable=invalid-name
        prefix = args.env + "."
        try:
            test_schema(pathlib.Path(fn), prefix)
        except Exception as err:  # pylint: disable=broad-except
            print(f"{fn} ... ERROR: {err}")
            continue


if __name__ == "__main__":
    main()
