#!/usr/bin/env python3

import argparse
import pandas


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filenames", metavar="FILENAME", nargs="+", help="Files to merge"
    )
    args = parser.parse_args()

    print(
        pandas.concat(map(pandas.read_csv, args.filenames), ignore_index=True).to_csv()
    )


if __name__ == "__main__":
    main()
