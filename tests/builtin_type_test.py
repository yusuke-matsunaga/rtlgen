#! /usr/bin/env python3

"""BuiltinType のテスト
:file builtin_type_test.py
:author Yusuke Matsunaga (松永 裕介)
:copyright (C) 2021 Yusuke Matsunaga, All rights reserved.
"""

from rtlgen.data_type import BuiltinType


def test_bit_str():
    assert BuiltinType.BIT.__str__() == 'bit'


def test_bitvector_str():
    assert BuiltinType.BITVECTOR.__str__() == 'bitvector'


def test_signed_bitvector_str():
    assert BuiltinType.SBITVECTOR.__str__() == 'signed_bitvector'


def test_array_str():
    assert BuiltinType.ARRAY.__str__() == 'array'


def test_record_str():
    assert BuiltinType.RECORD.__str__() == 'record'
