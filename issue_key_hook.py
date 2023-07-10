#!/usr/bin/env python

import re
import subprocess
import sys


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
    def __init__(self, branch_name):
        self.branch_name = branch_name

    @property
    def issue_id(self):
        project_format = "[A-Z][A-Z]+"
        issue_pattern = f"{project_format}-[\d]+"
        match = re.search(issue_pattern, self.branch_name)
        return match.group() if match else None

    @classmethod
    def fetch_current_branch_name(cls):
        try:
            return cls(
                subprocess.check_output("git symbolic-ref HEAD", shell=True)
                .decode()
                .strip()[11:]
            )
        except subprocess.CalledProcessError:
            print("Error: Unable to append issue ID. Are you in detached HEAD state?")
            sys.exit()


def add_issue_key():
    file_path = sys.argv[1]  # The commit message file passed as a command-line argument
    message_manager = CommitMessageFile(file_path)
    issue_id = BranchName.fetch_current_branch_name().issue_id

    if issue_id:
        original_message = message_manager.read_message()
        user_message = UserMessage(original_message)
        if user_message and issue_id not in user_message:
            message_manager.write_message(CommitMessage(issue_id, user_message))


if __name__ == "__main__":
    add_issue_key()
