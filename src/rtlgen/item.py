#! /usr/bin/env python3

"""
Item の定義

:file: item.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2022 Yusuke Matsunaga, All rights reserved.
"""

from rtlgen.net import Net
from rtlgen.var import Var


class Item:
    """RTL記述の基本構成要素の基底クラス

    item はインスタンスのような構成要素の基底クラスであり，
    内部にネットのリスト，継続的代入文のリストなどを持つ．

    また，継承クラスは自身の内容に対するVerilog-HDL記述，VHDL記述
    を生成する関数を持つ．
    """

    def __init__(self, parent, *, name=None):
        self.__parent = parent
        self.__name = name
        parent.reg_item(self)

    @property
    def name(self):
        """名前を返す．

        :rtype: str or None
        """
        return self.__name

    def set_name(self, name):
        """名前をセットする．

        :param str name: 名前
        """
        self.__name = name

    @property
    def is_inst(self):
        return False

    def add_net(self, data_type, *, name=None, reg_type=False):
        """ネットを追加する．"""
        net = self.__parent.add_net(
            data_type=data_type, name=name, reg_type=reg_type)
        return net

    def add_var(self, data_type, *, name=None):
        """変数を追加する．"""
        var = self.__parent.add_var(data_type, name=name)
        return var

    def add_cont_assign(self, lhs, rhs):
        """継続的代入文を追加する．"""
        self.__parent.add_cont_assign(lhs, rhs)
