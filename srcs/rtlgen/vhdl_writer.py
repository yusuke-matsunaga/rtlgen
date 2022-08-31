#! /usr/bin/env python3

"""VHDL 記述を出力するクラス

:file: vhdl_writer.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: (C) 2021 Yusuke Matsunaga, All rights reserved.
"""

from rtlgen.writer_base import WriterBase, SimpleBlock
from rtlgen.entity import Entity


class VhdlWriter(WriterBase):
    """VHDL 記述を出力するクラス

    :param fout: 出力先のファイルオブジェクト
    :type: fout file_object
    """

    def __init__(self, *, fout):
        super().__init__(fout=fout)

    def __call__(self, entity):
        """Entity の内容を出力する.

        :param Entity entity: エンティティ
        """

        entity.make_names()
        self.write_line('library IEEE;')
        self.write_line('use IEEE.std_logic_1164.all;')
        self.write_line('')

        # エンティティの出力
        header = 'entity {} is'.format(entity.name)
        footer = 'end entity {};\n'.format(entity.name)
        with SimpleBlock(self, header, footer):
            if entity.port_num > 0:
                # ポートリストの出力
                lines = list()
                for port in entity.port_gen:
                    if port.is_input:
                        port_type = 'in'
                    elif port.is_output:
                        port_type = 'out'
                    elif port.is_inout:
                        port_type = 'inout'
                    else:
                        assert False
                    data_type_str = VhdlWriter.__data_type_to_str(
                        port.data_type)
                    line = [port.name, ':', port_type, data_type_str]
                    lines.append(line)

                # 実際に出力する．
                with SimpleBlock(self, 'port (', ');'):
                    self.write_lines(lines, end=';', last_end='')

        # アーキテクチャの出力
        arch_name = 'rtl'
        arch_head = 'architecture {} of {} is'.format(
            arch_name, entity.name)
        with SimpleBlock(self, arch_head, None):
            # インスタンス記述で用いるコンポーネント宣言
            comp_dict = dict()
            for item in entity.item_gen:
                if item.is_inst:
                    if item.entity.name not in comp_dict:
                        comp_dict[item.entity.name] = item.entity
            for name in sorted(comp_dict.keys()):
                component = comp_dict[name]
                with SimpleBlock(self, 'component {} is'.format(name),
                                 'end component {};\n'.format(name)):
                    lines = list()
                    for port in component.port_gen:
                        if port.is_input:
                            port_type = 'in'
                        elif port.is_output:
                            port_type = 'out'
                        elif port.is_inout:
                            port_type = 'inout'
                        else:
                            assert False
                        data_type_str = VhdlWriter.__data_type_to_str(
                            port.data_type)
                        line = [port.name, ':', port_type, data_type_str]
                        lines.append(line)
                    with SimpleBlock(self, 'port (', ');'):
                        self.write_lines(lines, end=';', last_end='')

            # ネット宣言の出力
            lines = list()
            for net in entity.net_gen:
                data_type_str = VhdlWriter.__data_type_to_str(net.data_type)
                line = ['signal', net.name, ':', data_type_str]
                lines.append(line)
            self.write_lines(lines, end=';')

        # アーキテクチャ記述の本体
        with SimpleBlock(self, 'begin',
                         'end architecture {};'.format(arch_name)):
            # 要素の出力
            for item in entity.item_gen:
                item.gen_vhdl(self)

            # signal 代入文の出力
            lines = list()
            for ca in entity.cont_assign_gen:
                lhs_str = ca.lhs.vhdl_str
                rhs_str = ca.rhs.vhdl_str
                line = [lhs_str, '<=', rhs_str]
                lines.append(line)
            self.write_lines(lines, end=';')

    @ staticmethod
    def __data_type_to_str(data_type):
        """データタイプを表す VHDL 文字列を作る.

        :param DataType data_type: データタイプ
        :rtype: str
        """
        if data_type.is_bit_type:
            return 'std_logic'
        elif data_type.is_bitvector_type:
            return 'std_logic_vector({} downto 0)'.format(data_type.size - 1)
        elif data_type.is_signedbitvector_type:
            return 'signed({} downto 0)'.format(data_type.size - 1)
        else:
            # それ以外のタイプは使えない．
            assert False
        return None


def write_vhdl(self, *, fout=None):
    """内容を VHDL 形式で出力する．

    :param file_object fout: 出力先のファイルオブジェクト
    """
    vw = VhdlWriter(fout=fout)
    vw(self)


# Entity にメンバ関数(インスタンスメソッド)を追加する．
Entity.write_vhdl = write_vhdl
