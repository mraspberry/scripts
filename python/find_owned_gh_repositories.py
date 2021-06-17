#!/usr/bin/env python3

import argparse
import csv
import getpass
import os
import sys
from github import Github


def get_repos(team):
    fields = ["name", "html_url", "archived"]
    writer = csv.DictWriter(sys.stdout, fieldnames=fields)
    writer.writeheader()
    for repo in team.get_repos():
        data = {"name": repo.name, "html_url": repo.html_url, "archived": repo.archived}
        writer.writerow(data)


def find_repos(args):
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        token = getpass.getpass("Enter Github PAT: ")
    gh = Github(token)  # pylint: disable=invalid-name
    org = gh.get_organization(args.org)
    for tm in org.get_teams():  # pylint: disable=invalid-name
        if tm.name.lower() == args.team.lower():
            get_repos(tm)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("org", metavar="ORG", help="Org to look fir owners in")
    parser.add_argument("team", metavar="TEAM", help="Team to pull repositories for")
    args = parser.parse_args()  # just want the help

    find_repos(args)


if __name__ == "__main__":
    sys.exit(main())
