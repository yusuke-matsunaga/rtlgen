#! /usr/bin/env python3

"""DataType クラスの定義.

:file: data_type.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: (C) 2021 Yusuke Matsunaga, All rights reserved.

RTLgen では基本データ型として以下の種類を定義している．

* BitType: ビット
* BitVectorType: (符号無し)ビットベクタ
* SignedBitVectorType: 符号付きビットベクタ
* ArrayType: 同種のデータ型の配列タイプ
* RecordType: 複数のデータ型を名前付きで集めたもの

実はBitVectorTypeはBitTypeを基本データ型としたArrayTypeと
同一だが，簡便性のためにあらかじめ用意している．

VHDLやVerilogの場合，ビットベクタのMSBとLSBを自由に指定できるが，
ここではLSBは常に0，MSBは size - 1 と固定している．
"""

from enum import Enum


class DataType:
    """データ型を表すクラス."""

    @property
    def is_bit_type(self):
        """bit 型の時 True を返す."""
        return False

    @property
    def is_bitvector_type(self):
        """bitvector 型の時 True を返す."""
        return False

    @property
    def is_signedbitvector_type(self):
        """signedbitvector 型の時 True を返す."""
        return False

    @property
    def is_integer_type(self):
        """integer 型の時 True を返す．"""
        return False

    @property
    def is_float_type(self):
        """float 型の時 True を返す．"""
        return False

    @property
    def is_array_type(self):
        """array 型の時 True を返す."""
        return False

    @property
    def is_record_type(self):
        """record 型の時 True を返す."""
        return False

    @staticmethod
    def bit_type():
        """BitType を返す．"""
        return BitType()

    @staticmethod
    def bitvector_type(size):
        """BitVectorType を返す．

        :param int size: サイズ
        """
        return BitVectorType(size)

    @staticmethod
    def signed_bitvector_type(size):
        """SignedBitVectorType を返す．

        :param int size: サイズ
        """
        return SignedBitVectorType(size)

    @staticmethod
    def integer_type():
        """IntegerType を返す．"""
        return IntegerType()

    @staticmethod
    def float_type():
        """FloatType を返す．"""
        return FloatType()

    @staticmethod
    def array_type(subtype, size):
        """ArrayType を返す．

        :param DataType subtype: 要素の型
        :param int size: 要素数
        """
        return ArrayType(subtype, size)

    @staticmethod
    def record_type(rdict):
        """RecordType を返す．

        :param dict[str, DataType] rdict: レコードの辞書
        """
        return RecordType(rdict)

    @staticmethod
    def bitlen(max_val):
        """最大値から必要なビット長を計算する．

        :param int max_val: 最大値
        :return: max_val を表すのに必要なビット数
        """

        ans = 0
        while (1 << ans) < max_val:
            ans += 1
        return ans


class BitType(DataType):
    """bit型を表すクラス."""

    @property
    def is_bit_type(self):
        """bit 型の時 True を返す."""
        return True

    def __eq__(self, other):
        """等価比較演算子"""
        return isinstance(other, BitType)

    def __str__(self):
        """内容を表す文字列を返す．"""
        return "BitType"


class SizedType(DataType):
    """サイズを持つ型に共通の基底クラス.

    :param int size: 要素サイズ
    """

    def __init__(self, size):
        assert(isinstance(size, int))
        self.__size = size

    @property
    def size(self):
        """要素サイズを返す."""
        return self.__size


class BitVectorType(SizedType):
    """bitvector型を表すクラス.

    :param int size: ベクタサイズ

    LSB が 0，MSB が (size - 1) であるビットベクタ型を作る．
    """

    def __init__(self, size):
        super().__init__(size)

    @property
    def is_bitvector_type(self):
        """bitvector 型の時 True を返す."""
        return True

    def __eq__(self, other):
        """等価比較演算子

        サイズが同じBitVectorTypeを等価と見なしている．
        """
        return isinstance(other, BitVectorType) and \
            self.size == other.size

    def __str__(self):
        """内容を表す文字列を返す．"""
        return "BitVectorType[{}]".format(self.size)


class SignedBitVectorType(SizedType):
    """signed_bitvector型を表すクラス

    :param int size: ベクタサイズ

    LSB が 0，MSB が (size - 1) である符号付きビットベクタ型を作る．
    """

    def __init__(self, size):
        super().__init__(size)

    @property
    def is_signedbitvector_type(self):
        """signedbitvector型の時 True を返す．"""
        return True

    def __eq__(self, other):
        """等価比較演算子

        サイズが同じSignedBitVectorTypeを等価と見なしている．
        """
        return isinstance(other, SignedBitVectorType) and \
            self.size == other.size

    def __str__(self):
        """内容を表す文字列を返す．"""
        return "SignedBitVectorType[{}]".format(self.size)


class IntegerType(DataType):
    """integer 型を表すクラス."""

    @property
    def is_integer_type(self):
        """integer 型の時 True を返す."""
        return True

    def __eq__(self, other):
        """等価比較演算子"""
        return isinstance(other, IntegerType)

    def __str__(self):
        """内容を表す文字列を返す．"""
        return "IntegerType"


class FloatType(DataType):
    """float 型を表すクラス."""

    @property
    def is_float_type(self):
        """float 型の時 True を返す."""
        return True

    def __eq__(self, other):
        """等価比較演算子"""
        return isinstance(other, FloatType)

    def __str__(self):
        """内容を表す文字列を返す．"""
        return "FloatType"


class ArrayType(SizedType):
    """array型を表すクラス

    :param DataType subtype: 要素の型
    :param int size: 要素のサイズ

    0 から (size - 1) の要素を持つ配列型を作る．
    """

    def __init__(self, subtype, size):
        super().__init__(size)
        self.__subtype = subtype

    @property
    def is_array_type(self):
        """array 型の時 True を返す."""
        return True

    @property
    def subtype(self):
        """要素の型を返す."""
        return self.__subtype

    def __eq__(self, other):
        """等価比較演算子

        サイズと要素の型が同じArrayTypeを等価と見なしている．
        """
        return isinstance(other, ArrayType) and \
            self.size == other.size and \
            self.subtype == other.subtype

    def __str__(self):
        """内容を表す文字列を返す．"""
        return "ArrayType[{} x {}]".format(self.subtype, self.size)


class RecordType(DataType):
    """record型を表すクラス

    :param rdict: レコード名と型の辞書
    :type rdict: dict[str, DataType]

    個々のレコード名と型を要素として持つ複合型を作る．
    """

    def __init__(self, rdict):
        self.__rdict = dict(rdict)

    @property
    def is_record_type(self):
        """record 型の時 True を返す."""
        return True

    @property
    def record_list(self):
        """レコード名のリストを返す.

        :rtype: list[str]

        python の dict の実装の都合上，名前の順に規則性はない．
        """
        return self.__rdict.keys()

    def record_type(self, record_name):
        """レコード名から型を得る.

        :param str record_name: レコード名
        :rtype: DataType or None

        存在しない場合には None を返す．
        """
        if record_name in self.__rdict:
            return self.__rdict[record_name]
        else:
            return None

    def __eq__(self, other):
        """等価比較演算子

        要素の辞書が等価なRecordTypeを等価と見なしている．
        """
        return isinstance(other, RecordType) and \
            self.__rdict == other.__rdict

    def __str__(self):
        """内容を表す文字列を返す．"""
        ans = "RecordType["
        for key in sorted(self.record_list):
            subtype = self.record_type(key)
            ans += "{}:{}".format(key, subtype)
        ans += "]"
        return ans
