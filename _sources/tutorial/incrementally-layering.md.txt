# Building a project layer by layer

## Create a project from a template

https://github.com/rwxd/cookiecutter-github-project
```console
$ cookie-composer create https://github.com/rwxd/cookiecutter-github-project
full_name [rwxd]: Demo User
email [rwxd@pm.me]: demo_user@example.com
github_username [rwxd]: demo_user
project_name [Python Boilerplate]: Composer Demo
project_slug [composer_demo]:
project_short_description [Python Boilerplate contains all the boilerplate you need to create a Python package.]: A Cookie Composer demo
homepage [https://rwxd.github.io/composer_demo/]: https://demo_user.github.io/composer_demo/
Select project_type:
1 - python
2 - go
3 - ansible
4 - other
Choose from 1, 2, 3, 4 [1]:
topics []:
Select open_source_license:
1 - MIT license
2 - BSD license
3 - ISC license
4 - Apache Software License 2.0
5 - GNU General Public License v3
6 - Not open source
Choose from 1, 2, 3, 4, 5, 6 [1]:
```

## Add an Python package layer

```console
$ cd composer_demo
$ cookie-composer add https://github.com/kragniz/cookiecutter-pypackage-minimal
Usage: cookie-composer add [OPTIONS] PATH_OR_URL [DESTINATION]
Try 'cookie-composer add --help' for help.
╭─ Error ─────────────────────────────────────────────────────────────────────────────────────────────────╮
│ Some cookie composer commands only work on git repositories. Please make the destination directory a    │
│ git repo.                                                                                               │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

```console
$ git add -A
$ git commit -m"Initial commit"
[master (root-commit) 90a6a74] Initial commit
 15 files changed, 352 insertions(+)
 create mode 100644 .composition.yaml
 create mode 100644 .github/ISSUE_TEMPLATE/bug_report_md
 create mode 100644 .github/ISSUE_TEMPLATE/config.yml
 create mode 100644 .github/ISSUE_TEMPLATE/feature_request.md
 create mode 100644 .github/dependabot.yml
 create mode 100644 .github/settings.yml
 create mode 100644 .github/workflows/semantic-release.yml
 create mode 100644 .gitignore
 create mode 100644 .pre-commit-config.yaml
 create mode 100644 .releaserc.yml
 create mode 100644 LICENSE
 create mode 100644 Makefile
 create mode 100644 README.md
 create mode 100644 renovate.json
 create mode 100644 requirements-dev.txt
 ```

```console
cookie-composer add https://github.com/kragniz/cookiecutter-pypackage-minimal
author_name [Louis Taylor]: Demo User
author_email [louis@kragniz.eu]: demo_user@example.com
package_name [cookiecutter_pypackage_minimal]: composer_demo
package_version [0.1.0]:
package_description [An opinionated, minimal cookiecutter template for Python packages]: A Cookie Composer demo
package_url [https://github.com/kragniz/cookiecutter-pypackage-minimal]: https://github.com/demo_user/composer_demo
readme_pypi_badge [True]:
readme_travis_badge [True]: 
readme_travis_url [https://travis-ci.org/kragniz/cookiecutter-pypackage-minimal]: https://travis-ci.org/demouser/composer_demo
```

Now on branch `add_layer_cookiecutter-pypackage-minimal`


```console
$ git status
On branch add_layer_cookiecutter-pypackage-minimal
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   .composition.yaml

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	README.rst
	python_boilerplate/
	setup.py
	tests/
	tox.ini
```

The modified `.composition.yaml` file includes the new layer information.

Let's commit the new files

```console
$ git add -A
$ git commit -m"Added layer cookiecutter-pypackage-minimal"
[add_layer_cookiecutter-pypackage-minimal dc62ba1] Added layer cookiecutter-pypackage-minimal
 6 files changed, 115 insertions(+)
 create mode 100644 README.rst
 create mode 100644 python_boilerplate/__init__.py
 create mode 100644 setup.py
 create mode 100644 tests/test_sample.py
 create mode 100644 tox.ini
```

Now the new branch is ready to merge.

```console
$ git checkout master
$ git merge add_layer_cookiecutter-pypackage-minimal
Updating aa3f701..dc62ba1
Fast-forward
 .composition.yaml              | 24 ++++++++++++++++++++++++
 README.rst                     | 32 ++++++++++++++++++++++++++++++++
 python_boilerplate/__init__.py |  5 +++++
 setup.py                       | 44 ++++++++++++++++++++++++++++++++++++++++++++
 tests/test_sample.py           |  4 ++++
 tox.ini                        |  6 ++++++
 6 files changed, 115 insertions(+)
 create mode 100644 README.rst
 create mode 100644 python_boilerplate/__init__.py
 create mode 100644 setup.py
 create mode 100644 tests/test_sample.py
 create mode 100644 tox.ini
$ git branch -d add_layer_cookiecutter-pypackage-minimal
Deleted branch add_layer_cookiecutter-pypackage-minimal (was dc62ba1).
```

3. Show some of the issues when using templates not designed for composition

- similar questions
  - full_name vs. author_name
  - email vs. author_email
  - project_short_description vs. package_description
  - project_slug vs. package_name
  - homepage vs. package_url
- Duplicate files:
  - README.md vs README.rst
  - LICENSE
  - .gitignore
- Unused files
  - .releaserc.yml
  - renovate.json

4. Read [compositions](compositions.md) for ways to improve this.
