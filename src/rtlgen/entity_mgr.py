#! /usr/bin/env python3

"""EntityMgr の定義

:file: entity_mgr.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2022 Yusuke Matsunaga, All rights reserved.
"""

from rtlgen.entity import Entity
from rtlgen.rtlerror import RtlError


class EntityMgr:
    """RTL記述全体を表すクラス"""

    def __init__(self):
        self.__entity_list = []
        self.__entity_dict = {}

    @property
    def entity_gen(self):
        """エンティティのリストのジェネレータを返す．"""
        for entity in self.__entity_list:
            yield entity

    def add_entity(self, name):
        """エンティティを追加する．

        :param string name: エンティティ名
        """

        if name in self.__entity_dict:
            emsg = f'entity name "{name}" is already in use.'
            raise RtlError(emsg)
        ent = Entity(name)
        self.__entity_list.append(ent)
        self.__entity_dict[name] = ent
        return ent

    @staticmethod
    def get_entity_list(top_entity):
        """使用されているエンティティのリストを作る．"""

        ent_list = []
        ent_set = set()
        top_entity.gen_entity_sub(ent_list, ent_set)
        return ent_list
