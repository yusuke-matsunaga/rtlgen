#! /usr/bin/env python3

""" Item を管理するクラス

:file: item_mgr.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2024 Yusuke Matsunaga, All rights reserved.
"""

from rtlgen.net import Net
from rtlgen.var import Var
from rtlgen.data_type import BitType
from rtlgen.rtlerror import RtlError


class ItemMgr:

    def __init__(self, name):
        self.__name = name
        self.__net_list = []
        self.__var_list = []
        self.__item_list = []
        self.__block_list = []
        self.__name_dict = {}
        
    @property
    def name(self):
        """名前を返す．
        """
        return self.__name

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
        self.__net_list.append(net)
        self.reg_name(net)
        return net

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
        self.__var_list.append(var)
        self.reg_name(var)
        return var
    
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
        self.__item_list.append(item)
        self.reg_name(item)

    @property
    def block_num(self):
        """名前付きブロックの数を返す．
        """
        return len(self.__block_list)

    def block(self, pos):
        """pos 番目の名前付きブロックを返す．

        :param int pos: 位置
        :rtype: NamedStatementBlock
        :rise: AssertError (pos が範囲外)
        """
        assert 0 <= pos < self.block_num
        return self.__block_list[pos]

    @property
    def block_gen(self):
        """名前付きブロックリストのジェネレーターを返す."""
        for block in self.__block_list:
            yield block

    def reg_block(self, block):
        """名前付きブロックを登録する．

        :param NamedStatementBlock: 登録するブロック
        """
        self.__block_list.append(block)
        self.reg_name(block)

    def reg_name(self, item):
        """名前を登録する．

        :param Item item: 登録する要素
        """
        if item.name is not None:
            if item.name in self.__name_dict:
                # 名前がすでに使われていた．
                emsg = f'item name "{item.name}" of "{self.__name}" is already in use.'
                raise RtlError(emsg)
            self.__name_dict[item.name] = item
        
    def make_names(self, *,
                   net_template=None,
                   var_template=None,
                   item_template=None,
                   block_template=None):
        """無名のオブジェクトに名前をつける．

        :param string net_template: ネット名のテンプレート
        :param string var_template: 変数名のテンプレート
        :param string item_template: 要素名のテンプレート
        :param string block_template: ブロック名のテンプレート

        テンプレート文字列は Python3 の .format() の形式を用いる．
        置き換え引数は数値の一つだけ．
        """

        # 無名のネットに名前をつける．
        if net_template is None:
            # デフォルトのフォーマット
            net_template = "net{}"
        net_id = 1
        for net in self.__net_list:
            if net.name is None:
                while True:
                    name = net_template.format(net_id)
                    net_id += 1
                    if name not in self.__name_dict:
                        net.set_name(name)
                        self.__name_dict[name] = net
                        break

        # 無名の変数に名前をつける．
        if var_template is None:
            # デフォルトのフォーマット
            var_template = "var{}"
        var_id = 1
        for var in self.__var_list:
            if var.name is None:
                while True:
                    name = var_template.format(var_id)
                    net_id += 1
                    if name not in self.__name_dict:
                        var.set_name(name)
                        self.__name_dict[name] = var
                        break

        # 無名の要素に名前をつける．
        if item_template is None:
            # デフォルトのフォーマット
            item_template = "item{}"
        item_id = 1
        for item in self.__item_list:
            if item.name is None:
                while True:
                    name = item_template.format(item_id)
                    item_id += 1
                    if name not in self.__name_dict:
                        item.set_name(name)
                        self.__name_dict[name] = item
                        break
        
        # 匿名の名前付きブロックに名前をつける．
        if block_template is None:
            # デフォルトのフォーマット
            block_template = "block{}"
        block_id = 1
        for block in self.__block_list:
            if block.name is None:
                while True:
                    name = block_template.format(block_id)
                    block_id += 1
                    if name not in self.__name_dict:
                        block.set_name(name)
                        self.__name_dict[name] = block
                        break
            block.make_names(net_template=net_template,
                             var_template=var_template,
                             item_template=item_template,
                             block_template=block_template)
                    
