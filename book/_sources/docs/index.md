# [cvxFin](https://tschm.github.io/cvxFin/book)

![Apache 2.0 License](https://img.shields.io/badge/License-APACHEv2-brightgreen.svg)
[![CodeFactor](https://www.codefactor.io/repository/github/tschm/cvxFin/badge)](https://www.codefactor.io/repository/github/tschm/cvxFin)

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/tschm/cvxFin)

I have decided to continue this project with cvxpy rather than cvxopt. test

## uv

Starting with

```bash
make install
```

will install [uv](https://github.com/astral-sh/uv) and create
the virtual environment defined in
pyproject.toml and locked in uv.lock.

## marimo

We install [marimo](https://marimo.io) on the fly within the aforementioned
virtual environment. Executing

```bash
make marimo
```

will install and start marimo.
