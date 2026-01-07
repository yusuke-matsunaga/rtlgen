#! /usr/bin/env python3

"""Verilog-HDL 記述を出力するクラス

:file: verilog_writer.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: (C) 2021 Yusuke Matsunaga, All rights reserved.
"""

from rtlgen.writer_base import WriterBase, WriteBlock
from rtlgen.item_mgr import ItemMgr
from rtlgen.entity import Entity


class VerilogModule(WriteBlock):
    """Verilog-HDLのモジュール記述を行うためのクラス"""

    def __init__(self, writer, entity):
        super().__init__(writer)
        self.__entity = entity

    def on_enter(self):
        self.writer.write_module_header(self.__entity)

    def on_exit(self):
        self.writer.write_module_footer(self.__entity)


class VerilogWriter(WriterBase):
    """Verilog-HDL 記述を出力するクラス

    :param fout: 出力先のファイルオブジェクト(名前付きの引数)
    :type fout: file_object
    """

    def __init__(self, *, fout):
        super().__init__(fout=fout)

    def __call__(self, entity):
        """Entity の内容を出力する.

        :param Entity entity: エンティティ
        """

        entity.make_names()

        with VerilogModule(self, entity):
            entity.gen_verilog(self)

            # 継続的代入文の出力
            lines = []
            for ca in entity.cont_assign_gen:
                lhs_str = ca.lhs.verilog_str
                rhs_str = ca.rhs.verilog_str
                line = ['assign', lhs_str, '=', rhs_str]
                lines.append(line)
            self.write_lines(lines, end=';')

    def write_module_header(self, entity):
        """モジュールのヘッダを出力する．"""
        line = f'module {entity.name}'
        if entity.port_num > 0:
            line += '('
            self.write_line(line)
            self.inc_indent()
            if True:
                # ポートリストの出力
                lines = []
                for port in entity.port_gen:
                    line = []
                    if port.is_input:
                        port_type = 'input'
                    elif port.is_output:
                        port_type = 'output'
                    elif port.is_inout:
                        port_type = 'inout'
                    else:
                        assert False
                    signed_str, range_str = VerilogWriter.data_type_to_str(
                        port.data_type)
                    line = [port_type, signed_str, range_str, port.name]
                    lines.append(line)
                # 実際に出力する．
                self.write_lines(lines, end=',', last_end='')
            self.dec_indent()
            self.write_line(');')
        else:
            line += ';'
            self.write_line(line)

    def write_module_footer(self, entity):
        """モジュールのフッタを出力する．"""
        self.write_line(f'endmodule // {entity.name}')

    @ staticmethod
    def data_type_to_str(data_type):
        """データタイプを表す Verilog 文字列を作る.

        :param DataType data_type: データタイプ
        :return: データタイプを表す文字列
        :rtype: str
        """
        signed_str = ''
        range_str = ''
        if data_type.is_bit_type:
            # 何もしない．
            pass
        elif data_type.is_bitvector_type:
            range_str = f'[{data_type.size - 1}:0]'
        elif data_type.is_signedbitvector_type:
            signed_str = 'signed'
            range_str = f'signed [{data_type.size - 1}:0]'
        else:
            # それ以外のタイプは使えない．
            assert False
        return signed_str, range_str

    @staticmethod
    def edge_str(pol):
        """センシティブエッジを表す文字列を返す．

        :param str pol: 極性を表す文字列("positive"か"negative")
        :return: "posiedge"か"negedge"を返す．
        """
        if pol == "positive":
            return "posedge"
        elif pol == "negative":
            return "negedge"
        else:
            assert False

    @staticmethod
    def cond_str(sig, pol):
        """if 文の条件用の文字列を作る．

        :param Expr sig: 対象の信号線
        :param str pol: 極性を表す文字列("positive"か"negative")
        """
        sig_str = sig.verilog_str
        if pol == "positive":
            return sig_str
        elif pol == "negative":
            return '!' + sig_str
        else:
            assert False


def item_mgr_gen_verilog(item_mgr, writer):
    """Verilog-HDL 記述を出力する(ItemMgr用)．
    """
    # ネット宣言の出力
    lines = []
    for net in item_mgr.net_gen:
        if net.reg_type:
            net_str = 'reg'
        else:
            net_str = 'wire'
        signed_str, range_str = \
            VerilogWriter.data_type_to_str(net.data_type)
        line = [net_str, signed_str, range_str, net.name]
        lines.append(line)
    writer.write_lines(lines, end=';')
    writer.write_line('')

    # 要素記述の出力
    for item in item_mgr.item_gen:
        item.gen_verilog(writer)

# ItemMgr にメンバ関数（インスタンスメソッド）を追加する．
ItemMgr.gen_verilog = item_mgr_gen_verilog


def write_verilog(self, *, fout=None):
    """内容を Verilog-HDL 形式で出力する．

    :param file_object fout: 出力先のファイルオブジェクト
    """
    vw = VerilogWriter(fout=fout)
    vw(self)


# Entity にメンバ関数(インスタンスメソッド)を追加する．
Entity.write_verilog = write_verilog
