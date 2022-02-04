#!/usr/bin/env python3
"""Find github repos matching specified criteria"""

import argparse
import os
from github import Github


def find_repos(args):
    token = os.getenv("GH_TOKEN", "")
    if not token:
        sys.exit("Must set GH_TOKEN environment variable\n")
    gh = Github(token)
    org = gh.get_organization(args.org)
    langs = [l.lower() for l in args.language]

    for repo in org.get_repos():
        if langs:
            # have to call str because sometimes this is None
            if str(repo.language).lower() in langs:
                print(repo.full_name)
        else:
            print(repo.full_name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l",
        "--language",
        action="append",
        help="Only show repositories for the specified language",
    )
    parser.add_argument(
        "org", metavar="ORGANIZATION", help="Organization to find repositories in"
    )
    args = parser.parse_args()

    find_repos(args)


if __name__ == "__main__":
    main()
