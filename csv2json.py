#!/usr/bin/env python3

import csv
import json
import sys
from argparse import ArgumentParser

def csv2json(filename, outfn):
    info = list()
    with open(filename) as fd:
        reader = csv.DictReader(fd)
        for row in reader:
            info.append(row)
    if outfn == '-':
        print(json.dumps(info, indent=2))
    else:
        print('Writing', outfn)
        with open(outfn, 'w') as wfd:
            json.dump(info, wfd, indent=2)

def main():
    parser = ArgumentParser(description='Convert csv file to json')
    parser.add_argument('csvfile', metavar='FILENAME', help='CSV file to convert')
    parser.add_argument('outputfile', metavar='FILENAME', help="Output file. '-' can be specified for STDOUT")
    args = parser.parse_args()

    csv2json(args.csvfile, args.outputfile)

if __name__ == '__main__':
    main()
