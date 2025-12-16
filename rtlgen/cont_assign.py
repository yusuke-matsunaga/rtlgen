#! /usr/bin/env python3

"""
継続的代入文を表すクラス

:file: cont_assign.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2022 Yusuke Matsunaga, All rights reserved.
"""


class ContAssign:
    """継続的代入文を表すクラス
    """

    def __init__(self, lhs, rhs):
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
