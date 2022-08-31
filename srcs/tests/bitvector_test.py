#! /usr/bin/env python3

"""BitvectorType のテスト
:file bitvector_test.py
:author Yusuke Matsunaga (松永 裕介)
:copyright (C) 2021 Yusuke Matsunaga, All rights reserved.
"""

import pytest
from rtlgen import BitType
from rtlgen import BitVectorType


@pytest.fixture()
def bv10():
    return BitVectorType(10)


def test_bitvector_type(bv10):
    assert not bv10.is_bit_type
    assert bv10.is_bitvector_type
    assert not bv10.is_signedbitvector_type
    assert not bv10.is_array_type
    assert not bv10.is_record_type


def test_bitvector_size(bv10):
    assert bv10.size == 10


def test_bitvector_eq1(bv10):
    type1 = BitVectorType(10)
    assert type1 == bv10


def test_bitvector_eq2(bv10):
    type1 = BitVectorType(20)
    assert type1 != bv10


def test_bitvector_eq3(bv10):
    type1 = BitType()
    assert type1 != bv10
