#! /usr/bin/env python3

"""式の定義.

:file: expr.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: (C) 2021 Yusuke Matsunaga, All rights reserved.
"""

from enum import Enum
import numpy as np
from rtlgen.data_type import DataType


class OpType(Enum):
    """演算の種類を表す列挙型"""
    NOT = 1
    AND = 2
    NAND = 3
    OR = 4
    NOR = 5
    XOR = 6
    XNOR = 7
    RAND = 8
    RNAND = 9
    ROR = 10
    RNOR = 11
    RXOR = 12
    RXNOR = 13
    COMPL = 14
    ADD = 15
    SUB = 16
    MUL = 17
    DIV = 18
    MOD = 19
    LSFT = 20
    RSFT = 21
    BSEL = 22
    PSEL = 23
    RSEL = 24
    EQ = 25
    NE = 26
    LT = 27
    LE = 28
    LAND = 29
    LOR = 30
    LNOT = 31


class ExprHandle:
    """式を保持するオブジェクト"""

    def __init__(self, src=None):
        self.__ptr = None
        self.set(src)

    def set(self, expr):
        """値をセットする．"""
        prev = self.__ptr
        if prev is not None:
            # 以前の値をクリアする．
            prev.del_ref(self)
        self.__ptr = expr
        if expr is not None:
            expr.add_ref(self)

    @property
    def val(self):
        """値を返す．"""
        return self.__ptr


class Expr:
    """式を表す基底クラス.

    このクラスを定義する目的は Python の演算子を適用可能
    にするために特殊メソッドを定義するため.
    """

    def is_simple(self):
        """単純な式の時に True を返す．
        """
        return False
    
    @staticmethod
    def make_not(opr1):
        """bitwise NOT演算を作る.

        :param Expr opr1: オペランド
        :return: 作成した演算子を返す．
        :rtype: BinaryOp
        """
        return UnaryOp(OpType.NOT, opr1)

    @staticmethod
    def make_and(opr1, opr2):
        """bitwise AND演算を作る.

        :param Expr opr1: 第1オペランド
        :param Expr opr2: 第2オペランド
        :return: 作成した演算子を返す．
        :rtype: BinaryOp
        """
        return BinaryOp(OpType.AND, opr1, opr2)

    @staticmethod
    def make_or(opr1, opr2):
        """bitwise OR演算を作る.

        :param Expr opr1: 第1オペランド
        :param Expr opr2: 第2オペランド
        :return: 作成した演算子を返す．
        :rtype: BinaryOp
        """
        return BinaryOp(OpType.OR, opr1, opr2)

    @staticmethod
    def make_xor(opr1, opr2):
        """bitwise XOR演算を作る.

        :param Expr opr1: 第1オペランド
        :param Expr opr2: 第2オペランド
        :return: 作成した演算子を返す．
        :rtype: BinaryOp
        """
        return BinaryOp(OpType.XOR, opr1, opr2)

    @staticmethod
    def make_nand(opr1, opr2):
        """bitwise NAND演算を作る.

        :param Expr opr1: 第1オペランド
        :param Expr opr2: 第2オペランド
        :return: 作成した演算子を返す．
        :rtype: BinaryOp
        """
        return BinaryOp(OpType.NAND, opr1, opr2)

    @staticmethod
    def make_nor(opr1, opr2):
        """bitwise NOR演算を作る.

        :param Expr opr1: 第1オペランド
        :param Expr opr2: 第2オペランド
        :return: 作成した演算子を返す．
        :rtype: BinaryOp
        """
        return BinaryOp(OpType.NOR, opr1, opr2)

    @staticmethod
    def make_xnor(opr1, opr2):
        """bitwise XNOR演算を作る.

        :param Expr opr1: 第1オペランド
        :param Expr opr2: 第2オペランド
        :return: 作成した演算子を返す．
        :rtype: BinaryOp
        """
        return BinaryOp(OpType.XNOR, opr1, opr2)

    @staticmethod
    def make_uminus(opr1):
        """単項マイナス演算を作る.

        :param Expr opr1: オペランド
        :return: 作成した演算子を返す．
        :rtype: UnaryOp
        """
        return UnaryOp(OpType.COMPL, opr1)

    @staticmethod
    def make_add(opr1, opr2):
        """加算を作る.

        :param Expr opr1: 第1オペランド
        :param Expr opr2: 第2オペランド
        :return: 作成した演算子を返す．
        :rtype: BinaryOp
        """
        return BinaryOp(OpType.ADD, opr1, opr2)

    @staticmethod
    def make_sub(opr1, opr2):
        """減算を作る.

        :param Expr opr1: 第1オペランド
        :param Expr opr2: 第2オペランド
        :return: 作成した演算子を返す．
        :rtype: BinaryOp
        """
        return BinaryOp(OpType.SUB, opr1, opr2)

    @staticmethod
    def make_mul(opr1, opr2):
        """乗算を作る.

        :param Expr opr1: 第1オペランド
        :param Expr opr2: 第2オペランド
        :return: 作成した演算子を返す．
        :rtype: BinaryOp
        """
        return BinaryOp(OpType.MUL, opr1, opr2)

    @staticmethod
    def make_div(opr1, opr2):
        """除算を作る.

        :param Expr opr1: 第1オペランド
        :param Expr opr2: 第2オペランド
        :return: 作成した演算子を返す．
        :rtype: BinaryOp
        """
        return BinaryOp(OpType.DIV, opr1, opr2)

    @staticmethod
    def make_mod(opr1, opr2):
        """剰余算を作る.

        :param Expr opr1: 第1オペランド
        :param Expr opr2: 第2オペランド
        :return: 作成した演算子を返す．
        :rtype: BinaryOp
        """
        return BinaryOp(OpType.MOD, opr1, opr2)

    @staticmethod
    def make_lsft(opr1, opr2):
        """左シフト演算を作る.

        :param Expr opr1: 第1オペランド
        :param Expr opr2: 第2オペランド
        :return: 作成した演算子を返す．
        :rtype: BinaryOp
        """
        return BinaryOp(OpType.LSFT, opr1, opr2)

    @staticmethod
    def make_rsft(opr1, opr2):
        """右シフト演算を作る.

        :param Expr opr1: 第1オペランド
        :param Expr opr2: 第2オペランド
        :return: 作成した演算子を返す．
        :rtype: BinaryOp
        """
        return BinaryOp(OpType.RSFT, opr1, opr2)

    @staticmethod
    def make_eq(opr1, opr2):
        """等価比較演算を作る.

        :param Expr opr1: 第1オペランド
        :param Expr opr2: 第2オペランド
        :return: 作成した演算子を返す．
        :rtype: BinaryOp
        """
        return BinaryOp(OpType.EQ, opr1, opr2)

    @staticmethod
    def make_ne(opr1, opr2):
        """不等価比較演算を作る.

        :param Expr opr1: 第1オペランド
        :param Expr opr2: 第2オペランド
        :return: 作成した演算子を返す．
        :rtype: BinaryOp
        """
        return BinaryOp(OpType.NE, opr1, opr2)

    @staticmethod
    def make_lt(opr1, opr2):
        """小なり比較演算を作る.

        :param Expr opr1: 第1オペランド
        :param Expr opr2: 第2オペランド
        :return: 作成した演算子を返す．
        :rtype: BinaryOp
        """
        return BinaryOp(OpType.LT, opr1, opr2)

    @staticmethod
    def make_gt(opr1, opr2):
        """大なり比較演算を作る.

        :param Expr opr1: 第1オペランド
        :param Expr opr2: 第2オペランド
        :return: 作成した演算子を返す．
        :rtype: BinaryOp
        """
        return BinaryOp(OpType.LT, opr2, opr1)

    @staticmethod
    def make_le(opr1, opr2):
        """小なりイコール比較演算を作る.

        :param Expr opr1: 第1オペランド
        :param Expr opr2: 第2オペランド
        :return: 作成した演算子を返す．
        :rtype: BinaryOp
        """
        return BinaryOp(OpType.LE, opr1, opr2)

    @staticmethod
    def make_ge(opr1, opr2):
        """大なりイコール比較演算を作る.

        :param Expr opr1: 第1オペランド
        :param Expr opr2: 第2オペランド
        :return: 作成した演算子を返す．
        :rtype: BinaryOp
        """
        return BinaryOp(OpType.LE, opr2, opr1)

    @staticmethod
    def make_lnot(opr1):
        """NOT演算を作る.

        :param Expr opr1: オペランド
        :return: 作成した演算子を返す．
        :rtype: UnaryOp
        """
        return UnaryOp(OpType.LNOT, opr1)

    @staticmethod
    def make_land(opr1, opr2):
        """AND演算を作る.

        :param Expr opr1: 第1オペランド
        :param Expr opr2: 第2オペランド
        :return: 作成した演算子を返す．
        :rtype: BinaryOp
        """
        return BinaryOp(OpType.LAND, opr1, opr2)

    @staticmethod
    def make_lor(opr1, opr2):
        """OR演算を作る.

        :param Expr opr1: 第1オペランド
        :param Expr opr2: 第2オペランド
        :return: 作成した演算子を返す．
        :rtype: BinaryOp
        """
        return BinaryOp(OpType.LOR, opr1, opr2)

    @staticmethod
    def make_zero():
        """1ビットの0を作る．
        """
        return Constant(data_type=DataType.bit_type(), val=0)

    @staticmethod
    def make_one():
        """1ビットの1を作る．
        """
        return Constant(data_type=DataType.bit_type(), val=1)

    @staticmethod
    def make_constant(*, data_type=DataType.bit_type(), val):
        """定数を作る．

        :param DataType data_type: データ型
        :param int val: 値
        """
        return Constant(data_type=data_type, val=val)

    @staticmethod
    def make_intconstant(val):
        """int型の定数を作る．

        :param int val: 値
        """
        return IntConstant(val)

    @staticmethod
    def bit_select(primary, index):
        """ビット選択演算を作る．

        :param Expr primary: 選択対象の式
        :param Expr index: インデックス
        :rtype: BitSelect
        """
        if isinstance(index, int):
            index = IntConstant(index)
        return BitSelect(primary, index)

    @staticmethod
    def part_select(primary, left, right):
        """範囲選択演算を作る．

        :param Expr primary: 選択対象の式
        :param Expr left: 左の範囲
        :param Expr right: 右の範囲
        :rtype: PartSelect
        """
        assert(isinstance(left, int))
        assert(isinstance(right, int))
        return PartSelect(primary, left, right)

    @staticmethod
    def concat(expr_list):
        """連結演算

        :param list(Expr) expr_list: 式のリスト
        :rtype: Concat
        """
        return Concat(expr_list)

    @staticmethod
    def multi_concat(rep_num, expr_list):
        """繰り返し連結演算

        :param int rep_num: 繰り返し数
        :param list(Expr) expr_list: 式のリスト
        :rtype: MultiConcat
        """
        return MultiConcat(rep_num, expr_list)

    @staticmethod
    def extension(src, dst_size):
        """ビット拡張を行う．

        :param Expr src: ソースの式
        :param int dst_size: 結果のビット幅
        """
        src_type = src.data_type
        if src_type.size == dst_size:
            # 結果も同じ型なら src を返す．
            return src
        n = dst_size - src_type.size
        assert n > 0
        # 上位に0を詰めて拡張する．
        return Expr.concat([Constant(DataType.bitvector_type(n), 0), src])

    @staticmethod
    def sign_extension(src, dst_size):
        """符号付きのビット拡張を行う．

        :param Expr src: ソースの式
        :param int dst_size: 結果のビット幅
        """
        src_type = src.data_type
        if src_type.size == dst_size:
            # 結果も同じ型なら src を返す．
            return src
        n = dst_size - src_type.size
        assert n > 0
        # 符号拡張を行う．
        msb = src_type.size - 1
        src_list = []
        msb_expr = Expr.bit_select(src, msb)
        src_list.append(Expr.multi_concat(n, [msb_expr]))
        src_list.append(src)
        return Expr.concat(src_list)

    def __init__(self):
        self.__ref_list = []

    def __invert__(self):
        """NOT演算"""
        return Expr.make_not(self)

    def __and__(self, other):
        """bitwise AND演算子

        :param other: 右側のオペランド
        other は Expr 型に変換可能である必要がある．
        """
        other = self.coerce(other)
        assert isinstance(other, Expr)
        return Expr.make_and(self, other)

    def __rand__(self, other):
        """bitwise AND演算

        :param other: 左側のオペランド
        other は Expr 型に変換可能である必要がある．
        右側のオペランドが Expr 型
        """
        other = self.coerce(other)
        assert isinstance(other, Expr)
        return Expr.make_and(other, self)

    def __or__(self, other):
        """bitwise OR演算"""
        other = self.coerce(other)
        assert isinstance(other, Expr)
        return Expr.make_or(self, other)

    def __ror__(self, other):
        """bitwise OR演算

        右側のオペランドが Expr 型
        """
        other = self.coerce(other)
        assert isinstance(other, Expr)
        return Expr.make_or(other, self)

    def __xor__(self, other):
        """bitwise XOR演算"""
        other = self.coerce(other)
        assert isinstance(other, Expr)
        return Expr.make_xor(self, other)

    def __rxor__(self, other):
        """bitwise XOR演算

        右側のオペランドが Expr 型
        """
        other = self.coerce(other)
        assert isinstance(other, Expr)
        return Expr.make_xor(other, self)

    def __neg__(self):
        """単項マイナス演算"""
        return Expr.make_uminus(self)

    def __pos__(self):
        """単項プラス演算"""
        # そのまま返す．
        return self

    def __add__(self, other):
        """加算"""
        other = self.coerce(other)
        assert isinstance(other, Expr)
        return Expr.make_add(self, other)

    def __radd__(self, other):
        """加算

        右側のオペランドが Expr 型
        """
        other = self.coerce(other)
        assert isinstance(other, Expr)
        return Expr.make_add(other, self)

    def __sub__(self, other):
        """減算"""
        other = self.coerce(other)
        assert isinstance(other, Expr)
        return Expr.make_sub(self, other)

    def __rsub__(self, other):
        """減算

        右側のオペランドが Expr 型
        """
        other = self.coerce(other)
        assert isinstance(other, Expr)
        return Expr.make_sub(other, self)

    def __mul__(self, other):
        """乗算"""
        other = self.coerce(other)
        assert isinstance(other, Expr)
        return Expr.make_mul(self, other)

    def __rmul__(self, other):
        """乗算

        右側のオペランドが Expr 型
        """
        other = self.coerce(other)
        assert isinstance(other, Expr)
        return Expr.make_mul(other, self)

    def __truediv__(self, other):
        """除算"""
        other = self.coerce(other)
        assert isinstance(other, Expr)
        return Expr.make_div(self, other)

    def __rtruediv__(self, other):
        """除算

        右側のオペランドが Expr 型
        """
        other = self.coerce(other)
        assert isinstance(other, Expr)
        return Expr.make_div(other, self)

    def __mod__(self, other):
        """剰余算"""
        other = self.coerce(other)
        assert isinstance(other, Expr)
        return Expr.make_mod(self, other)

    def __rmod__(self, other):
        """剰余算

        右側のオペランドが Expr 型
        """
        other = self.coerce(other)
        assert isinstance(other, Expr)
        return Expr.make_mod(other, self)

    def __lshift__(self, other):
        """左シフト演算"""
        other = self.coerce(other)
        assert isinstance(other, Expr)
        return Expr.make_lsft(self, other)

    def __rlshift__(self, other):
        """左シフト演算

        右側のオペランドが Expr 型
        """
        other = self.coerce(other)
        assert isinstance(other, Expr)
        return Expr.make_lsft(other, self)

    def __rshift__(self, other):
        """右シフト演算"""
        other = self.coerce(other)
        assert isinstance(other, Expr)
        return Expr.make_rsft(self, other)

    def __rrshift__(self, other):
        """右シフト演算

        右側のオペランドが Expr 型
        """
        other = self.coerce(other)
        assert isinstance(other, Expr)
        return Expr.make_rsft(other, self)

    def __eq__(self, other):
        """等価比較演算"""
        other = self.coerce(other)
        assert isinstance(other, Expr)
        return Expr.make_eq(self, other)

    def __ne__(self, other):
        """不等価比較演算"""
        other = self.coerce(other)
        assert isinstance(other, Expr)
        return Expr.make_ne(self, other)

    def __lt__(self, other):
        """小なり比較演算"""
        other = self.coerce(other)
        assert isinstance(other, Expr)
        return Expr.make_lt(self, other)

    def __gt__(self, other):
        """大なり比較演算"""
        other = self.coerce(other)
        assert isinstance(other, Expr)
        return Expr.make_lt(other, self)

    def __le__(self, other):
        """小なりイコール比較演算"""
        other = self.coerce(other)
        assert isinstance(other, Expr)
        return Expr.make_le(self, other)

    def __ge__(self, other):
        """大なりイコール比較演算"""
        other = self.coerce(other)
        assert isinstance(other, Expr)
        return Expr.make_le(other, self)

    def coerce(self, other):
        """int 型を Constant に変換する."""
        if isinstance(other, Expr):
            return other
        else:
            data_type = self.data_type
            return Constant(data_type=data_type, val=other)

    def add_ref(self, ref):
        self.__ref_list.append(ref)

    def del_ref(self, ref):
        self.__ref_list.remove(ref)

    @property
    def needs_net(self):
        """ネット生成の必要があるとき True を返す．"""
        if self.ref_num > 1:
            return True
        else:
            return False

    @property
    def ref_num(self):
        """参照数を返す．"""
        return len(self.__ref_list)

    @property
    def ref_list(self):
        """参照元(ExprHandle)のリストを返す．"""
        return self.__ref_list

    @property
    def ref0(self):
        """最初の参照元を返す．"""
        return self.__ref_list[0].val


class OpBase(Expr):
    """演算子を表すクラス

    :param OpType op_type: 演算子の型
    """

    def __init__(self, op_type):
        super().__init__()
        self.__type = op_type

    @property
    def op_type(self):
        """演算子の型を返す.

        :rtype: OpType
        """
        return self.__type


class UnaryOp(OpBase):
    """単項演算子を表すクラス

    :param OpType: op_type 演算子の型
    :param Expr opr1: オペランド
    """

    def __init__(self, op_type, opr1):
        super().__init__(op_type)
        self.__opr1 = ExprHandle(opr1)

    @property
    def operand1(self):
        """第一オペランドを返す.

        :rtype: Expr
        """
        return self.__opr1.val

    @property
    def data_type(self):
        """データ型を返す.

        :rtype: DataType
        """
        return self.operand1.data_type

    @property
    def verilog_str(self):
        """Verilog-HDL の式を表す文字列を返す．"""
        str1 = self.operand1.verilog_str
        if self.op_type == OpType.NOT:
            op_str = '~'
        elif self.op_type == OpType.RAND:
            op_str = '&'
        elif self.op_type == OpType.RNAND:
            op_str = '~&'
        elif self.op_type == OpType.ROR:
            op_str = '|'
        elif self.op_type == OpType.RNOR:
            op_str = '~|'
        elif self.op_type == OpType.RXOR:
            op_str = '^'
        elif self.op_type == OpType.RXNOR:
            op_str = '~^'
        elif self.op_type == OpType.COMPL:
            op_str = '-'
        elif self.op_type == OpType.LNOT:
            op_str = '!'
        else:
            assert False
        if self.operand1.is_simple():
            return f'{op_str}{str1}'
        else:
            return f'({op_str}{str1})'

    @property
    def vhdl_str(self):
        """VHDL の式を表す文字列を返す．"""
        str1 = self.operand1.vhdl_str
        if self.op_type == OpType.NOT:
            op_str = '~'
        elif self.op_type == OpType.RAND:
            op_str = '&'
        elif self.op_type == OpType.RNAND:
            op_str = '~&'
        elif self.op_type == OpType.ROR:
            op_str = '|'
        elif self.op_type == OpType.RNOR:
            op_str = '~|'
        elif self.op_type == OpType.RXOR:
            op_str = '^'
        elif self.op_type == OpType.RXNOR:
            op_str = '~^'
        elif self.op_type == OpType.COMPL:
            op_str = '-'
        elif self.op_type == OpType.LNOT:
            op_str = '!'
        else:
            assert False
        if self.operand1.is_simple():
            return f'{op_str}{str1}'
        else:
            return f'({op_str}{str1})'


class BinaryOp(OpBase):
    """二項演算子を表すクラス

    :param OpType op_type: 演算子の型
    :param Expr opr1: 第一オペランド
    :param Expr opr2: 第二オペランド
    """

    def __init__(self, op_type, opr1, opr2):
        super().__init__(op_type)
        self.__opr1 = ExprHandle(opr1)
        self.__opr2 = ExprHandle(opr2)

    @property
    def operand1(self):
        """第一オペランドを返す.

        :rtype: Expr
        """
        return self.__opr1.val

    @property
    def operand2(self):
        """第二オペランドを返す.

        :rtype: Expr
        """
        return self.__opr2.val

    @property
    def data_type(self):
        """データ型を返す.

        :rtype: DataType
        """
        return self.operand1.data_type

    @property
    def verilog_str(self):
        """Verilog-HDL の式を表す文字列を返す．"""
        str1 = self.operand1.verilog_str
        str2 = self.operand2.verilog_str
        if self.op_type == OpType.AND:
            op_str = '&'
        elif self.op_type == OpType.NAND:
            op_str = '~&'
        elif self.op_type == OpType.OR:
            op_str = '|'
        elif self.op_type == OpType.NOR:
            op_str = '~|'
        elif self.op_type == OpType.XOR:
            op_str = '^'
        elif self.op_type == OpType.XNOR:
            op_str = '~^'
        elif self.op_type == OpType.ADD:
            op_str = '+'
        elif self.op_type == OpType.SUB:
            op_str = '-'
        elif self.op_type == OpType.MUL:
            op_str = '*'
        elif self.op_type == OpType.DIV:
            op_str = '/'
        elif self.op_type == OpType.MOD:
            op_str = '%'
        elif self.op_type == OpType.LSFT:
            op_str = '<<'
        elif self.op_type == OpType.RSFT:
            op_str = '>>'
        elif self.op_type == OpType.EQ:
            op_str = '=='
        elif self.op_type == OpType.NE:
            op_str = '!='
        elif self.op_type == OpType.LT:
            op_str = '<'
        elif self.op_type == OpType.LE:
            op_str = '<='
        elif self.op_type == OpType.LAND:
            op_str = '&&'
        elif self.op_type == OpType.LOR:
            op_str = '||'
        else:
            assert False
        return f'({str1} {op_str} {str2})'

    @property
    def vhdl_str(self):
        """VHDL の式を表す文字列を返す．"""
        str1 = self.operand1.vhdl_str
        str2 = self.operand2.vhdl_str
        if self.op_type == OpType.AND:
            op_str = '&'
        elif self.op_type == OpType.NAND:
            op_str = '~&'
        elif self.op_type == OpType.OR:
            op_str = '|'
        elif self.op_type == OpType.NOR:
            op_str = '~|'
        elif self.op_type == OpType.XOR:
            op_str = '^'
        elif self.op_type == OpType.XNOR:
            op_str = '~^'
        elif self.op_type == OpType.ADD:
            op_str = '+'
        elif self.op_type == OpType.SUB:
            op_str = '-'
        elif self.op_type == OpType.MUL:
            op_str = '*'
        elif self.op_type == OpType.DIV:
            op_str = '/'
        elif self.op_type == OpType.MOD:
            op_str = '%'
        elif self.op_type == OpType.LSFT:
            op_str = '<<'
        elif self.op_type == OpType.RSFT:
            op_str = '>>'
        elif self.op_type == OpType.EQ:
            op_str = '='
        elif self.op_type == OpType.NE:
            op_str = '!='
        elif self.op_type == OpType.LT:
            op_str = '<'
        elif self.op_type == OpType.LE:
            op_str = '<='
        elif self.op_type == OpType.LAND:
            op_str = '&&'
        elif self.op_type == OpType.LOR:
            op_str = '||'
        else:
            assert False
        return f'({str1} {op_str} {str2})'


class Constant(Expr):
    """定数を表すクラス

    :param DataType data_type: データ型
    :param int val: 値
    """

    def __init__(self, *, data_type, val):
        super().__init__()
        self.__type = data_type
        self.__val = val
        assert type(val) == int

    @property
    def data_type(self):
        """データ型を返す.

        :rtype: DataType
        """
        return self.__type

    @property
    def value(self):
        """値を返す.

        :rtype: int
        """
        return self.__val

    def bit_value(self, bit):
        """ビットの値を返す．

        :param int bit: 対象のビット
        :return: bit の位置の値(True|False) を返す．
        """
        if isinstance(self.value, np.uint64):
            mask = np.uint64(1 << bit)
        else:
            mask = (1 << bit)
        if self.value & mask:
            return True
        else:
            return False

    @property
    def verilog_str(self):
        """Verilog-HDL の式を表す文字列を返す．"""
        if self.data_type.is_bit_type:
            return f"1'b{self.value}"
        elif self.data_type.is_bitvector_type:
            size = self.data_type.size
            ans = f"{size}'b"
            for i in range(size):
                if self.bit_value(size - i - 1):
                    ans += "1"
                else:
                    ans += "0"
            return ans
        elif self.data_type.is_signedbitvector_type:
            size = self.data_type.size
            ans = f"{size}'sb"
            for i in range(size):
                if self.bit_value(size - i - 1):
                    ans += "1"
                else:
                    ans += "0"
            return ans
        elif self.data_type.is_integer_type:
            return str(self.value)
        elif self.data_type.is_float_type:
            return str(self.value)
        else:
            assert False

    @property
    def vhdl_str(self):
        """VHDL の式を表す文字列を返す．"""
        if self.data_type.is_bit_type:
            return "'" + str(self.value) + "'"
        elif self.data_type.is_bitvector_type:
            size = self.data_type.size
            ans = '"'
            for i in range(size):
                if self.bit_value(size - i - 1):
                    ans += '1'
                else:
                    ans += '0'
            ans += '"'
            return ans
        elif self.data_type.is_signedbitvector_type:
            size = self.data_type.size
            ans = '"'
            for i in range(size):
                if self.bit_value(size - i - 1):
                    ans += '1'
                else:
                    ans += '0'
            ans += '"'
            return ans
        elif self.data_type.is_integer_type:
            return "'" + str(self.value) + "'"
        elif self.data_type.is_float_type:
            return "'" + str(self.value) + "'"
        else:
            assert False


class IntConstant(Constant):
    """integer 型の定数を表すクラス

    :param int val: 値
    """

    def __init__(self, val):
        super().__init__(data_type=DataType.integer_type(), val=val)


class BitSelect(Expr):
    """ビット選択演算を表すクラス

    :param Expr primary: 対象の式
    :param Expr index: インデックス
    """

    def __init__(self, primary, index):
        super().__init__()
        self.__primary = primary
        self.__index = index

    @property
    def data_type(self):
        """データ型を返す.

        :rtype: DataType
        """
        return DataType.bit_type()

    @property
    def primary(self):
        """対象の式を返す．"""
        return self.__primary

    @property
    def index(self):
        """インデックスを返す．"""
        return self.__index

    @property
    def verilog_str(self):
        """Verilog-HDL の式を表す文字列を返す．"""
        ans = f'{self.primary.verilog_str}[{self.index.verilog_str}]'
        return ans

    @property
    def vhdl_str(self):
        """VHDL の式を表す文字列を返す．"""
        ans = f'{self.primary.verilog_str}({self.index.verilog_str})'
        return ans


class PartSelect(Expr):
    """範囲選択演算を表すクラス

    :param Expr primary: 対象の式
    :param Expr left: 左の範囲
    :param Expr right: 右の範囲
    """

    def __init__(self, primary, left, right):
        super().__init__()
        assert(isinstance(left, int))
        assert(isinstance(right, int))
        self.__primary = primary
        self.__left = left
        self.__right = right
        if left > right:
            direction = "down"
        else:
            direction = "up"
        self.__direction = direction

    @property
    def data_type(self):
        """データ型を返す.

        :rtype: DataType
        """
        if self.left > self.right:
            w = self.left - self.right
        else:
            w = self.right - self.left
        return DataType.bitvector_type(w + 1)

    @property
    def primary(self):
        """対象の式を返す．"""
        return self.__primary

    @property
    def left(self):
        """左の範囲を返す．"""
        return self.__left

    @property
    def right(self):
        """右の範囲を返す．"""
        return self.__right

    @property
    def direction(self):
        """向きを返す．"""
        return self.__direction

    @property
    def verilog_str(self):
        """Verilog-HDL の式を表す文字列を返す．"""
        ans = f'{self.primary.verilog_str}[{self.left}:{self.right}]'
        return ans

    @property
    def vhdl_str(self):
        """VHDL の式を表す文字列を返す．"""
        if self.direction == "up":
            to_str = "to"
        elif self.direction == "down":
            to_str = "downto"
        else:
            assert False
        ans = f'{self.primary.vhdl_str}({self.left} {to_str} {self.right})'
        return ans


class Concat(Expr):
    """連結演算子"""

    def __init__(self, src_list):
        super().__init__()
        self.__src_list = src_list[:]

    @property
    def data_type(self):
        """データ型を返す.

        :rtype: DataType
        """
        bw = 0
        for src in self.__src_list:
            assert src.data_type.is_bitvector_type
            bw += src.data_type.size
        return DataType.bitvector_type(bw)

    @property
    def src_list(self):
        return self.__src_list

    @property
    def verilog_str(self):
        """Verilog-HDL の式を表す文字列を返す．"""
        ans = '{'
        comma = ''
        for src in self.__src_list:
            ans += comma
            ans += src.verilog_str
            comma = ', '
        ans += '}'
        return ans

    @property
    def vhdl_str(self):
        """VHDL の式を表す文字列を返す．"""
        ans = '('
        comma = ''
        for src in self.__src_list:
            ans += comma
            ans += src.vhdl_str
            comma = ' & '
        ans += ')'
        return ans


class MultiConcat(Expr):
    """繰り返し連結演算子"""

    def __init__(self, rep_num, src_list):
        super().__init__()
        self.__rep_num = rep_num
        self.__src_list = src_list

    @property
    def data_type(self):
        """データ型を返す.

        :rtype: DataType
        """
        # 未完
        assert False

    @property
    def rep_num(self):
        """繰り返し数を返す．"""
        return self.__rep_num

    @property
    def src_list(self):
        return self.__src_list

    @property
    def verilog_str(self):
        """Verilog-HDL の式を表す文字列を返す．"""
        ans = '{'
        ans += f'{self.__rep_num}'
        ans += '{'
        comma = ''
        for src in self.__src_list:
            ans += comma
            ans += src.verilog_str
            comma = ', '
        ans += '}}'
        return ans

    @property
    def vhdl_str(self):
        """VHDL の式を表す文字列を返す．"""
        # VHDL には繰り返し連結演算子はないので
        # ここで直接展開する．
        ans = '('
        comma = ''
        for _ in range(self.__rep_num):
            for src in self.__src_list:
                ans += comma
                ans += src.vhdl_str
                comma = ' & '
        ans += ')'
        return ans
