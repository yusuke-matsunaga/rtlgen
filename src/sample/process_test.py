#! /usr/bin/env python3

""" ClockedProcess を使ったサンプルプログラム

:file: process_test.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2022 Yusuke Matsunaga, All rights reserved.
"""

from rtlgen import EntityMgr, Expr

mgr = EntityMgr()

# 1ビットのenable付きD-FF用のプロセス
ent1 = mgr.add_entity('dff1')
data_in = ent1.add_input_port(name='data_in')
enable = ent1.add_input_port(name='enable')
clock = ent1.add_input_port(name='clock')
q = ent1.add_output_port(name='q')

proc1 = ent1.add_clocked_process(clock=clock, clock_pol="positive")

net = ent1.add_net(reg_type=True)
with proc1.body() as _:
    if_stmt = _.add_if(enable)
    with if_stmt.then_body() as _:
        # スコープルールがあるので '_' を使いまわしても
        # 問題ない．
        # 別に b1, b2 という普通の変数を用いてもOK
        _.add_assign(net, data_in)

# 出力の接続を行う．
ent1.connect(q, net)

# VHDL出力
ent1.write_vhdl()
# Verilog出力
ent1.write_verilog()

# 1ビットの非同期リセット付きD-FF用のプロセス
ent2 = mgr.add_entity('dff2')
data_in = ent2.add_input_port(name='data_in')
reset = ent2.add_input_port(name='reset')
clock = ent2.add_input_port(name='clock')
q = ent2.add_output_port(name='q')

proc2 = ent2.add_clocked_process(clock=clock, clock_pol="positive",
                                 asyncctl=reset, asyncctl_pol="negative")

net = ent2.add_net(reg_type=True)
with proc2.body() as _:
    _.add_assign(net, data_in)
# 非同期リセットは別に記述する．
with proc2.asyncctl_body() as _:
    _.add_assign(net, Expr.make_constant(val=0))

# 出力の接続を行う．
ent2.connect(q, net)

# VHDL出力
ent2.write_vhdl()
# Verilog出力
ent2.write_verilog()
