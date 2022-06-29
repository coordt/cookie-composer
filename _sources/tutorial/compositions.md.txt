# Building a project from a composition

Do the same thing as incrementally layering, but use a composition to alleviate the issues.

Issues to resolve:

- similar prompts
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

## Create a base composition

A composition is a series of template layers. We can reproduce the results of the [previous tutorial](incrementally-layering.md) using this file: 

```{literalinclude} /_includes/tutorial-composition-1.yaml
---
language: yaml
linenos:
name: tutorial-composition-1-yaml
caption: my-package-composition.yaml
---
```

We didn't change the default for the `project_slug`, `topics` or `open_source_license` prompts. You don't have to change all the prompts or include all the prompts in the composition.

Then run:

```console
$ cookie-composer create /path/to/my-package-composition.yaml

full_name [rwxd]: Demo User
email [rwxd@pm.me]: demo_user@example.com
github_username [rwxd]: demo_user
project_name [Python Boilerplate]: Cookie Composer Demo
project_slug [composer_demo]:
project_short_description [Python Boilerplate contains all the boilerplate you need to create a Python package.]: Cookie Composer Demo
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
author_name [Louis Taylor]: Demo User
author_email [louis@kragniz.eu]: demo_user@example.com
package_name [cookiecutter_pypackage_minimal]: composer_demo
package_version [0.1.0]:
package_description [An opinionated, minimal cookiecutter template for Python packages]: Cookie Composer Demo
package_url [https://github.com/kragniz/cookiecutter-pypackage-minimal]: https://github.com/demo_user/composer_demo
readme_pypi_badge [True]:
readme_travis_badge [True]:
readme_travis_url [https://travis-ci.org/kragniz/cookiecutter-pypackage-minimal]: https://travis-ci.org/demouser/composer_demo
```

Both layers are applied without requiring a git repository or multiple commands.

## Providing better defaults

The composition can also improve the defaults for the template prompts by:

- Providing new defaults that work better for your use case.
- Using a default from a previous template.

Let's start by changing some defaults to the first template. You can find the original prompt in this template's [cookiecutter.json file.](https://github.com/rwxd/cookiecutter-github-project/blob/main/cookiecutter.json)

```{literalinclude} /_includes/tutorial-composition-2.yaml
---
language: yaml
linenos:
name: tutorial-composition-2-yaml
caption: my-package-composition.yaml
---
```

The new defaults provide better suggestions based on previous prompt answers.

## Using values from previous templates

The second template has several prompts that simply synonymns of promts from the previous template. It would be nice if we could use our answers from that template here.

Let's do that. You can find the original prompts in this template's [cookiecutter.json file.](https://github.com/kragniz/cookiecutter-pypackage-minimal/blob/master/cookiecutter.json)

```{literalinclude} /_includes/tutorial-composition-3.yaml
---
language: yaml
linenos:
name: tutorial-composition-3-yaml
caption: my-package-composition.yaml
---
```

Now:

- `author_name` defaults to `full_name`'s value
- `author_email` defaults to `email`'s value
- `package_name` defaults to `project_slug`'s value
- `package_description` defaults to `project_short_description`'s value
- `package_url` references both `github_username`'s and `project_slug`'s values

## Putting it into action

```console
$ cookie-composer create /path/to/tutorial-composition-3.yaml

full_name [Your Name]: Demo User
email [demo_user@example.com]:
github_username [demo_user]:
project_name [Python Boilerplate]: Composer Demo
project_slug [composer_demo]:
project_short_description []: Cookie Composer Demo
homepage [https://demo_user.github.io/composer_demo]:
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
author_name [Demo User]:
author_email [demo_user@example.com]:
package_name [composer_demo]:
package_version [0.1.0]:
package_description [Cookie Composer Demo]:
package_url [https://github.com/demo_user/composer_demo]:
readme_pypi_badge [True]:
readme_travis_badge [False]:
readme_travis_url []:
```

Notice how the better defaults allow less typing and more consistency.
