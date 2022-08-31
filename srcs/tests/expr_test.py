#! /usr/bin/env python3

""" Expr のテストプログラム
:file expr_test.py
:author Yusuke Matsunaga (松永 裕介)
:copyright (C) 2021 Yusuke Matsunaga, All rights reserved.
"""

import pytest
from rtlgen import Expr
from rtlgen.expr import OpType, UnaryOp, BinaryOp
from rtlgen import Net
from rtlgen import BitType, BitVectorType


@pytest.fixture
def bit_type():
    return BitType()


@pytest.fixture
def bv16_type():
    return BitVectorType(16)


def test_net1(bit_type):
    net = Net(bit_type)
    assert net.data_type == bit_type


def test_make_not(bit_type):
    net1 = Net(bit_type)
    expr = Expr.make_not(net1)
    assert isinstance(expr, UnaryOp)
    assert expr.op_type == OpType.NOT
    assert expr.data_type == bit_type


def test_make_and(bit_type):
    net1 = Net(bit_type)
    net2 = Net(bit_type)
    expr = Expr.make_and(net1, net2)
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.AND
    assert expr.data_type == bit_type


def test_make_or(bit_type):
    net1 = Net(bit_type)
    net2 = Net(bit_type)
    expr = Expr.make_or(net1, net2)
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.OR
    assert expr.data_type == bit_type


def test_make_xor(bit_type):
    net1 = Net(bit_type)
    net2 = Net(bit_type)
    expr = Expr.make_xor(net1, net2)
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.XOR
    assert expr.data_type == bit_type


def test_make_nand(bit_type):
    net1 = Net(bit_type)
    net2 = Net(bit_type)
    expr = Expr.make_nand(net1, net2)
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.NAND
    assert expr.data_type == bit_type


def test_make_nor(bit_type):
    net1 = Net(bit_type)
    net2 = Net(bit_type)
    expr = Expr.make_nor(net1, net2)
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.NOR
    assert expr.data_type == bit_type


def test_make_xnor(bit_type):
    net1 = Net(bit_type)
    net2 = Net(bit_type)
    expr = Expr.make_xnor(net1, net2)
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.XNOR
    assert expr.data_type == bit_type


def test_make_uminus(bv16_type):
    net1 = Net(bv16_type)
    expr = Expr.make_uminus(net1)
    assert isinstance(expr, UnaryOp)
    assert expr.op_type == OpType.COMPL
    assert expr.data_type == bv16_type


def test_make_add(bv16_type):
    net1 = Net(bv16_type)
    net2 = Net(bv16_type)
    expr = Expr.make_add(net1, net2)
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.ADD
    assert expr.data_type == bv16_type


def test_make_sub(bv16_type):
    net1 = Net(bv16_type)
    net2 = Net(bv16_type)
    expr = Expr.make_sub(net1, net2)
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.SUB
    assert expr.data_type == bv16_type


def test_make_mul(bv16_type):
    net1 = Net(bv16_type)
    net2 = Net(bv16_type)
    expr = Expr.make_mul(net1, net2)
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.MUL
    assert expr.data_type == bv16_type


def test_make_div(bv16_type):
    net1 = Net(bv16_type)
    net2 = Net(bv16_type)
    expr = Expr.make_div(net1, net2)
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.DIV
    assert expr.data_type == bv16_type


def test_make_mod(bv16_type):
    net1 = Net(bv16_type)
    net2 = Net(bv16_type)
    expr = Expr.make_mod(net1, net2)
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.MOD
    assert expr.data_type == bv16_type


def test_make_lsft(bv16_type):
    net1 = Net(bv16_type)
    net2 = Net(bv16_type)
    expr = Expr.make_lsft(net1, net2)
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.LSFT
    assert expr.data_type == bv16_type


def test_make_rsft(bv16_type):
    net1 = Net(bv16_type)
    net2 = Net(bv16_type)
    expr = Expr.make_rsft(net1, net2)
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.RSFT
    assert expr.data_type == bv16_type


def test_make_eq(bv16_type):
    net1 = Net(bv16_type)
    net2 = Net(bv16_type)
    expr = Expr.make_eq(net1, net2)
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.EQ
    assert expr.data_type == bv16_type


def test_make_ne(bv16_type):
    net1 = Net(bv16_type)
    net2 = Net(bv16_type)
    expr = Expr.make_ne(net1, net2)
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.NE
    assert expr.data_type == bv16_type


def test_make_lt(bv16_type):
    net1 = Net(bv16_type)
    net2 = Net(bv16_type)
    expr = Expr.make_lt(net1, net2)
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.LT
    assert expr.data_type == bv16_type
    assert expr.operand1 == net1
    assert expr.operand2 == net2


def test_make_gt(bv16_type):
    net1 = Net(bv16_type)
    net2 = Net(bv16_type)
    expr = Expr.make_gt(net1, net2)
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.LT
    assert expr.data_type == bv16_type
    assert expr.operand1 == net2
    assert expr.operand2 == net1


def test_make_le(bv16_type):
    net1 = Net(bv16_type)
    net2 = Net(bv16_type)
    expr = Expr.make_le(net1, net2)
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.LE
    assert expr.data_type == bv16_type
    assert expr.operand1 == net1
    assert expr.operand2 == net2


def test_make_ge(bv16_type):
    net1 = Net(bv16_type)
    net2 = Net(bv16_type)
    expr = Expr.make_ge(net1, net2)
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.LE
    assert expr.data_type == bv16_type
    assert expr.operand1 == net2
    assert expr.operand2 == net1


def test_not(bit_type):
    net1 = Net(bit_type)
    expr = ~net1
    assert isinstance(expr, UnaryOp)
    assert expr.op_type == OpType.NOT
    assert expr.data_type == bit_type


def test_and(bit_type):
    net1 = Net(bit_type)
    net2 = Net(bit_type)
    expr = net1 & net2
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.AND
    assert expr.data_type == bit_type


def test_andc1(bit_type):
    net1 = Net(bit_type)
    expr = net1 & 1
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.AND
    assert expr.data_type == bit_type


def test_andc2(bit_type):
    net1 = Net(bit_type)
    expr = 1 & net1
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.AND
    assert expr.data_type == bit_type


def test_or(bit_type):
    net1 = Net(bit_type)
    net2 = Net(bit_type)
    expr = net1 | net2
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.OR
    assert expr.data_type == bit_type


def test_orc1(bit_type):
    net1 = Net(bit_type)
    expr = net1 | 1
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.OR
    assert expr.data_type == bit_type


def test_orc2(bit_type):
    net1 = Net(bit_type)
    expr = 1 | net1
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.OR
    assert expr.data_type == bit_type


def test_xor(bit_type):
    net1 = Net(bit_type)
    net2 = Net(bit_type)
    expr = net1 ^ net2
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.XOR
    assert expr.data_type == bit_type


def test_xorc1(bit_type):
    net1 = Net(bit_type)
    expr = net1 ^ 1
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.XOR
    assert expr.data_type == bit_type


def test_xorc2(bit_type):
    net1 = Net(bit_type)
    expr = 1 ^ net1
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.XOR
    assert expr.data_type == bit_type


def test_neg(bv16_type):
    net1 = Net(bv16_type)
    expr = -net1
    assert isinstance(expr, UnaryOp)
    assert expr.op_type == OpType.COMPL
    assert expr.data_type == bv16_type


def test_add(bv16_type):
    net1 = Net(bv16_type)
    net2 = Net(bv16_type)
    expr = net1 + net2
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.ADD
    assert expr.data_type == bv16_type


def test_addc1(bv16_type):
    net1 = Net(bv16_type)
    expr = net1 + 4
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.ADD
    assert expr.data_type == bv16_type


def test_addc2(bv16_type):
    net1 = Net(bv16_type)
    expr = 4 + net1
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.ADD
    assert expr.data_type == bv16_type


def test_sub(bv16_type):
    net1 = Net(bv16_type)
    net2 = Net(bv16_type)
    expr = net1 - net2
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.SUB
    assert expr.data_type == bv16_type


def test_subc1(bv16_type):
    net1 = Net(bv16_type)
    expr = net1 - 3
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.SUB
    assert expr.data_type == bv16_type


def test_subc2(bv16_type):
    net1 = Net(bv16_type)
    expr = 3 - net1
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.SUB
    assert expr.data_type == bv16_type


def test_mul(bv16_type):
    net1 = Net(bv16_type)
    net2 = Net(bv16_type)
    expr = net1 * net2
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.MUL
    assert expr.data_type == bv16_type


def test_mulc1(bv16_type):
    net1 = Net(bv16_type)
    expr = net1 * 2
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.MUL
    assert expr.data_type == bv16_type


def test_mulc2(bv16_type):
    net1 = Net(bv16_type)
    expr = 2 * net1
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.MUL
    assert expr.data_type == bv16_type


def test_div(bv16_type):
    net1 = Net(bv16_type)
    net2 = Net(bv16_type)
    expr = net1 / net2
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.DIV
    assert expr.data_type == bv16_type


def test_divc1(bv16_type):
    net1 = Net(bv16_type)
    expr = net1 / 5
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.DIV
    assert expr.data_type == bv16_type


def test_divc2(bv16_type):
    net1 = Net(bv16_type)
    expr = 5 / net1
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.DIV
    assert expr.data_type == bv16_type


def test_mod(bv16_type):
    net1 = Net(bv16_type)
    net2 = Net(bv16_type)
    expr = net1 % net2
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.MOD
    assert expr.data_type == bv16_type


def test_modc1(bv16_type):
    net1 = Net(bv16_type)
    expr = net1 % 6
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.MOD
    assert expr.data_type == bv16_type


def test_modc2(bv16_type):
    net1 = Net(bv16_type)
    expr = 6 % net1
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.MOD
    assert expr.data_type == bv16_type


def test_lsft(bv16_type):
    net1 = Net(bv16_type)
    net2 = Net(bv16_type)
    expr = net1 << net2
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.LSFT
    assert expr.data_type == bv16_type


def test_lsftc1(bv16_type):
    net1 = Net(bv16_type)
    expr = net1 << 7
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.LSFT
    assert expr.data_type == bv16_type


def test_rsft(bv16_type):
    net1 = Net(bv16_type)
    net2 = Net(bv16_type)
    expr = net1 >> net2
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.RSFT
    assert expr.data_type == bv16_type


def test_rsftc1(bv16_type):
    net1 = Net(bv16_type)
    expr = net1 >> 8
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.RSFT
    assert expr.data_type == bv16_type


def test_eq(bv16_type):
    net1 = Net(bv16_type)
    net2 = Net(bv16_type)
    expr = net1 == net2
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.EQ
    assert expr.data_type == bv16_type


def test_eqc1(bv16_type):
    net1 = Net(bv16_type)
    expr = net1 == 0
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.EQ
    assert expr.data_type == bv16_type


def test_eqc2(bv16_type):
    net1 = Net(bv16_type)
    expr = 8 == net1
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.EQ
    assert expr.data_type == bv16_type


def test_ne(bv16_type):
    net1 = Net(bv16_type)
    net2 = Net(bv16_type)
    expr = net1 != net2
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.NE
    assert expr.data_type == bv16_type


def test_nec1(bv16_type):
    net1 = Net(bv16_type)
    expr = net1 != 1
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.NE
    assert expr.data_type == bv16_type


def test_nec1(bv16_type):
    net1 = Net(bv16_type)
    expr = 1 != net1
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.NE
    assert expr.data_type == bv16_type


def test_lt(bv16_type):
    net1 = Net(bv16_type)
    net2 = Net(bv16_type)
    expr = net1 < net2
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.LT
    assert expr.data_type == bv16_type
    assert expr.operand1 == net1
    assert expr.operand2 == net2


def test_ltc1(bv16_type):
    net1 = Net(bv16_type)
    expr = net1 < 2
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.LT
    assert expr.data_type == bv16_type
    assert expr.operand1 == net1


def test_ltc2(bv16_type):
    net1 = Net(bv16_type)
    expr = net1 < 2
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.LT
    assert expr.data_type == bv16_type
    assert expr.operand1 == net1


def test_ltc2(bv16_type):
    net1 = Net(bv16_type)
    expr = 2 < net1
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.LT
    assert expr.data_type == bv16_type
    assert expr.operand1 == net1


def test_gt(bv16_type):
    net1 = Net(bv16_type)
    net2 = Net(bv16_type)
    expr = net1 > net2
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.LT
    assert expr.data_type == bv16_type
    assert expr.operand1 == net2
    assert expr.operand2 == net1


def test_gtc1(bv16_type):
    net1 = Net(bv16_type)
    expr = net1 > 3
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.LT
    assert expr.data_type == bv16_type
    assert expr.operand2 == net1


def test_gtc2(bv16_type):
    net1 = Net(bv16_type)
    expr = 3 > net1
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.LT
    assert expr.data_type == bv16_type
    assert expr.operand2 == net1


def test_le(bv16_type):
    net1 = Net(bv16_type)
    net2 = Net(bv16_type)
    expr = net1 <= net2
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.LE
    assert expr.data_type == bv16_type
    assert expr.operand1 == net1
    assert expr.operand2 == net2


def test_lec1(bv16_type):
    net1 = Net(bv16_type)
    expr = net1 <= 4
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.LE
    assert expr.data_type == bv16_type
    assert expr.operand1 == net1


def test_lec2(bv16_type):
    net1 = Net(bv16_type)
    expr = 4 <= net1
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.LE
    assert expr.data_type == bv16_type
    assert expr.operand1 == net1


def test_ge(bv16_type):
    net1 = Net(bv16_type)
    net2 = Net(bv16_type)
    expr = net1 >= net2
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.LE
    assert expr.data_type == bv16_type
    assert expr.operand1 == net2
    assert expr.operand2 == net1


def test_gec1(bv16_type):
    net1 = Net(bv16_type)
    expr = net1 >= 5
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.LE
    assert expr.data_type == bv16_type
    assert expr.operand2 == net1


def test_gec2(bv16_type):
    net1 = Net(bv16_type)
    expr = 5 >= net1
    assert isinstance(expr, BinaryOp)
    assert expr.op_type == OpType.LE
    assert expr.data_type == bv16_type
    assert expr.operand2 == net1
