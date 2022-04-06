# Contribution Guideline

<!-- * Use proper Python 3 Syntax -->
* Follow [PEP8](https://www.python.org/dev/peps/pep-0008/) Python style conventions
* Conform to the following formatting and documentation standards
* Include tests for your code
* Minimize module dependencies
* Ensure that your code is readable

## Minimum Version

This project targets Python 3.10.

## Merge|Pull Requests

* It's the requestor's onus to show that his code is working
* It's the merger's responsibility to be reasonably convinced that the code is working
* Request reviews early into the process, so that proper allocations can be made
* [Disagree and Commit](https://en.wikipedia.org/wiki/Disagree_and_commit)

## Commits

* Commits are to be prefixed with `Add`, `Chg` or `Del`
* Commits are to be written in imperative mood (imagine there's an exclamation mark at
  the end of your commit message)

## autopep8

Autopep8 fixes most of the issues reported by `pylint API/`.

Formatting all .py files in the API/ can be done via:
```bash
find API/ -name '*.py*' -print0 | xargs -0 autopep8 --in-place --aggressive --aggressive
```

Formatting a singular file:

```bash
autopep8 --in-place --aggressive --aggressive ${file:-__init__.py}
```
