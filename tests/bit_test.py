#! /usr/bin/env python3

"""BitTypeのテスト
:file bit_test.py
:author Yusuke Matsunaga (松永 裕介)
:copyright (C) 2021 Yusuke Matsunaga, All rights reserved.
"""

import pytest
from rtlgen import DataType


@pytest.fixture
def bit_type():
    return DataType.bit_type()


def test_bit_root_type(bit_type):
    assert bit_type.is_bit_type
    assert not bit_type.is_bitvector_type
    assert not bit_type.is_signedbitvector_type
    assert not bit_type.is_array_type
    assert not bit_type.is_record_type


def test_bit_eq1(bit_type):
    type1 = DataType.bit_type()
    assert type1 == bit_type


def test_bit_eq2(bit_type):
    type1 = DataType.bitvector_type(10)
    assert type1 != bit_type
