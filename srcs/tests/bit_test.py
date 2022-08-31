#! /usr/bin/env python3

"""BitTypeのテスト
:file bit_test.py
:author Yusuke Matsunaga (松永 裕介)
:copyright (C) 2021 Yusuke Matsunaga, All rights reserved.
"""

import pytest
from rtlgen import BitType
from rtlgen import BitVectorType


@pytest.fixture
def bit_type():
    return BitType()


def test_bit_root_type(bit_type):
    assert bit_type.is_bit_type
    assert not bit_type.is_bitvector_type
    assert not bit_type.is_signedbitvector_type
    assert not bit_type.is_array_type
    assert not bit_type.is_record_type


def test_bit_eq1(bit_type):
    type1 = BitType()
    assert type1 == bit_type


def test_bit_eq2(bit_type):
    type1 = BitVectorType(10)
    assert type1 != bit_type
