#! /usr/bin/env python3

"""Dff の定義

:file: dff.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2022 Yusuke Matsunaga, All rights reserved.
"""

from rtlgen.process import ClockedProcess
from rtlgen.data_type import BitType
from rtlgen.entity import Entity
from rtlgen.expr import Expr


class Dff(ClockedProcess):
    """D-FF を表すクラス

    :param str name: 名前
    :param Expr data_in: データ入力
    :param DataType data_type: データ入力の型
    :param Expr clock: クロック入力
    :param str clock_edge: クロックのアクティブエッジを表す文字列
                  'positive' か 'negative'
    :param Expr reset: リセット入力
    :param str reset_pol: リセットの極性を表す文字列
                  'positive' か 'negative'
    :param Expr enable: イネーブル入力
    :param str enable_pol: イネーブル信号の極性を表す文字列
                  'positive' か 'negative'

    以下の入出力を持つ．
    * data_in: データ入力．タイプは任意
    * clock:   クロック入力．タイプは BitType
    * reset:   リセット入力(オプショナル)．タイプは BitType
    * enable:  イネーブル入力(オプショナル)．タイプはBitType
    * q:       出力．タイプは data_in と同じ．
    """

    def __init__(self, parent, *,
                 name=None,
                 data_in=None,
                 data_type=BitType,
                 clock,
                 clock_pol="positive",
                 reset=None,
                 reset_pol=None,
                 reset_val=None,
                 enable=None,
                 enable_pol=None):
        super().__init__(parent, name=name,
                         clock=clock, clock_pol=clock_pol,
                         asyncctl=reset, asyncctl_pol=reset_pol)
        # 入出力のネットを作る．
        if data_in is None:
            self.__data_in = self.add_net(data_type)
        else:
            data_type = data_in.data_type
            self.__data_in = data_in
        if reset_val is not None and isinstance(reset_val, int):
            reset_val = Expr.make_constant(data_type=data_type, val=reset_val)
        self.__reset_val = reset_val
        self.__enable_pol = enable_pol
        if enable_pol is not None:
            if enable is None:
                self.__enable = self.add_net(BitType)
            else:
                self.__enable = enable
        else:
            self.__enable = None
        self.__q = self.add_net(data_type, reg_type=True)

        # リセット動作を表す statement を作る．
        if self.reset is not None:
            with self.asyncctl_body() as _:
                _.add_assign(self.q, self.__reset_val)
        # 動作を表す statement を作る．
        if self.enable is None:
            with self.body() as _:
                _.add_assign(self.q, self.data_in)
        else:
            if self.__enable_pol == "positive":
                val = 1
            else:
                val = 0
            cond = Expr.make_eq(self.enable, Expr.make_constant(val=val))
            with self.body() as _:
                if_stmt = _.add_if(cond)
                with if_stmt.then_body() as _:
                    _.add_assign(self.q, self.data_in)

    @property
    def data_in(self):
        """データ入力のネットを返す．"""
        return self.__data_in

    @property
    def reset(self):
        """リセットのネットを返す．"""
        return self.asyncctl

    @property
    def enable(self):
        """イネーブルのネットを返す．"""
        return self.__enable

    @property
    def q(self):
        """データ出力のネットを返す．"""
        return self.__q

    @property
    def output(self):
        """データ出力のネットを返す．"""
        return self.__q


def add_dff(self, *,
            name=None,
            data_in=None,
            data_type=BitType,
            clock=None,
            clock_pol=None,
            reset=None,
            reset_pol=None,
            reset_val=None,
            enable=None,
            enable_pol=None):
    """Dff を追加する．

    :param str name: 名前
    :param Expr data_in: データ入力
    :param DataType data_type: データ入力の型
    :param Expr clock: クロック入力
    :param str clock_pol: クロックのアクティブエッジを表す文字列
                  'positive' か 'negative'
    :param Expr reset: リセット入力
    :param str reset_pol: リセットの極性を表す文字列
                  'positive' か 'negative'
    :param Expr enable: イネーブル入力
    :param str enable_pol: イネーブル信号の極性を表す文字列
                  'positive' か 'negative'
    """
    if clock is None:
        clock = self.default_clock
    if clock_pol is None:
        clock_pol = self.default_clock_pol
    if reset is None:
        reset = self.default_reset
    if reset_pol is None:
        reset_pol = self.default_reset_pol
    dff = Dff(self, name=name, data_in=data_in, data_type=data_type,
              clock=clock, clock_pol=clock_pol,
              reset=reset, reset_pol=reset_pol, reset_val=reset_val,
              enable=enable, enable_pol=enable_pol)
    return dff


def add_delay(self, data_in, delay=1, *,
              name=None,
              clock=None,
              clock_pol=None,
              reset=None,
              reset_pol=None):
    """遅延ユニットを作る．

    :param Expr data_in: データ入力
    :param int delay: 遅延値
    :param str name: 名前
    :param Expr clock: クロック入力
    :param str clock_pol: クロックのアクティブエッジを表す文字列
    :param Expr reset: リセット入力
    :param str reset_pol: リセットの極性を表す文字列
    """
    if clock is None:
        clock = self.default_clock
    if clock_pol is None:
        clock_pol = self.default_clock_pol
    if reset is None:
        reset = self.default_reset
    if reset_pol is None:
        reset_pol = self.default_reset_pol
    tmp_net = data_in
    rval = Expr.make_constant(data_type=data_in.data_type, val=0)
    for _ in range(delay):
        dff = Dff(self, data_in=tmp_net,
                  clock=clock, clock_pol=clock_pol,
                  reset=reset, reset_pol=reset_pol,
                  reset_val=rval)
        tmp_net = dff.output
    out = self.add_net(name=name, data_type=data_in.data_type)
    self.connect(out, tmp_net)
    return out


# Entity クラスにメンバ関数(インスタンスメソッド)を追加する．
Entity.add_dff = add_dff
Entity.add_delay = add_delay
