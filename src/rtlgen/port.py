#! /usr/bin/env python3

"""Port の定義.

:file: port.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2021 Yusuke Matsunaga, All rights reserved.
"""

from enum import Enum
from rtlgen.expr import Expr, ExprHandle


class PortType(Enum):
    """ポートの種類を表す列挙型"""
    INPUT = 0
    OUTPUT = 1
    INOUT = 2

    def __repr__(self):
        """文字列表現を返す."""
        if self == PortType.INPUT:
            return 'input'
        elif self == PortType.OUTPUT:
            return 'output'
        elif self == PortType.INOUT:
            return 'inout'
        else:
            assert False


class Port(Expr):
    """ポートを表す基底クラス

    :param DataType data_type: データタイプ
    :param str name: ポート名(名前付きのオプション引数)
    """

    def __init__(self, data_type, *, name=None):
        super().__init__()
        self.__data_type = data_type
        self.__name = name

    def is_simple(self):
        return True

    @property
    def needs_net(self):
        return False

    @property
    def is_input(self):
        """入力ポートの時 True を返す."""
        return False

    @property
    def is_output(self):
        """出力ポートの時 True を返す."""
        return False

    @property
    def is_inout(self):
        """入出力ポートの時 True を返す."""
        return False

    @property
    def data_type(self):
        """データタイプを返す.

        :rtype: DataType
        """
        return self.__data_type

    @property
    def name(self):
        """名前を返す.

        :rtype: str
        """
        return self.__name

    def set_name(self, name):
        """名前を設定する．

        :param string name: ポート名
        """
        self.__name = name

    @property
    def verilog_str(self):
        """Verilog-HDLの表記を返す．"""
        return self.name

    @property
    def vhdl_str(self):
        """VHDLの表記を返す．"""
        return self.name


class InputPort(Port):
    """入力ポートを表すクラス

    :param DataType data_type: データタイプ
    :param str name: ポート名(名前付きのオプション引数)
    """

    def __init__(self, data_type, *, name=None):
        super().__init__(data_type, name=name)

    @property
    def port_type(self):
        """ポートの種類を返す.

        :rtype: PortType
        """
        return PortType.INPUT

    @property
    def is_input(self):
        """入力ポートの時 True を返す."""
        return True

    @property
    def verilog_str(self):
        """Verilog-HDL の式を表す文字列を返す．"""
        return self.name

    @property
    def vhdl_str(self):
        """VHDL の式を表す文字列を返す．"""
        return self.name


class OutputPort(Port):
    """出力ポートを表すクラス

    :param DataType data_type: データタイプ
    :param str name: 名前(名前付きのオプション引数)
    """

    def __init__(self, data_type, *, name=None):
        super().__init__(data_type, name=name)

    @property
    def port_type(self):
        """ポートの種類を返す.

        :rtype: PortType
        """
        return PortType.OUTPUT

    @property
    def is_output(self):
        """出力ポートの時 True を返す."""
        return True


class InoutPort(OutputPort):
    """入出力ポートを表すクラス

    :param DataType data_type: データタイプ
    :param str name: 名前(名前付きのオプション引数)
    """

    def __init__(self, data_type, *, name=None):
        super().__init__(data_type, name=name)

    @property
    def port_type(self):
        """ポートの種類を返す.

        :rtype: PortType
        """
        return PortType.INOUT

    @property
    def is_output(self):
        """出力ポートの時 True を返す."""
        return False

    @property
    def is_inout(self):
        """入出力ポートの時 True を返す."""
        return True
