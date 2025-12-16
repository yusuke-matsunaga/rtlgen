#! /usr/bin/env python3

"""Entity の定義

:file: entity.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: (C) 2021, 2022 Yusuke Matsunaga, All rights reserved.

"""

from rtlgen.port import PortType, InputPort, OutputPort, InoutPort
from rtlgen.net import Net
from rtlgen.var import Var
from rtlgen.cont_assign import ContAssign
from rtlgen.data_type import BitType
from rtlgen.rtlerror import RtlError


class Entity:
    """Entity を表すクラス

    :param str name: 名前

    VHDLのentity+architecture，Verilog-HDLのmoduleに相当する構成要素を表す．
    具体的には外部との接続インターフェイスを表すポートのリストと
    内部の構造を表すアイテムのリストを持つ．
    """

    def __init__(self, name):
        self.__name = name
        self.__port_list = list()
        self.__port_dict = dict()
        self.__net_list = list()
        self.__var_list = list()
        self.__cont_assign_list = list()
        self.__item_list = list()
        self.__item_dict = dict()
        self.__default_clock = None
        self.__default_clock_pol = None
        self.__default_reset = None
        self.__default_reset_pol = None

    @property
    def name(self):
        """名前を返す.

        :rtype: str
        """
        return self.__name

    @property
    def default_clock(self):
        """デフォルトのクロック信号を返す．"""
        return self.__default_clock

    @property
    def default_clock_pol(self):
        """デフォルトのクロック極性を返す．"""
        return self.__default_clock_pol

    @property
    def default_reset(self):
        """デフォルトのリセット信号を返す．"""
        return self.__default_reset

    @property
    def default_reset_pol(self):
        """デフォルトのリセット極性を返す．"""
        return self.__default_reset_pol

    def set_default_clock(self, clock, clock_pol):
        """デフォルトのクロックを設定する．

        :param Expr clock: クロック信号
        :param str clock_pol: クロックの極性
        """
        self.__default_clock = clock
        self.__default_clock_pol = clock_pol

    def set_default_reset(self, reset, reset_pol):
        """デフォルトのリセットを設定する．

        :param Expr reset: リセット信号
        :param str clock_pol: リセットの極性
        """
        self.__default_reset = reset
        self.__default_reset_pol = reset_pol

    @property
    def port_num(self):
        """ポート数を返す.

        :rtype: int
        """
        return len(self.__port_list)

    def port(self, pos):
        """pos 番目のポートを返す.

        :param int pos: 位置
        :rtype: Port
        :rise: AssertError (posが範囲外の時)
        """
        assert 0 <= pos < self.port_num
        return self.__port_list[pos]

    @property
    def port_gen(self):
        """ポートリストのジェネレーターを返す."""
        for port in self.__port_list:
            yield port

    def find_port(self, name):
        """ポート名からポートを返す.

        :param str name: ポート名
        :rtype: Port or None

        見つからない場合には None を返す．
        """
        if name in self.__port_dict:
            return self.__port_dict[name]
        else:
            return None

    def add_input_port(self, *, name, data_type=BitType()):
        """入力ポートを追加する．

        :param str name: ポート名(名前付きの引数)
        :param DataType data_type: データタイプ(名前付きのオプション引数)
        :return: 生成されたポートを返す．
        """
        return self.__add_port(PortType.INPUT, name, data_type, None)

    def add_output_port(self, *, name, data_type=BitType(), src=None):
        """出力ポートを追加する．

        :param str name: ポート名(名前付きの引数)
        :param DataType data_type: データタイプ(名前付きのオプション引数)
        :param Expr src: ソース(名前付きのオプション引数)
        :return: 生成されたポートを返す．
        """
        return self.__add_port(PortType.OUTPUT, name, data_type, src)

    def add_inout_port(self, *, name, data_type=BitType(), src=None):
        """入出力ポートを追加する．

        :param str name: ポート名(名前付きの引数)
        :param DataType data_type: データタイプ(名前付きのオプション引数)
        :param Expr src: ソース(名前付きのオプション引数)
        :return: 生成されたポートを返す．
        """
        return self.__add_port(PortType.OUTPUT, name, data_type, src)

    def __add_port(self, port_type, name, data_type, src):
        """ポートを追加する．

        :param PortType port_type: ポートの種類(INPUT, OUTPUT, INOUT)
        :param str name: ポート名
        :param DataType data_type: データタイプ
        :param Expr src: ソース
        :return: 生成されたポートを返す．

        src は OUTPUT, INOUT タイプの時のみ意味を持つ．
        """
        if name in self.__port_dict:
            # すでに同じ名前のポートが登録されている．
            emsg = 'port name "{}" of'.format(name)
            emsg += '"{}" is already in use.'.format(self.__name)
            raise RtlError(emsg)
        if port_type == PortType.INPUT:
            port = InputPort(data_type, name=name)
        elif port_type == PortType.OUTPUT:
            port = OutputPort(data_type, name=name)
            if src is not None:
                self.connect(port, src)
        elif port_type == PortType.INOUT:
            port = InoutPort(data_type, name=name)
            if src is not None:
                self.connect(port, src)
        self.__port_list.append(port)
        if name is not None:
            self.__port_dict[name] = port
        return port

    @property
    def net_num(self):
        """ネット数を返す．

        :rtype: int
        """
        return len(self.__net_list)

    def net(self, pos):
        """pos 番目のネットを返す．

        :param int pos: 位置
        :rtype: Net
        :rise: AssertError (pos が範囲外)
        """
        assert 0 <= pos < self.net_num
        return self.__net_list[pos]

    @property
    def net_gen(self):
        """ネットリストのジェネレーターを返す．"""
        for net in self.__net_list:
            yield net

    def add_net(self, *, name=None, data_type=None, reg_type=False, src=None):
        """ネットを生成する．

        :param str Name: 名前(名前付きのオプション引数)
        :param DataType data_type: データタイプ(名前付きのオプション引数)
        :return: 生成したネットを返す．
        :rtype: Net
        """
        if data_type is None:
            if src is None:
                data_type = BitType()
            else:
                data_type = src.data_type
        elif src is not None:
            if data_type != src.data_type:
                emsg = 'data_type mismatch'
                raise RtlError(emsg)
        net = Net(data_type, name, reg_type=reg_type)
        self.reg_net(net)
        if src is not None:
            self.connect(net, src)
        return net

    def reg_net(self, net):
        """ネットを登録する．

        :param Net net: 対象のネット
        """
        self.__net_list.append(net)
        if net.name is not None:
            if net.name in self.__item_dict:
                # 名前がすでに使われていた．
                emsg = 'net name "{}" of "{}" is already in use.'.format(
                    net.name, self.__name)
                raise RtlError(emsg)
            self.__item_dict[net.name] = net

    @property
    def var_num(self):
        """変数の数を返す．

        :rtype: int
        """
        return len(self.__var_list)

    def var(self, pos):
        """pos 番目の変数を返す．

        :param int pos: 位置
        :rtype: Var
        :rise: AssertError (pos が範囲外)
        """
        assert 0 <= pos < self.var_num
        return self.__var_list[pos]

    @property
    def var_gen(self):
        """変数リストのジェネレーターを返す．"""
        for var in self.__var_list:
            yield var

    def add_var(self, *, name=None, data_type=None):
        """変数を生成する．

        :param str Name: 名前(名前付きのオプション引数)
        :param DataType data_type: データタイプ(名前付きのオプション引数)
        :return: 生成した変数を返す．
        :rtype: Var
        """
        if data_type is None:
            data_type = BitType()
        var = Var(data_type, name)
        self.reg_var(var)
        return var

    def reg_var(self, var):
        """変数を登録する．

        :param Var var: 対象のネット
        """
        self.__var_list.append(var)
        if var.name is not None:
            if var.name in self.__item_dict:
                # 名前がすでに使われていた．
                emsg = 'variable name "{}" of "{}" is already in use.'.format(
                    var.name, self.__name)
                raise RtlError(emsg)
            self.__item_dict[var.name] = var

    @property
    def cont_assign_num(self):
        """継続的代入文の数を返す．"""
        return len(self.__cont_assign_list)

    @property
    def cont_assign_gen(self):
        """継続的代入文のリストのジェネレータを返す．"""
        for ca in self.__cont_assign_list:
            yield ca

    def connect(self, lhs, rhs):
        """ネットの接続を行う．

        :param Expr lhs: 左辺式
        :param Expr rhs: 右辺式
        """
        ca = ContAssign(lhs, rhs)
        self.__cont_assign_list.append(ca)

    @property
    def item_num(self):
        """要素数を返す.

        :rtype: int
        """
        return len(self.__inst_list)

    def item(self, pos):
        """pos 番目の要素を返す.

        :param int pos: 位置
        :rtype: Item
        :rise: AssertError (pos が範囲外)
        """
        assert 0 <= pos < self.item_num
        return self.__item_list[pos]

    @property
    def item_gen(self):
        """要素リストのジェネレーターを返す."""
        for item in self.__item_list:
            yield item

    def reg_item(self, item):
        """要素を登録する．

        :param Item item: 登録する要素
        """
        if item.name is not None:
            if item.name in self.__item_dict:
                # 名前がすでに使われていた．
                emsg = 'item name "{}" is already in use.'.format(item.name)
                raise RtlError(emsg)
            self.__item_dict[item.name] = item
        self.__item_list.append(item)

    def make_names(self, *,
                   port_template=None,
                   net_template=None,
                   var_template=None,
                   item_template=None):
        """無名のオブジェクトに名前をつける．

        :param Entity top_entity: トップレベルのエンティティ
        :param string port_template: ポート名のテンプレート
        :param string net_template: ネット名のテンプレート
        :param string var_template: 変数名のテンプレート
        :param string item_template: 要素名のテンプレート

        テンプレート文字列は Python3 の .format() の形式を用いる．
        置き換え引数は数値の一つだけ．
        """

        # 無名のポートに名前をつける．
        if port_template is None:
            port_template = "port{}"
        port_id = 1
        for port in self.__port_list:
            if port.name is None:
                while True:
                    name = port_template.format(port_id)
                    port_id += 1
                    if name not in self.__port_dict:
                        port.set_name(name)
                        self.__port_dict[name] = port
                        break

        # 無名のネットに名前をつける．
        if net_template is None:
            net_template = "net{}"
        net_id = 1
        for net in self.__net_list:
            if net.name is None:
                while True:
                    name = net_template.format(net_id)
                    net_id += 1
                    if name not in self.__item_dict:
                        net.set_name(name)
                        self.__item_dict[name] = net
                        break

        # 無名の変数に名前をつける．
        if var_template is None:
            var_template = "var{}"
        var_id = 1
        for var in self.__var_list:
            if var.name is None:
                while True:
                    name = var_template.format(var_id)
                    net_id += 1
                    if name not in self.__item_dict:
                        var.set_name(name)
                        self.__item_dict[name] = var
                        break

        # 無名の要素に名前をつける．
        if item_template is None:
            item_template = "item{}"
        item_id = 1
        for item in self.__item_list:
            if item.name is None:
                while True:
                    name = item_template.format(item_id)
                    item_id += 1
                    if name not in self.__item_dict:
                        item.set_name(name)
                        self.__item_dict[name] = item
                        break

    def gen_entity_sub(self, ent_list, ent_set):
        if self in ent_set:
            return
        ent_set.add(self)
        ent_list.append(self)

        for item in self.__item_list:
            item.entity.gen_entity_sub(ent_list, ent_set)
