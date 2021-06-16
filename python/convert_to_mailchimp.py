#!/usr/bin/env python3

import csv
import sys
from argparse import ArgumentParser


def make_mailchimp(infile, outfd=sys.stdout):
    with open(infile, newline="") as fd:
        reader = csv.DictReader(fd)
        writer = csv.DictWriter(outfd, ("Email Address", "First Name", "Last Name"))
        writer.writeheader()
        for row in reader:
            outdict = dict()
            outdict["Email Address"] = row["Email"]
            outdict["First Name"] = row["First Name"]
            outdict["Last Name"] = row["Last Name"]
            writer.writerow(outdict)


def main():
    parser = ArgumentParser(
        description="Take CSV from SimpleChurch and convert to MailChimp"
    )
    parser.add_argument("filename", metavar="FILENAME", help="Filename to convert")
    parser.add_argument("-o", "--outfile", help="Output file (default STDOUT)")
    args = parser.parse_args()

    if args.outfile:
        outfd = open(outfile, "w", newline="")
    else:
        outfd = sys.stdout

    make_mailchimp(args.filename, outfd)


if __name__ == "__main__":
    main()
