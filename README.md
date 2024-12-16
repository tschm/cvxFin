# cvxFin

![Apache 2.0 License](https://img.shields.io/badge/License-APACHEv2-brightgreen.svg)

I have decided to continue this project with cvxpy rather than cvxopt. test

## uv

You need to install [task](https://taskfile.dev).
Starting with

```bash
task cvxFin:install
```

will install [uv](https://github.com/astral-sh/uv) and create
the virtual environment defined in
pyproject.toml and locked in uv.lock.

## marimo

We install [marimo](https://marimo.io) on the fly within the aforementioned
virtual environment. Executing

```bash
task cvxFin:marimo
```

will install and start marimo.
