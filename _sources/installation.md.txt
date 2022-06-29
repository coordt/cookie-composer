# Installation

## Installing with pipx

```{note}
This is the recommended method for installing cookie composer because it works on all platforms and should require minimal effort.
```

`pipx` is a tool to help you install and run end-user applications written in Python. It's roughly similar to macOS's `brew`, JavaScript's `npx`, and Linux's `apt`. `pipx` installs the application in an isolated Python environment yet still makes the app available in your shell.

### Install pipx

The full instructions for installing `pipx` are on its [website](https://pypa.github.io/pipx/installation/).

### Install cookie composer

With `pipx` installed, install `cookie-composer` by running:

```console
$ pipx install cookie-composer
```

### Using cookie composer

The `cookie-composer` command is available in your shell as any other command.


## Installing into a Python virtual environment

```{note}
Installing cookie composer into a Python virtual environment, also known as a virtualenv or venv, means the command is only available while that environment is active.
```

```{note}
The instructions assume you already have Python installed.
```

### Create the virtual environment

The full documentation on creating [virtual environments](https://docs.python.org/3.10/library/venv.html#creating-virtual-environments) gives a greater set of instructions. It will be something like running:

```console
$ python3 -m venv /path/to/new/virtual/environment
```

### Activate the virtual environment

The method of activating the environment depends on the shell and are listed in the [documentation](https://docs.python.org/3.10/library/venv.html#creating-virtual-environments). For bash or zsh it is:

```console
$ source </path/to/new/virtual/environment>/bin/activate
```

### Install cookie composer

Once the virtual environment is activate, use [`pip`](https://pip.pypa.io) to install `cookie-composer`:

```console
$ python3 -m pip install cookie-composer
```
