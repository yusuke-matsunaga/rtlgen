#! /usr/bin/env python3

"""

:file: process_test.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2022 Yusuke Matsunaga, All rights reserved.
"""

from rtlgen import EntityMgr
from rtlgen import Statement

mgr = EntityMgr()

ent1 = mgr.add_entity('process1')
data_in = ent1.add_input_port(name='data_in')
clock = ent1.add_input_port(name='clock')
q = ent1.add_output_port(name='q')

# 1ビットのD-FF
dff1 = ent1.add_process(clock=(clock, "positive"))

net = ent1.add_net(reg_type=True)
stmt1 = Statement.new_NonblockingAssign(net, data_in)
dff1.add_body_stmt(stmt1)

# 出力の接続を行う．
ent1.connect(q, net)

# Verilog出力
ent1.write_verilog()
