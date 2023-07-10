from setuptools import setup

setup(
    name='issue-key-commit-msg',
    version='1.0.0',
    description='A pre-commit hook to add issue key to the commit message',
    author='Balazs Erdos',
    url='https://github.com/balazser/issue-key-commit-msg',
    py_modules=['issue_key_hook'],
    entry_points={
        'console_scripts': [
            'add-issue-key = issue_key_hook:add_issue_key',
        ],
    },
)

