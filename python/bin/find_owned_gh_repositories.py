#!/usr/bin/env python3

import argparse
import csv
import getpass
import logging
import os
import sys
from github import Github


def check_codeowners(repo, team):
    try:
        content = repo.get_contents(".github/CODEOWNERS").decoded_content.decode()
    except Exception:
        logging.exception("Exception caught while getting content of CODEOWNERS")
        return "no codeowners"
    logging.debug("CODEOWNERS")
    logging.debug("%s", content)
    if team.name.lower().replace(" ", "-") in content:
        ans = True
    else:
        ans = False
    return str(ans)


def get_repos(team):
    fields = ["name", "html_url", "in_codeowners", "archived"]
    writer = csv.DictWriter(sys.stdout, fieldnames=fields)
    writer.writeheader()
    for repo in team.get_repos():
        data = {
            "name": repo.name,
            "html_url": repo.html_url,
            "in_codeowners": check_codeowners(repo, team),
            "archived": repo.archived,
        }
        writer.writerow(data)


def find_repos(args):
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        token = getpass.getpass("Enter Github PAT: ")
    gh = Github(token)  # pylint: disable=invalid-name
    org = gh.get_organization(args.org)
    for tm in org.get_teams():  # pylint: disable=invalid-name
        logging.debug("Checking team name: %s", tm.name)
        if tm.name.lower() == args.team.lower():
            get_repos(tm)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("org", metavar="ORG", help="Org to look fir owners in")
    parser.add_argument("team", metavar="TEAM", help="Team to pull repositories for")
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Turn on debugging output"
    )
    args = parser.parse_args()  # just want the help

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.getLogger().addHandler(logging.NullHandler())

    find_repos(args)


if __name__ == "__main__":
    sys.exit(main())
