#! /usr/bin/env python3

"""
変数を表すクラス

:file: var.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2022 Yusuke Matsunaga, All rights reserved.
"""

from rtlgen.expr import Expr


class Var(Expr):
    """変数を表すクラス

    :param DataType data_type: データタイプ
    :param str name: 名前
    """

    def __init__(self, data_type, name=None):
        super().__init__()
        self.__type = data_type
        self.__name = name

    def is_simple(self):
        return True

    @property
    def data_type(self):
        """データタイプを返す．"""
        return self.__type

    @property
    def name(self):
        """名前を返す．"""
        return self.__name

    def set_name(self, name):
        """名前を設定する．

        :param string name: ポート名
        """
        self.__name = name

    @ property
    def verilog_str(self):
        """Verilog-HDL の式を表す文字列を返す．"""
        return self.name

    @ property
    def vhdl_str(self):
        """VHDL の式を表す文字列を返す．"""
        return self.name
