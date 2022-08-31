#! /usr/bin/env python3

"""
D-FF のテストプログラム

:file: dff_test.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2022 Yusuke Matsunaga, All rights reserved.
"""

from rtlgen import EntityMgr
from rtlgen import Expr

mgr = EntityMgr()

ent1 = mgr.add_entity('dff1')
data_in = ent1.add_input_port(name='data_in')
clock = ent1.add_input_port(name='clock')
q = ent1.add_output_port(name='q')

# 1ビットのD-FF
# 入出力のネットはすべて自動生成
dff1 = ent1.add_dff(clock=clock)

# 入出力の接続を行う．
ent1.connect(dff1.data_in, data_in)
ent1.connect(q, dff1.q)

# Verilog出力
ent1.write_verilog()

ent2 = mgr.add_entity('dff2')
data_in = ent2.add_input_port(name='data_in')
clock = ent2.add_input_port(name='clock')
reset = ent2.add_input_port(name='reset')
enable = ent2.add_input_port(name='enable')
q = ent2.add_output_port(name='q')

dff2 = ent2.add_dff(data_in=data_in,
                    clock=clock, clock_pol="positive",
                    reset=reset, reset_pol="negative",
                    reset_val=Expr.make_intconstant(0),
                    enable=enable, enable_pol="positive")

# 出力の接続を行う．
ent2.connect(q, dff2.q)

# Verilog出力
ent2.write_verilog()
