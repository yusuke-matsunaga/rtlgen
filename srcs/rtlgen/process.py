#! /usr/bin/env python3

"""Process の定義

:file: process.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2022 Yusuke Matsunaga, All rights reserved.
"""

from rtlgen.item import Item
from rtlgen.entity import Entity
from rtlgen.writer_base import SimpleBlock
from rtlgen.verilog_writer import VerilogWriter
from rtlgen.rtlerror import RtlError
from rtlgen.statement import StatementBlock


class Process(Item):
    """process を表すクラス

    VHDL の process，Verilog-HDL の always に相当する構成要素を表す．
    ただし，センシティビティリストを
    - クロック
    - 非同期制御
    の2種類に分類している．

    クロックは信号線と "positive" か "negative" の文字列を指定する．
    非同期制御は信号線と"positive" か "negative" の文字列を指定する．

    クロックも非同期制御もない場合には純粋な組み合わせ論理回路を合成する．
    クロックなしで非同期制御のみが指定された場合はエラーとなる．
    """

    def __init__(self, parent, name,
                 clock, clock_pol,
                 asyncctl, asyncctl_pol):
        super().__init__(parent, name=name)
        self.__clock = clock
        self.__clock_pol = clock_pol
        self.__async = asyncctl
        self.__async_pol = asyncctl_pol
        self.__async_body = StatementBlock()
        self.__body = StatementBlock()

    def add_async_stmt(self, stmt):
        """非同期制御のステートメントを追加する．"""
        if self.asyncctl is None:
            emsg = "asyncctl is not specified"
            raise RtlError(emsg)
        self.__async_body.append(stmt)

    def add_body_stmt(self, stmt):
        """本体のステートメントを追加する．"""
        self.__body.append(stmt)

    @property
    def clock(self):
        """クロック信号を返す．"""
        return self.__clock

    @property
    def clock_pol(self):
        """クロックの極性を返す．"""
        return self.__clock_pol

    @property
    def asyncctl(self):
        """非同期制御信号を返す．"""
        return self.__async

    @property
    def asyncctl_pol(self):
        """非同期制御の極性を返す．"""
        return self.__async_pol

    @property
    def asyncctl_body(self):
        """非同期制御の本体を返す．"""
        return self.__async_body

    @property
    def body(self):
        """本体を返す．"""
        return self.__body

    def gen_verilog(self, writer):
        """Verilog-HDL記述の出力を行う．

        :param VerilogWriter writer: Verilog-HDL出力器
        """
        header = 'always @'
        if self.clock is not None:
            header += '('
            sense_str = VerilogWriter.edge_str(self.__clock_pol)
            header += '{} {}'.format(sense_str, self.clock.verilog_str)
            if self.asyncctl is not None:
                sense_str = VerilogWriter.edge_str(self.__async_pol)
                header += ' or {} {}'.format(sense_str,
                                             self.asyncctl.verilog_str)
            header += ')'
        else:
            header += '*'
        header += ' begin'
        footer = 'end\n'
        with SimpleBlock(writer, header, footer):
            if self.asyncctl is not None:
                cond = VerilogWriter.cond_str(
                    self.asyncctl, self.__async_pol)
                header = 'if ( {} ) begin'.format(cond)
                footer = 'end'
                with SimpleBlock(writer, header, footer):
                    self.asyncctl_body.gen_verilog(writer)
                header = 'else begin'
                footer = 'end'
                with SimpleBlock(writer, header, footer):
                    self.body.gen_verilog(writer)
            else:
                self.body.gen_verilog(writer)

    def gen_vhdl(self, writer):
        """VHDL記述の出力を行う．

        :param VhdlWriter writer: VHDL出力器
        """
        header = '{}: process('.format(self.name)
        if self.clock is not None:
            header += self.clock.vhdl_str
            if self.asyncctl is not None:
                header += ', {}'.format(self.asyncctl.vhdl_str)
        header += ') begin'
        footer = 'end process;\n'
        with SimpleBlock(writer, header, footer):
            if self.clock is not None:
                if self.asyncctl is not None:
                    if self.__async_pol == "positive":
                        asyncctl_val = "'1'"
                    elif self.__async_pol == "negative":
                        asyncctl_val = "'0'"
                    else:
                        assert False
                    header = 'if {} = {} then'.format(
                        self.asyncctl.vhdl_str, asyncctl_val)
                    footer = ''
                    with SimpleBlock(writer, header, footer):
                        self.asyncctl_body.gen_vhdl(writer)
                    if_str = 'elsif'
                else:
                    if_str = 'if'
                if self.__clock_pol == "positive":
                    clock_edge = "rising_edge"
                elif self.__clock_pol == "negative":
                    clock_edge = "falling_edge"
                else:
                    assert False
                header = '{} {}( {} ) then'.format(
                    if_str, clock_edge, self.clock.vhdl_str)
                footer = 'end if;'
                with SimpleBlock(writer, header, footer):
                    self.body.gen_vhdl(writer)
            else:
                self.body.gen_vhdl(writer)


def add_process(self, *,
                name=None,
                clock=None,
                clock_pol=None,
                asyncctl=None,
                asyncctl_pol=None):
    """プロセスを追加する．

    :param str name: 名前
    :param Expr clock: クロック信号線
    :param str clock_pol: クロックの極性 ("positive"/"negative")
    :param Expr asyncctl: 非同期制御信号線
    :param str asyncctl_pol: 非同期制御の極性 ("positive"/"negative")
    :return: 生成したプロセスを返す．
    """
    if clock is None and asyncctl is not None:
        emsg = "asyncctl withou clock is not allowed."
        raise RtlError(emsg)
    if clock is not None:
        if clock_pol != "positive" and clock_pol != "negative":
            emsg = "clock_pol should be 'positive' or 'negative'"
            raise RtlError(emsg)
    if asyncctl is not None:
        if asyncctl_pol != "positive" and asyncctl_pol != "negative":
            emsg = "asyncctl_pol should be 'positive' or 'negative'"
            raise RtlError(emsg)
    process = Process(self, name=name,
                      clock=clock, clock_pol=clock_pol,
                      asyncctl=asyncctl, asyncctl_pol=asyncctl_pol)
    return process


def add_comb_body(self, *,
                  name=None):
    """組み合わせ回路用のプロセスを作る．

    :param str name: 名前
    :return: 本体のステートメントブロックを返す．
    """
    proc = Process(self, name=name,
                   clock=None, clock_pol=None,
                   asyncctl=None, asyncctl_pol=None)
    return proc.body


# Entity クラスにメンバ関数(インスタンスメソッド)を追加する．
Entity.add_process = add_process
Entity.add_comb_body = add_comb_body
