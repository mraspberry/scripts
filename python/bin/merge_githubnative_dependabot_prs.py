#!/usr/bin/env python3

import argparse
import getpass
import os
import sys
from github import Github
from github.GithubException import GithubException


def close_pr(pull_req):
    print("Closing", pull_req.html_url)
    pull_req.edit(state="closed")


def merge_native_dependabot_pr(pull_req):
    if pull_req is None:
        return
    if not pull_req.mergeable:
        print("WARNING: Unable to merge", pull_req.html_url, file=sys.stderr)
        return
    print("Merging", pull_req.html_url)
    try:
        pull_req.merge(merge_method="squash")
    except GithubException:
        print("WARNING: Unable to merge", pull_req.html_url, file=sys.stderr)


def find_dependabot_prs(repo):
    native = None
    other = list()
    for req in repo.get_pulls(state="open"):
        branch = req.head.ref
        if branch.startswith("dependabot"):
            if branch.endswith("add-v2-config-file"):
                native = req
            else:
                other.append(req)

    return (native, other)


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
        (native_dpb_pr, other_dpb_prs) = find_dependabot_prs(gh_repo)
        # for req in other_dpb_prs:
        # close_pr(req)
        merge_native_dependabot_pr(native_dpb_pr)


if __name__ == "__main__":
    main()
