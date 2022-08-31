#! /usr/bin/env python3

"""

:file: sample3.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2022 Yusuke Matsunaga, All rights reserved.
"""

from rtlgen import DataType
from rtlgen import EntityMgr


# データタイプの定義
bit_type = DataType.bit_type()  # 1ビット

mgr = EntityMgr()

# AND ゲートのエンティティ
and_gate = mgr.add_entity('and2')
port_a = and_gate.add_input_port(name='a')
port_b = and_gate.add_input_port(name='b')
port_x = and_gate.add_output_port(name='x')
and_gate.connect(port_x, port_a & port_b)

# ANDゲートを2つつなげたエンティティ
entity = mgr.add_entity('ent1')
port_1 = entity.add_input_port(data_type=bit_type, name='port1')
port_2 = entity.add_input_port(name='port2', data_type=bit_type)
port_3 = entity.add_input_port(data_type=bit_type, name='port3')
port_4 = entity.add_output_port(data_type=bit_type, name='port4')

inst1 = entity.add_inst(and_gate)
inst2 = entity.add_inst(and_gate)

entity.connect(inst1.a, port_1)
entity.connect(inst1.b, port_2)
entity.connect(inst2.a, inst1.x)
entity.connect(inst2.b, port_3)
entity.connect(port_4, inst2.x)

ent_list = mgr.get_entity_list(entity)
for ent in ent_list:
    ent.write_verilog()
