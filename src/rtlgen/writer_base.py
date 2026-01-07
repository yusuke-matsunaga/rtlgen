#! /usr/bin/env python3

"""WriterBase の定義

:file: writer.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: (C) 2021 Yusuke Matsunaga, All rights reserved.
"""

import sys


class WriteBlock:
    """ブロックを管理するためのクラス

    with 構文で用いられることを仮定している．
    主な仕事をインデントを適切に保つこと．
    ブロックに入ったときに on_enter() 関数が呼ばれる．
    ブロックから抜けるときに on_exit() 関数が呼ばれる．
    このクラスでは実装していないので継承クラスで適切な
    関数を用意する必要がある．
    """

    def __init__(self, writer):
        self.writer = writer

    def __enter__(self):
        self.on_enter()
        self.writer.inc_indent()
        return self

    def __exit__(self, ex_type, ex_value, trace):
        self.writer.dec_indent()
        self.on_exit()


class SimpleBlock(WriteBlock):
    """単純な形式のブロック"""

    def __init__(self, writer, prefix, suffix):
        super().__init__(writer)
        self.__prefix = prefix
        self.__suffix = suffix

    def on_enter(self):
        if self.__prefix is not None:
            self.writer.write_line(self.__prefix)

    def on_exit(self):
        if self.__suffix is not None and self.__suffix != '':
            self.writer.write_line(self.__suffix)


class WriterBase:
    """出力用のベースクラス

    :param fout: 出力先(名前付き引数)
    :type fout: file_object
    """

    def __init__(self, *, fout):
        if fout is None:
            fout = sys.stdout
        self.__fout = fout
        self.__indent = 0
        self.__suspended = False

    def write_line(self, line, *, no_nl=False):
        """一行分の出力を行う．

        :param str line: 一行分の文字列
        :param bool no_nl: 改行抑止フラグ

        * 字下げが行われる．
        * no_nl = True 以外では改行が行われる．
        """
        if line != '':
            if self.__suspended:
                spc = ''
            else:
                spc = '  ' * self.__indent
            self.__write(f'{spc}{line}')
        if no_nl:
            self.__suspended = True
        else:
            self.__suspended = False
            self.write_nl()

    def write_nl(self):
        """改行を行う．"""
        self.__write('\n')

    def write_lines(self, lines, *, end='', last_end=None):
        """各フィールドの開始位置を揃えて出力する．

        :param elem_list: 出力する要素のリスト
        :type elem_list: list[str]
        :param str end: 終端文字列
        :param str last_end: 最後の行の終端文字列

        last_endが省略された場合には end の値を用いる．
        """
        if last_end is None:
            last_end = end
        n0 = self.__indent * 2
        tab_list = WriterBase.calc_tab_list(lines, n0)
        c = 0
        for line in lines:
            c += 1
            if c < len(lines):
                end_str = end
            else:
                end_str = last_end
            end_str += '\n'
            self.__write_line(tab_list, line, end=end_str)

    def __write_line(self, tab_list, elem_list, *, end=''):
        """各フィールドの開始位置を揃えて出力する.

        :param tab_list: 開始位置のリスト
        :type tab_list: list[int]
        :param elem_list: 出力する要素のリスト
        :type elem_list: list[str]

        * len(tab_list) >= len(elem_list) でなければならない．
        * 指定されたタブ位置に収まらない時はずれる．
        """
        assert len(tab_list) >= len(elem_list)

        # 現在の位置
        cur_pos = 0
        prev_elem = ''
        for elem, tab_pos in zip(elem_list, tab_list):
            if len(prev_elem) > 0:
                self.__write(' ')
                cur_pos += 1
            # 次のタブ位置と現在の位置の差分
            n = tab_pos - cur_pos
            if n < 0:
                # 最低でも一つの空白を入れる．
                n = 1
            # 差分だけスペースを入れる．
            self.__write(' ' * n)
            cur_pos += n
            # 要素を書き出す．
            self.__write(elem)
            # その分だけ現在の位置を進める．
            cur_pos += len(elem)
            prev_elem = elem

        self.__write(end)

    def __write(self, s):
        """出力用の下請け関数"""
        self.__fout.write(s)

    def inc_indent(self):
        """字下げ量を増やす．"""
        self.__indent += 1

    def dec_indent(self):
        """字下げ量を減らす．"""
        self.__indent -= 1

    @staticmethod
    def calc_tab_list(lines, n0=2):
        """複数の行のタブ位置を合わせて出力するためのタブ位置を計算する

        :param list[list[str]] lines: 要素のリスト
        :param int n0: 先頭の字下げ位置
        """

        # 各行の要素数の最大値を求める．
        n_elem = 0
        for line in lines:
            n = len(line)
            n_elem = max(n_elem, n)

        # 各位置の文字列の長さの最大値を求める．
        n_list = [0 for _ in range(n_elem)]
        for line in lines:
            for i, w in enumerate(line):
                n = len(w)
                n_list[i] = max(n_list[i], n)

        # 長さを1増やす．
        for i in range(n_elem - 1):
            if n_list[i] > 0:
                n_list[i] += 1

        # 結果の tab_list を作る．
        tab_list = []
        tab_list.append(n0)
        for i in range(1, n_elem):
            n1 = n0 + n_list[i - 1]
            tab_list.append(n1)
            n0 = n1
        return tab_list
