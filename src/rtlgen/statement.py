#! /usr/bin/env python3

"""Statement の定義

:file: statement.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2022 Yusuke Matsunaga, All rights reserved.
"""

from enum import Enum
from rtlgen.expr import Expr
from rtlgen.item_mgr import ItemMgr
from rtlgen.writer_base import SimpleBlock


class StmtType(Enum):
    """ステートメントの種類を表す列挙型"""
    BlockingAssign = 1
    NonblockingAssign = 2
    IfStatement = 3
    CaseStatement = 4
    WhileStatement = 5
    StatementBlock = 6


class StmtContext:
    """StatementBlock 用のコンテキストマネージャ
    """

    def __init__(self, statement):
        self.__statement = statement

    def __enter__(self):
        return self.__statement

    def __exit__(self, exc_type, exc_value, traceback):
        pass


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
        line = f'{self.lhs.verilog_str} = {self.rhs.verilog_str};'
        writer.write_line(line)

    def gen_vhdl(self, writer):
        """VHDL記述を生成する

        :param VhdlWriter writer: VHDL出力器
        """
        line = f'{self.lhs.vhdl_str} = {self.rhs.vhdl_str};'
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
        line = f'{self.lhs.verilog_str} <= {self.rhs.verilog_str};'
        writer.write_line(line)

    def gen_vhdl(self, writer):
        """VHDL記述を生成する

        :param VhdlWriter writer: VHDL出力器
        """
        line = f'{self.lhs.vhdl_str} <= {self.rhs.vhdl_str};'
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

    def then_body(self):
        """Then節を返す．"""
        return StmtContext(self.__then)

    def else_body(self):
        """Else節を返す．"""
        return StmtContext(self.__else)

    def gen_verilog(self, writer):
        """Verilog-HDL記述を生成する

        :param VerilogWriter writer: Verilog-HDL出力器
        """
        writer.write_line(f'if ( {self.cond.verilog_str} ) ', no_nl=True)
        self.__then.gen_verilog(writer)
        if not self.__else.is_null:
            writer.write_line('else ', no_nl=True)
            self.__else.gen_verilog(writer)

    def gen_vhdl(self, writer):
        """VHDL記述を生成する

        :param VhdlWriter writer: VHDL出力器
        """
        header = f'if {self.cond.vhdl_str} then'
        if self.__else.is_null:
            footer = 'end if;'
        else:
            footer = ''
        with SimpleBlock(writer, header, footer):
            if self.__then.is_null:
                writer.write_line(';')
            else:
                for stmt in self.__then.statement_gen:
                    stmt.gen_vhdl(writer)
        if not self.__else.is_null:
            header = 'else'
            footer = 'end'
            with SimpleBlock(writer, header, footer):
                for stmt in self.__else.statement_gen:
                    stmt.gen_vhdl(writer)


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
        return StmtContext(block)

    @property
    def case_gen(self):
        """case節のジェネレータを返す．"""
        for case in self.__case_list:
            yield case

    def gen_verilog(self, writer):
        """Verilog-HDL記述を生成する

        :param VerilogWriter writer: Verilog-HDL出力器
        """
        header = f'case ( {self.cond.verilog_str} )'
        footer = 'endcase'
        with SimpleBlock(writer, header, footer):
            for label, body in self.__case_list:
                line = f'{label.verilog_str}:'
                writer.write_line(line)
                with SimpleBlock(writer, '', ''):
                    body.gen_verilog(writer)

    def gen_vhdl(self, writer):
        """VHDL記述を生成する

        :param VhdlWriter writer: VHDL出力器
        """
        header = f'case {self.cond.vhdl_str} is'
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

    @property
    def statement_gen(self):
        for stmt in self.__statement_list:
            yield stmt

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
        header = 'begin'
        footer = 'end'
        with SimpleBlock(writer, header, footer):
            if self.is_null:
                writer.write_line(';')
            else:
                for statement in self.__statement_list:
                    statement.gen_verilog(writer)

    def gen_vhdl(self, writer):
        """VHDL記述を生成する

        :param VhdlWriter writer: VHDL出力器
        """
        header = 'begin'
        footer = 'end'
        with SimpleBlock(writer, header, footer):
            if self.is_null:
                writer.write_line(';')
            else:
                for statement in self.__statement_list:
                    statement.gen_vhdl(writer)


class NamedStatementBlock(StatementBlock):
    """Statement を保持するクラス(名前付き)
    """

    def __init__(self, name):
        super().__init__()
        self.__item_mgr = ItemMgr(name)

    @property
    def name(self):
        """名前を返す.

        :rtype: str
        """
        return self.__item_mgr.name

    def reg_item(self, item):
        """要素を登録する．

        :param Item item: 登録する要素
        """
        self.__item_mgr.reg_item(item)

    @property
    def net_num(self):
        """ネット数を返す．

        :rtype: int
        """
        return self.__item_mgr.net_num

    def net(self, pos):
        """pos 番目のネットを返す．

        :param int pos: 位置
        :rtype: Net
        :rise: AssertError (pos が範囲外)
        """
        return self.__item_mgr.net(pos)

    @property
    def net_gen(self):
        """ネットリストのジェネレーターを返す．"""
        return self.__item_mgr.net_gen

    def add_net(self, *, name=None, data_type=None, reg_type=False, src=None):
        """ネットを生成する．

        :param str Name: 名前(名前付きのオプション引数)
        :param DataType data_type: データタイプ(名前付きのオプション引数)
        :return: 生成したネットを返す．
        :rtype: Net
        """
        net = self.__item_mgr.add_net(name=name,
                                      data_type=data_type,
                                      reg_type=reg_type,
                                      src=src)
        if src is not None:
            self.connect(net, src)
        return net

    @property
    def var_num(self):
        """変数の数を返す．

        :rtype: int
        """
        return self.__item_mgr.var_num

    def var(self, pos):
        """pos 番目の変数を返す．

        :param int pos: 位置
        :rtype: Var
        :rise: AssertError (pos が範囲外)
        """
        return self.__item_mgr.var(pos)

    @property
    def var_gen(self):
        """変数リストのジェネレーターを返す．"""
        return self.__item_mgr.var_gen

    def add_var(self, *, name=None, data_type=None):
        """変数を生成する．

        :param str Name: 名前(名前付きのオプション引数)
        :param DataType data_type: データタイプ(名前付きのオプション引数)
        :return: 生成した変数を返す．
        :rtype: Var
        """
        return self.__item_mgr.add_var(name=name, data_type=data_type)

    def gen_verilog(self, writer):
        """Verilog-HDL記述を生成する

        :param VerilogWriter writer: Verilog-HDL出力器
        """
        header = f'begin: {self.name}'
        footer = 'end'
        with SimpleBlock(writer, header, footer):
            self.__item_mgr.gen_verilog(writer)
            if self.is_null:
                writer.write_line(';')
            else:
                for statement in self.__statement_list:
                    statement.gen_verilog(writer)
        for statement in self.__statement_list:
            statement.gen_verilog(writer)

    def gen_vhdl(self, writer):
        """VHDL記述を生成する

        :param VhdlWriter writer: VHDL出力器
        """
        header = f'begin: {self.name}'
        footer = 'end'
        with SimpleBlock(writer, header, footer):
            self.__item_mgr.gen_vhdl(writer)
            if self.is_null:
                writer.write_line(';')
            else:
                for statement in self.__statement_list:
                    statement.gen_vhdl(writer)
