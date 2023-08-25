# -*- coding: utf-8 -*-
"""
Global fixtures
"""
from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture(scope="session", name="resource_dir")
def resource_fixture():
    return Path(__file__).parent / "resources"
