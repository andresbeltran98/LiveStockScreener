#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from screener.skeleton import fib

__author__ = "Andres Beltran"
__copyright__ = "Andres Beltran"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
