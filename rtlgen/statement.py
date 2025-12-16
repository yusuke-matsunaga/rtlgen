#! /usr/bin/env python3

"""Statement の定義

:file: statement.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2022 Yusuke Matsunaga, All rights reserved.
"""

from enum import Enum
from rtlgen.expr import Expr
from rtlgen.writer_base import SimpleBlock


class StmtType(Enum):
    """ステートメントの種類を表す列挙型"""
    BlockingAssign = 1
    NonblockingAssign = 2
    IfStatement = 3
    CaseStatement = 4
    WhileStatement = 5
    StatementBlock = 6


class Statement:
    """ステートメントを表すクラス
    """

    def __init__(self):
        # 実はこの継承クラスにあまり用はない．
        pass


class AssignBase(Statement):
    """代入文を表すクラス
    """

    def __init__(self, lhs, rhs):
        super().__init__()
        rhs = lhs.coerce(rhs)
        self.__lhs = lhs
        self.__rhs = rhs

    @property
    def lhs(self):
        """左辺式を返す．"""
        return self.__lhs

    @property
    def rhs(self):
        """右辺式を返す．"""
        return self.__rhs


class BlockingAssign(AssignBase):
    """ブロッキング代入文を表すクラス
    """

    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs)

    @property
    def type(self):
        """ステートメントの種類を返す．"""
        return StmtType.BlockingAssign

    def gen_verilog(self, writer):
        """Verilog-HDL記述を生成する

        :param VerilogWriter writer: Verilog-HDL出力器
        """
        line = '{} = {};'.format(self.lhs.verilog_str, self.rhs.verilog_str)
        writer.write_line(line)

    def gen_vhdl(self, writer):
        """VHDL記述を生成する

        :param VhdlWriter writer: VHDL出力器
        """
        line = '{} = {};'.format(self.lhs.vhdl_str, self.rhs.vhdl_str)
        writer.write_line(line)


class NonblockingAssign(AssignBase):
    """ノンブロッキング代入文を表すクラス
    """

    def __init__(self, lhs, rhs):
        super().__init__(lhs, rhs)

    @property
    def type(self):
        """ステートメントの種類を返す．"""
        return StmtType.NonblockingAssign

    def gen_verilog(self, writer):
        """Verilog-HDL記述を生成する

        :param VerilogWriter writer: Verilog-HDL出力器
        """
        line = '{} <= {};'.format(self.lhs.verilog_str, self.rhs.verilog_str)
        writer.write_line(line)

    def gen_vhdl(self, writer):
        """VHDL記述を生成する

        :param VhdlWriter writer: VHDL出力器
        """
        line = '{} <= {};'.format(self.lhs.vhdl_str, self.rhs.vhdl_str)
        writer.write_line(line)


class IfStatement(Statement):
    """If 文を表すクラス
    """

    def __init__(self, cond):
        super().__init__()
        self.__cond = cond
        self.__then = StatementBlock()
        self.__else = StatementBlock()

    @property
    def type(self):
        """ステートメントの種類を返す．"""
        return StmtType.IfStatement

    @property
    def cond(self):
        """条件式を返す．"""
        return self.__cond

    @property
    def then_body(self):
        """Then節を返す．"""
        return self.__then

    @property
    def else_body(self):
        """Else節を返す．"""
        return self.__else

    def gen_verilog(self, writer):
        """Verilog-HDL記述を生成する

        :param VerilogWriter writer: Verilog-HDL出力器
        """
        header = 'if ( {} ) begin'.format(self.cond.verilog_str)
        footer = 'end'
        with SimpleBlock(writer, header, footer):
            if self.then_body.is_null:
                writer.write_line(';')
            else:
                self.then_body.gen_verilog(writer)
        if not self.else_body.is_null:
            header = 'else begin'
            footer = 'end'
            with SimpleBlock(writer, header, footer):
                self.else_body.gen_verilog(writer)

    def gen_vhdl(self, writer):
        """VHDL記述を生成する

        :param VhdlWriter writer: VHDL出力器
        """
        header = 'if {} then'.format(self.cond.vhdl_str)
        if self.else_body.is_null:
            footer = 'end if;'
        else:
            footer = ''
        with SimpleBlock(writer, header, footer):
            if self.then_body.is_null:
                writer.write_line(';')
            else:
                self.then_body.gen_vhdl(writer)
        if not self.else_body.is_null:
            header = 'else'
            footer = 'end'
            with SimpleBlock(writer, header, footer):
                self.else_body.gen_vhdl(writer)


class CaseStatement(Statement):
    """Case 文を表すクラス
    """

    def __init__(self, cond):
        super().__init__()
        self.__cond = cond
        self.__case_list = []

    @property
    def type(self):
        """ステートメントの種類を返す．"""
        return StmtType.CaseStatement

    @property
    def cond(self):
        """条件式を返す．"""
        return self.__cond

    def add_label(self, label):
        """case節のラベルを追加する．

        :param Expr label: ラベル
        """
        block = StatementBlock()
        self.__case_list.append((label, block))
        return block

    @property
    def case_gen(self):
        """case節のジェネレータを返す．"""
        for case in self.__case_list:
            yield case

    def gen_verilog(self, writer):
        """Verilog-HDL記述を生成する

        :param VerilogWriter writer: Verilog-HDL出力器
        """
        header = 'case ( {} )'.format(self.cond.verilog_str)
        footer = 'endcase'
        with SimpleBlock(writer, header, footer):
            for label, body in self.__case_list:
                line = '{}:'.format(label.verilog_str)
                writer.write_line(line)
                with SimpleBlock(writer, '', ''):
                    body.gen_verilog(writer)

    def gen_vhdl(self, writer):
        """VHDL記述を生成する

        :param VhdlWriter writer: VHDL出力器
        """
        header = 'case {} is'.format(self.cond.vhdl_str)
        footer = 'end case'
        with SimpleBlock(writer, header, footer):
            for label, body in self.__case_list:
                pass


class StatementBlock:
    """Statement を保持するクラス
    """

    def __init__(self):
        self.__statement_list = []

    @property
    def is_null(self):
        if len(self.__statement_list) == 0:
            return True
        else:
            return False

    def add_assign(self, lhs, rhs,
                   *, blocking=False):
        """代入文を追加する．

        :param Expr lhs: 左辺式
        :param Expr rhs: 右辺式
        :param bool blocking: ブロッキング代入の時に True にする．
        :return: 生成したステートメントを返す．
        """
        if blocking:
            stmt = BlockingAssign(lhs, rhs)
        else:
            stmt = NonblockingAssign(lhs, rhs)
        self.__statement_list.append(stmt)
        return stmt

    def add_if(self, cond):
        """IF 文を追加する．

        :param Expr cond: 条件式
        :return: 生成したステートメントを返す．
        """
        stmt = IfStatement(cond)
        self.__statement_list.append(stmt)
        return stmt

    def add_case(self, cond):
        """CASE 文を追加する．

        :param Expr cond: 条件式
        :return 生成したステートメントを返す．
        """
        stmt = CaseStatement(cond)
        self.__statement_list.append(stmt)
        return stmt

    def gen_verilog(self, writer):
        """Verilog-HDL記述を生成する

        :param VerilogWriter writer: Verilog-HDL出力器
        """
        for statement in self.__statement_list:
            statement.gen_verilog(writer)

    def gen_vhdl(self, writer):
        """VHDL記述を生成する

        :param VhdlWriter writer: VHDL出力器
        """
        for statement in self.__statement_list:
            statement.gen_vhdl(writer)
