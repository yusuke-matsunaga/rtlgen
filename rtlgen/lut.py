#! /usr/bin/env python3

"""
LookUpTable を表すクラス

:file: lut.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2022 Yusuke Matsunaga, All rights reserved.
"""

from rtlgen.expr import Expr
from rtlgen.item import Item
from rtlgen.data_type import BitVectorType
from rtlgen.entity import Entity
from rtlgen.writer_base import SimpleBlock


class Lut(Item):
    """LookUp Table を表すクラス

    :param int input_bw: 入力のビット幅
    :param DataType data_type: 出力のデータ型
    :param list[(Expr, Expr)] data_list: データのリスト

    入出力の仕様
    * input: 入力．データ型は BitVectorType(input_bw)
    * output: 出力．データ型は data_type
    """

    def __init__(self, parent, *,
                 name=None,
                 input_bw=None,
                 input=None,
                 data_type,
                 data_list=None):
        super().__init__(parent, name=name)
        self.__data_list = list()
        if input is None:
            assert input_bw is not None
            ibv = BitVectorType(input_bw)
            self.__input = self.add_net(data_type=ibv)
        else:
            self.__input = input
            ibv = input.data_type
        self.__output = self.add_net(data_type=data_type, reg_type=True)
        for idata, odata in data_list:
            if not isinstance(idata, Expr):
                idata = Expr.make_constant(data_type=ibv, val=idata)
            if not isinstance(odata, Expr):
                odata = Expr.make_constant(data_type=data_type, val=odata)
            self.__data_list.append((idata, odata))

    @property
    def input(self):
        """入力のネットを返す．"""
        return self.__input

    @property
    def output(self):
        """出力のネットを返す．"""
        return self.__output

    @property
    def data_gen(self):
        for indata, outdata in self.__data_list:
            yield indata, outdata

    def add_data(self, indata, outdata):
        """データを追加する．

        :param Expr indata: 入力値
        :param Expr outdata: 出力値
        """
        assert indata.data_type == self.__input.data_type
        assert outdata.data_type == self.__output.data_type
        self.__data_list.append((indata, outdata))

    def gen_verilog(self, writer):
        """Verilog-HDL記述を生成する．

        :param VerilogWriter writer: Verilog-DL出力器
        """
        header = "always @* begin"
        footer = "end\n"
        with SimpleBlock(writer, header, footer):
            header = 'case ( {} )'.format(self.__input.verilog_str)
            footer = 'endcase'
            with SimpleBlock(writer, header, footer):
                lines = list()
                for indata, outdata in self.__data_list:
                    line = ['{}:'.format(indata.verilog_str),
                            '{} <= {}'.format(self.__output.verilog_str,
                                              outdata.verilog_str)]
                    lines.append(line)
                line = ['default:', '']
                lines.append(line)
                writer.write_lines(lines, end=';')

    def gen_vhdl(self, writer):
        """VHDL記述を生成する．

        :param VhdlWriter writer: VHDL出力器
        """
        header = '{}: process ( {} ) begin'.format(
            self.name, self.__input.vhdl_str)
        footer = 'end process {};\n'.format(self.name)
        with SimpleBlock(writer, header, footer):
            header = 'case {} is'.format(self.__input.vhdl_str)
            footer = 'end case;'
            with SimpleBlock(writer, header, footer):
                lines = list()
                for indata, outdata in self.__data_list:
                    line = ['when {}'.format(indata.vhdl_str),
                            '=>', '{} <= {}'.format(self.__output.vhdl_str,
                                                    outdata.vhdl_str)]
                    lines.append(line)
                line = ['when others', '=>', 'null']
                lines.append(line)
                writer.write_lines(lines, end=';')


def add_lut(self, *,
            input_bw=None, input=None,
            data_type,
            data_list=None):
    lut = Lut(self, input_bw=input_bw, input=input,
              data_type=data_type,
              data_list=data_list)
    return lut


# Entity にメンバ関数(インスタンスメソッド)を追加する．
Entity.add_lut = add_lut
