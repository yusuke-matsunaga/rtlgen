#! /usr/bin/env python3

"""Entity のテスト
:file entity_test.py
:author Yusuke Matsunaga (松永 裕介)
:copyright (C) 2021 Yusuke Matsunaga, All rights reserved.
"""

import pytest
from rtlgen.entity import Entity
from rtlgen import DataType


@pytest.fixture
def bit_type():
    return DataType.bit_type()


def test_entity(bit_type):
    name = 'ent1'
    entity = Entity(name)
    port1 = entity.add_input_port(name='port1', data_type=bit_type)
    port2 = entity.add_input_port(name='port2', data_type=bit_type)
    expr = port1 & port2
    port3 = entity.add_output_port(name='oport', data_type=bit_type, src=expr)
    assert entity.name == name
    assert entity.port_num == 3
    assert entity.port(0) == port1
    assert entity.port(1) == port2
    assert entity.port(2) == port3
