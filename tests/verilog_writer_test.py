#! /usr/bin/env python3

"""VerilogWriter のテスト
:file entity_test.py
:author Yusuke Matsunaga (松永 裕介)
:copyright (C) 2021 Yusuke Matsunaga, All rights reserved.
"""

import sys
import pytest
from rtlgen.entity import Entity
from rtlgen import DataType
from rtlgen.verilog_writer import VerilogWriter


@pytest.fixture
def bit_type():
    return DataType.bit_type()


def test_verilong_writer(bit_type):
    name = 'ent1'
    entity = Entity(name)
    port1 = entity.add_input_port(data_type=bit_type, name='port1')
    port2 = entity.add_input_port(data_type=bit_type, name='port2')
    expr = port1 & port2
    port3 = entity.add_output_port(data_type=bit_type, name='oport', src=expr)
    vw = VerilogWriter(fout=sys.stdout)
    vw(entity)
