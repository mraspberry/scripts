#!/usr/bin/env python3

import argparse
import getpass
import os
import sys
from github import Github
from github.GithubException import GithubException


def open_pr(ref, prs):
    branch = ref.ref.replace("refs/heads/", "")
    for req in prs:
        if req.head.ref == branch:
            return True
    return False


def delete_dependabot_refs(repo):
    prs = tuple(repo.get_pulls(state="open"))
    for ref in repo.get_git_refs():
        if not open_pr(ref, prs) and "dependabot" in ref.ref:
            print(ref.ref)


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
        delete_dependabot_refs(gh_repo)


if __name__ == "__main__":
    main()
