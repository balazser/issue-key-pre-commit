# Issue Key Pre-Commit Plugin

This Python script serves as a plugin for pre-commit, a multi-language package manager for pre-commit hooks. It adds issue keys (as extracted from the branch name) to the commit message, improving the traceability of commits by associating them with related issue keys and making it easier to track changes across branches and tasks.

## Features

- Extracts issue keys from the branch name using regular expressions.
- Automatically adds issue keys to commit messages.
- Optionally fails the commit when the branch name doesn't match a certain pattern.
- Supports ignoring specific branch names.

## Installation

This pre-commit hook can be installed by adding it to your pre-commit config file (.pre-commit-config.yaml). Here's an example of what the entry might look like:

```yaml
repos:
  - repo: https://gitlab.com/rentouch-public/issue-key-pre-commit
    rev: v1.0.0 # Use the ref you want to point at
    hooks:
      - id: issue-key
        args: ["-p", "BUG-[\\d]+", "-r", "-i", ["dev", "master"]]
```

Please replace `v1.0.0` with the tag/commit you want to use.

## Usage

The tool will run automatically when a commit is made if it has been correctly set up in your pre-commit configuration. However, you can customize its behavior using the following arguments:

- `-p, --pattern`: Pattern to match the issue key in the branch name. The default is `[A-Z][A-Z]+-[\d]+`.
- `-r, --required`: If provided, the script will fail if the branch name doesn't contain the issue key according to the pattern.
- `-i, --ignore`: List of ignored branch names. Defaults to `["dev", "develop", "master", "main", "stage", "staging"]`.

## Dependencies

This plugin requires Python 3.6 or newer. It does not have any external Python dependencies.

## Known Limitations

This script does not support branches in a detached HEAD state.

## Contributing

If you find a bug or think of a feature, feel free to create an issue or a merge request. All contributions are welcome!

## Author

Balazs Erdos - balazs.erdos@scaledagile.com

## License

This plugin is available under the [MIT License](https://opensource.org/licenses/MIT).
