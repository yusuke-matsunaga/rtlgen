#! /usr/bin/env python3

# @file net.py
# @brief Net のクラス定義
# @author Yusuke Matsunaga (松永 裕介)
###
# Copyright (C) 2021 Yusuke Matsunaga
# All rights reserved.

from rtlgen.expr import Expr


class Net(Expr):
    """ネットを表すクラス

    :param DataType data_type: データタイプ
    :param str name: 名前
    """

    def __init__(self, data_type, name=None, reg_type=False):
        super().__init__()
        self.__type = data_type
        self.__name = name
        self.__reg_type = reg_type

    @property
    def needs_net(self):
        return False

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

    @property
    def reg_type(self):
        """reg 型の時 True を返す．"""
        return self.__reg_type

    @property
    def verilog_str(self):
        """Verilog-HDL の式を表す文字列を返す．"""
        return self.name

    @property
    def vhdl_str(self):
        """VHDL の式を表す文字列を返す．"""
        return self.name
