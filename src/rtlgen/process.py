#! /usr/bin/env python3

"""Process の定義

:file: process.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2022 Yusuke Matsunaga, All rights reserved.
"""

from rtlgen.item import Item
from rtlgen.entity import Entity
from rtlgen.expr import Expr
from rtlgen.writer_base import SimpleBlock
from rtlgen.verilog_writer import VerilogWriter
from rtlgen.rtlerror import RtlError
from rtlgen.statement import StatementBlock, NamedStatementBlock, StmtContext


class Process(Item):
    """process を表すクラス

    VHDL の process，Verilog-HDL の always に相当する構成要素を表す．
    このクラスはセンシティビティリストを持たない組み合わせ論理回路用
    の記述を表す．

    名前を持つことができるが，実際には直下に名前付きブロックが作られる．
    """

    def __init__(self, parent, name=None):
        super().__init__(parent, name=name)
        if name is None:
            self.__body = StatementBlock()
        else:
            self.__body = NamedStatementBlock(name)

    def add_body_stmt(self, stmt):
        """本体のステートメントを追加する．"""
        self.__body.append(stmt)

    def process_body(self):
        """本体を返す．"""
        return StmtContext(self.__body)

    def gen_verilog(self, writer):
        """Verilog-HDL記述の出力を行う．

        :param VerilogWriter writer: Verilog-HDL出力器
        """
        header = self.verilog_header()
        writer.write_line(header, no_nl=True)
        self.__body.gen_verilog(writer)
        writer.write_line('')

    def verilog_header(self):
        return 'always @* '

    def gen_vhdl(self, writer):
        """VHDL記述の出力を行う．

        :param VhdlWriter writer: VHDL出力器
        """
        header = f'{self.name}: process ( ) begin'
        footer = f'end process {self.name};\n'
        with SimpleBlock(writer, header, footer):
            self.__body.gen_vhdl(writer)


class ClockedProcess(Process):
    """process を表すクラス

    VHDL の process，Verilog-HDL の always に相当する構成要素を表す．
    このクラスはセンシティビティリストとしてクロックと非同期制御の
    の2種類を持つ．
    ただし，非同期制御信号は省略可

    クロックは信号線と "positive" か "negative" の文字列を指定する．
    非同期制御は信号線と"positive" か "negative" の文字列を指定する．

    名前を持つことができるが，実際には直下に名前付きブロックが作られる．
    """

    def __init__(self, parent, *, name,
                 clock, clock_pol,
                 asyncctl=None, asyncctl_pol=None):
        super().__init__(parent, name=name)
        self.__clock = clock
        self.__clock_pol = clock_pol
        self.__async = asyncctl
        self.__async_pol = asyncctl_pol
        if self.__async is not None:
            if asyncctl_pol == 'positive':
                async_expr = self.__async
            else:
                async_expr = Expr.make_lnot(self.__async)
            with self.process_body() as _:
                self.__async_if = _.add_if(async_expr)
        else:
            self.__async_if = None

    def add_async_stmt(self, stmt):
        """非同期制御のステートメントを追加する．"""
        with self.__async_if.then_body() as _:
            _.append(stmt)

    def asyncctl_body(self):
        """非同期制御の本体を返す．"""
        if self.__async_if is None:
            return None
        return self.__async_if.then_body()

    def add_body_stmt(self, stmt):
        """本体のステートメントを追加する．"""
        with self.body() as _:
            _.append(stmt)

    def body(self):
        """本体を返す．"""
        if self.__async_if is None:
            return self.process_body()
        else:
            return self.__async_if.else_body()

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

    def asyncctl_body(self):
        """非同期制御の本体を返す．"""
        return self.__async_if.then_body()

    def verilog_header(self):
        header = 'always @( '
        sense_str = VerilogWriter.edge_str(self.__clock_pol)
        header += f'{sense_str} {self.clock.verilog_str}'
        if self.asyncctl is not None:
            sense_str = VerilogWriter.edge_str(self.asyncctl_pol)
            header += f' or {sense_str} {self.asyncctl.verilog_str}'
        header += ' ) '
        return header

    def gen_vhdl(self, writer):
        """VHDL記述の出力を行う．

        :param VhdlWriter writer: VHDL出力器
        """
        header = f'{self.name}: process ( '
        header += self.clock.vhdl_str
        if self.asyncctl is not None:
            header += f', {self.asyncctl.vhdl_str}'
        header += ' ) begin'
        footer = f'end process {self.name};\n'
        with SimpleBlock(writer, header, footer):
            if self.asyncctl is not None:
                if self.asyncctl_pol == 'positive':
                    async_val = 1
                else:
                    async_val = 0
                header = f"if {self.asyncctl.vhdl_str} = '{async_val}' then"
                footer = ''
                with SimpleBlock(writer, header, footer):
                    with self.asyncctl_body() as _:
                        for stmt in _.statement_gen:
                            stmt.gen_vhdl(writer)
                header = 'elsif '
            else:
                header = 'if '
            if self.clock_pol == 'positive':
                header += 'rising_edge'
            else:
                header += 'falling_edge'
            header += f'({self.clock.vhdl_str}) then'
            footer = 'end if;'
            with SimpleBlock(writer, header, footer):
                with self.body() as _:
                    for stmt in _.statement_gen:
                        stmt.gen_vhdl(writer)


def add_clocked_process(self, *,
                        name=None,
                        clock,
                        clock_pol,
                        asyncctl=None,
                        asyncctl_pol=None):
    """クロックに同期したプロセスを追加する．

    :param str name: 名前
    :param Expr clock: クロック信号線
    :param str clock_pol: クロックの極性 ("positive"/"negative")
    :param Expr asyncctl: 非同期制御信号線
    :param str asyncctl_pol: 非同期制御の極性 ("positive"/"negative")
    :return: 生成したプロセスを返す．
    """
    if clock_pol not in ("positive", "negative"):
        emsg = "clock_pol should be 'positive' or 'negative'"
        raise RtlError(emsg)
    if asyncctl is not None:
        if asyncctl_pol not in ("positive", "negative"):
            emsg = "asyncctl_pol should be 'positive' or 'negative'"
            raise RtlError(emsg)
    process = ClockedProcess(self, name=name,
                             clock=clock,
                             clock_pol=clock_pol,
                             asyncctl=asyncctl,
                             asyncctl_pol=asyncctl_pol)
    return process


class CombProcess(Process):
    """組み合わせ回路用の process を表すクラス

    唯一の役目は Process.process_body() の別名を
    body()として定義していること．
    """

    def __init__(self, parent, name=None):
        super().__init__(parent, name=name)

    def body(self):
        """本体を返す．"""
        return self.process_body()


def add_comb_process(self, *,
                     name=None):
    """組み合わせ回路用のプロセスを作る．

    :param str name: 名前
    :return: 生成したプロセスを返す．
    """
    process = CombProcess(self, name=name)
    return process


# Entity クラスにメンバ関数(インスタンスメソッド)を追加する．
Entity.add_clocked_process = add_clocked_process
Entity.add_comb_process = add_comb_process
