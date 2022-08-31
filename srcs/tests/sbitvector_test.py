#! /usr/bin/env python3

"""SignedBitvectorType のテスト
:file sbitvector_test.py
:author Yusuke Matsunaga (松永 裕介)
:copyright (C) 2021 Yusuke Matsunaga, All rights reserved.
"""

import pytest
from rtlgen import BitType
from rtlgen import SignedBitVectorType


@pytest.fixture()
def sbv20():
    return SignedBitVectorType(20)


def test_signedbitvector_type(sbv20):
    assert not sbv20.is_bit_type
    assert not sbv20.is_bitvector_type
    assert sbv20.is_signedbitvector_type
    assert not sbv20.is_array_type
    assert not sbv20.is_record_type


def test_signedbitvector_size(sbv20):
    assert sbv20.size == 20


def test_signedbitvector_eq1(sbv20):
    type1 = SignedBitVectorType(20)
    assert type1 == sbv20


def test_signedbitvector_ew2(sbv20):
    type1 = SignedBitVectorType(10)
    assert type1 != sbv20


def test_signedbitvector_eq3(sbv20):
    type1 = BitType()
    assert type1 != sbv20
