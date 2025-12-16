#! /usr/bin/env python3

"""Port のテストプログラム
:file port_test.py
:author Yusuke Matsunaga (松永 裕介)
:copyright (C) 2021 Yusuke Matsunaga, All rights reserved.
"""

import pytest
from rtlgen import InputPort, OutputPort, InoutPort
from rtlgen import BitType
from rtlgen.port import PortType


@pytest.fixture
def bit_type():
    return BitType()


def test_input_port1(bit_type):
    port = InputPort(bit_type)
    assert port.port_type == PortType.INPUT
    assert port.is_input
    assert not port.is_output
    assert not port.is_inout
    assert port.name is None


def test_input_port2(bit_type):
    name = 'port1'
    port = InputPort(bit_type, name=name)
    assert port.port_type == PortType.INPUT
    assert port.is_input
    assert not port.is_output
    assert not port.is_inout
    assert port.name == name


def test_output_port1(bit_type):
    port = OutputPort(bit_type)
    assert port.port_type == PortType.OUTPUT
    assert not port.is_input
    assert port.is_output
    assert not port.is_inout
    assert port.name is None


def test_output_port2(bit_type):
    name = 'port2'
    port = OutputPort(bit_type, name=name)
    assert port.port_type == PortType.OUTPUT
    assert not port.is_input
    assert port.is_output
    assert not port.is_inout
    assert port.name == name


def test_inout_port1(bit_type):
    port = InoutPort(bit_type)
    assert port.port_type == PortType.INOUT
    assert not port.is_input
    assert not port.is_output
    assert port.is_inout
    assert port.name is None


def test_inout_port2(bit_type):
    name = 'port2'
    port = InoutPort(bit_type, name=name)
    assert port.port_type == PortType.INOUT
    assert not port.is_input
    assert not port.is_output
    assert port.is_inout
    assert port.name == name
