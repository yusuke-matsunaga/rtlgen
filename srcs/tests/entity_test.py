#! /usr/bin/env python3

"""Entity のテスト
:file entity_test.py
:author Yusuke Matsunaga (松永 裕介)
:copyright (C) 2021 Yusuke Matsunaga, All rights reserved.
"""

import pytest
from rtlgen import Entity
from rtlgen import InputPort, OutputPort
from rtlgen import BitType


@pytest.fixture
def bit_type():
    return BitType()


def test_entity(bit_type):
    name = 'ent1'
    port1 = InputPort(bit_type, name='port1')
    port2 = InputPort(bit_type, name='port2')
    port3 = OutputPort(bit_type, name='oport')
    expr = port1 & port2
    port3.set_src(expr)
    entity = Entity(name, [port1, port2, port3])
    assert entity.name == name
    assert entity.port_num == 3
    assert entity.port(0) == port1
    assert entity.port(1) == port2
    assert entity.port(2) == port3
