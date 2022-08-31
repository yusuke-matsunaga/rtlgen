#! /usr/bin/env python3

"""VerilogWriter のテスト
:file entity_test.py
:author Yusuke Matsunaga (松永 裕介)
:copyright (C) 2021 Yusuke Matsunaga, All rights reserved.
"""

import sys
import pytest
from rtlgen import Entity
from rtlgen import InputPort, OutputPort
from rtlgen import BitType
from rtlgen import VerilogWriter


@pytest.fixture
def bit_type():
    return BitType()


def test_verilong_writer(bit_type):
    name = 'ent1'
    port1 = InputPort(bit_type, name='port1')
    port2 = InputPort(bit_type, name='port2')
    port3 = OutputPort(bit_type, name='oport')
    expr = port1 & port2
    port3.set_src(expr)
    entity = Entity(name, [port1, port2, port3])
    vw = VerilogWriter(fout=sys.stdout)
    vw(entity)
