#! /usr/bin/env python3

"""
Mux を追加するプログラム

:file: mux.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2022 Yusuke Matsunaga, All rights reserved.
"""

from rtlgen.entity import Entity
from rtlgen.expr import Expr


def add_mux2(self, *,
             sel,
             in0,
             in1,
             data_type=None,
             name=None):
    """2入力MUX を追加する．

    :param Expr sel: 選択信号線
    :param Expr in0: 入力0
    :param Expr in1: 入力1
    :param Expr data_type: 出力のデータ型
    :param str name: 出力の名前
    :return: 出力の信号線を返す．

    通常は出力のデータ型は入力のデータ型から決まる．
    入力の一方が整数の場合には他方のデータ型に補正される．
    2つの入力が共に整数の場合には data_type が用いられる．
    """

    if isinstance(in0, int):
        if isinstance(in1, int):
            assert data_type is not None
            in0 = Expr.make_constant(data_type=data_type, val=in0)
            in1 = Expr.make_constant(data_type=data_type, val=in1)
        else:
            in0 = Expr.make_constant(data_type=in1.data_type, val=in0)
    else:
        if isinstance(in1, int):
            in1 = Expr.make_constant(data_type=data_type, val=in1)

    assert in0.data_type == in1.data_type

    out = self.add_net(reg_type=True, data_type=in0.data_type, name=name)
    mux_body = self.add_comb_body()
    mux_if = mux_body.add_if(sel)
    mux_if.then_body.add_assign(out, in1)
    mux_if.else_body.add_assign(out, in0)
    return out


# Entity クラスにメンバ関数(インスタンスメソッド)を追加する．
Entity.add_mux2 = add_mux2
