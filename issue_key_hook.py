#!/usr/bin/env python

import argparse
from collections.abc import Container
import re
import subprocess
import sys
import typing


class UserMessage:
    GIT_EDITOR_MSG = "# Please enter the commit message for your changes."

    def __init__(self, user_message) -> None:
        self.user_message = user_message

    def _trim_git_editor_message(self, message):
        return message.split(self.GIT_EDITOR_MSG)[0].rstrip()

    def __contains__(self, value):
        return value in self.user_message

    def __str__(self) -> str:
        return self._trim_git_editor_message(self.user_message)

    def __bool__(self) -> bool:
        return bool(self.user_message)


class CommitMessage:
    COMMIT_MSG_TEMPLATE = "{issue_id} {user_message}"
    GIT_EDITOR_MSG = "# Please enter the commit message for your changes."

    def __init__(self, issue_id, user_message) -> None:
        self.issue_id = issue_id
        self.user_message = user_message

    def __str__(self):
        return self.COMMIT_MSG_TEMPLATE.format(
            issue_id=self.issue_id, user_message=str(self.user_message)
        )


class CommitMessageFile:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_message(self):
        with open(self.file_path, "r") as file:
            return file.read()

    def write_message(self, message: CommitMessage):
        with open(self.file_path, "w") as file:
            file.write(str(message))


class BranchName:
    def __init__(self, branch_name: str):
        self.branch_name = branch_name

    def get_issue_id(self, pattern: str):
        match = re.search(pattern, self.branch_name)
        return match.group() if match else None

    def is_ignored(self, ignored_names: Container) -> bool:
        return self.branch_name in ignored_names

    @classmethod
    def fetch_current_branch_name(cls):
        try:
            return cls(
                subprocess.check_output("git symbolic-ref HEAD", shell=True)
                .decode()
                .strip()[11:],
            )
        except subprocess.CalledProcessError:
            print("Error: Unable to append issue ID. Are you in detached HEAD state?")
            sys.exit()


def add_issue_key(
    commit_msg_file: str, pattern: str, required: bool, ignore: Container
):
    message_manager = CommitMessageFile(commit_msg_file)
    branch = BranchName.fetch_current_branch_name()

    def exit(exitmsg: typing.Optional[str]):
        if required:
            sys.exit(exitmsg)
        else:
            sys.exit(exitmsg)

    if branch.is_ignored(ignore):
        exit(
            "Error: Issue key check skipped as the current branch is on the ignore list. Please use a different branch name if you need to include an issue key."
        )

    issue_id = branch.get_issue_id(pattern)
    if not issue_id:
        exit(
            "Error: Unable to locate an Issue Key in the branch name. Please ensure that your branch name includes a valid Issue Key according to the specified pattern."
        )

    original_message = message_manager.read_message()
    user_message = UserMessage(original_message)
    if user_message and issue_id not in user_message:
        message_manager.write_message(CommitMessage(issue_id, user_message))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Issue key pre commit",
        description="A pre-commit hook to add issue key to the commit message",
    )
    parser.add_argument("commit_msg_file", help="Path to the commit message file")
    parser.add_argument(
        "--pattern",
        "-p",
        type=str,
        help="issue key pattern",
        default="[A-Z][A-Z]+-[\d]+",
    )
    parser.add_argument(
        "--required",
        "-r",
        action="store_true",
        help="fail if branch name does not contain the issue key according to the pattern",
    )
    parser.add_argument(
        "--ignore",
        "-i",
        nargs="+",
        default=["dev", "develop", "master", "main", "stage", "staging"],
        help="ignored branch names",
        type=set,
    )
    args = parser.parse_args()
    add_issue_key(args.commit_msg_file, args.pattern, args.required, args.ignore)
