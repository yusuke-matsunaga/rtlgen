#! /usr/bin/env python3

"""ArrayTypeのテスト
:file array_test.py
:author Yusuke Matsunaga (松永 裕介)
:copyright (C) 2021 Yusuke Matsunaga, All rights reserved.
"""

import pytest
from rtlgen import BitType
from rtlgen import BitVectorType
from rtlgen import ArrayType


@pytest.fixture()
def barray10():
    bit_type = BitType()
    return ArrayType(bit_type, 10)


def test_array_type(barray10):
    assert not barray10.is_bit_type
    assert not barray10.is_bitvector_type
    assert not barray10.is_signedbitvector_type
    assert barray10.is_array_type
    assert not barray10.is_record_type


def test_array_subtype(barray10):
    assert barray10.subtype == BitType()


def test_array_size(barray10):
    assert barray10.size == 10


def test_bitvector_eq1(barray10):
    bit_type = BitType()
    type1 = ArrayType(bit_type, 10)
    assert type1 == barray10


def test_bitvector_eq2(barray10):
    bv_type = BitVectorType(10)
    type1 = ArrayType(bv_type, 10)
    assert type1 != barray10


def test_bitvector_eq3(barray10):
    bit_type = BitType()
    type1 = ArrayType(bit_type, 20)
    assert type1 != barray10
