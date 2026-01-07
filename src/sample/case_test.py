#! /usr/bin/env python3

""" case 文のサンプルプログラム

:file: case_test.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2025 Yusuke Matsunaga, All rights reserved.
"""


from rtlgen import EntityMgr, DataType, Expr

mgr = EntityMgr()

# 2ビットのビットベクタ
bv2 = DataType.bitvector_type(2)

ent1 = mgr.add_entity('comb1')
a = ent1.add_input_port(name='a')
b = ent1.add_input_port(name='b')
c = ent1.add_input_port(name='c')
d = ent1.add_input_port(name='d')
sel = ent1.add_input_port(name='sel', data_type=bv2)
o = ent1.add_output_port(name='o')

proc1 = ent1.add_comb_process()

net = ent1.add_net(reg_type=True)
with proc1.body() as _:
    case1 = _.add_case(sel)
    with case1.add_label(Expr.make_constant(data_type=bv2, val=0)) as _:
        _.add_assign(net, a)
    with case1.add_label(Expr.make_constant(data_type=bv2, val=1)) as _:
        _.add_assign(net, b)
    with case1.add_label(Expr.make_constant(data_type=bv2, val=2)) as _:
        _.add_assign(net, c)
    with case1.add_label(Expr.make_constant(data_type=bv2, val=3)) as _:
        _.add_assign(net, d)

ent1.connect(o, net)

ent1.write_vhdl()
ent1.write_verilog()
