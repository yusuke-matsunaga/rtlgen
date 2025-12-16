#! /usr/bin/env python3

"""コンポーネントインスタンスを表す定義

:file: inst.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: (C) 2021, 2022 Yusuke Matsunaga, All rights reserved.
"""

from rtlgen.item import Item
from rtlgen.rtlerror import RtlError
from rtlgen.entity import Entity
from rtlgen.writer_base import SimpleBlock


class Inst(Item):
    """コンポーネントインスタンスを表す定義"""

    def __init__(self, parent, entity, *, name=None):
        """初期化
        :param Entity entity: エンティティ
        :param str name: インスタンス名(オプショナル)

        """
        super().__init__(parent, name=name)
        self.__entity = entity
        self.__net_list = list()
        self.__port_dict = dict()
        for iport in entity.port_gen:
            net = self.add_net(iport.data_type)
            self.__net_list.append(net)
            # ポートの対応付を行う。
            if iport.name is not None:
                self.__port_dict[iport.name] = net

    @property
    def is_inst(self):
        return True

    @property
    def entity(self):
        """エンティティを返す．

        :rtype: Entity
        """
        return self.__entity

    @property
    def port_num(self):
        """ポート数を返す．

        :rtype: int
        """
        return self.__entity.port_num

    def port(self, pos):
        """pos 番目のポートを返す．

        :param int pos: 位置
        :rtype: Port|Net, Port
        :rise: AssertError (pos が範囲外の時)

        返り値は (外側のポート(ネット)、内側のポート) のタプルとなっている．
        """
        assert 0 <= pos < self.port_num
        return self.__net_list[pos], self.entity.port(pos)

    @property
    def port_gen(self):
        """ポートリストのジェネレーターを返す．"""
        for pos in range(self.port_num):
            yield self.port(pos)

    def __getattr__(self, name):
        """ポートをアクセスするためのギミック"""

        if name in self.__port_dict:
            return self.__port_dict[name]
        else:
            emsg = '{}: Illegal port name'.format(name)
            raise RtlError(emsg)

    def gen_verilog(self, writer):
        """Verilog-HDL記述を生成する．

        :param VerilogWriter writer: Verilog-DL出力器
        """
        line_str = '{} {}('.format(self.entity.name, self.name)
        comma = ''
        for oport, iport in self.port_gen:
            line_str += '{}.{}({})'.format(comma, iport.name, oport.name)
            comma = ', '
        line_str += ');'
        writer.write_line(line_str)
        writer.write_line('')

    def gen_vhdl(self, writer):
        """VHDL記述を生成する．

        :param VhdlWriter writer: VHDL出力器
        """
        header = '{}: {} port map('.format(self.name, self.entity.name)
        footer = ');\n'
        lines = list()
        for oport, iport in self.port_gen:
            name = oport.name
            line = [iport.name, '=>', name]
            lines.append(line)
        with SimpleBlock(writer, header, footer):
            writer.write_lines(lines, end=',', last_end='')


def add_inst(self, entity, *, name=None):
    """エンティティにインスタンスを追加する．

    :param Entity entity: 元のエンティティ
    :param str name: 名前
    """
    inst = Inst(self, entity, name=name)
    return inst


# Entity クラスにメンバ関数(インスタンスメソッド)を追加する．
Entity.add_inst = add_inst
