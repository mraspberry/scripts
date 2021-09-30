#!/usr/bin/env python3

import argparse
import getpass
import os
import sys
from github import Github
from github.GithubException import GithubException


def check_dependabot(repo):
    paths = {
        "native": ".github/dependabot.yml",
        "legacy": ".dependabot/config.yml",
    }
    for ver, path in paths.items():
        try:
            _ = repo.get_contents(path)
        except GithubException:
            pass
        else:
            return ver
    else:
        return None


def _get_token():
    return os.getenv("GH_TOKEN", "") or getpass.getpass("Enter Github token: ")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "repos",
        nargs="+",
        metavar="OWNER/REPOSITORY",
        help="Repository(s) to merge GH native dependabot PR on",
    )
    args = parser.parse_args()
    github = Github(_get_token())
    for repo in args.repos:
        gh_repo = github.get_repo(repo)
        dpb_version = check_dependabot(gh_repo)
        print(f"{repo}: {str(dpb_version).upper()}")


if __name__ == "__main__":
    main()
