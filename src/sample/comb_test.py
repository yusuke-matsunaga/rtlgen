#! /usr/bin/env python3

""" 組み合わせ回路用プロセスのサンプルプログラム

:file: comb_test.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2025 Yusuke Matsunaga, All rights reserved.
"""


from rtlgen import EntityMgr, DataType, Expr

mgr = EntityMgr()

# ２ビットのビットベクタ
otype = DataType.bitvector_type(2)

ent1 = mgr.add_entity('comb1')
a = ent1.add_input_port(name='a')
b = ent1.add_input_port(name='b')
c = ent1.add_input_port(name='c')
o = ent1.add_output_port(name='o', data_type=otype)

proc1 = ent1.add_comb_process()

net = ent1.add_net(reg_type=True)
with proc1.body() as _:
    _.add_assign(net, Expr.make_constant(data_type=otype, val=0))
    if1 = _.add_if(a)
    with if1.then_body() as _:
        _.add_assign(net, Expr.make_constant(data_type=otype, val=1))
    with if1.else_body() as _:
        if2 = _.add_if(b)
        with if2.then_body() as _:
            _.add_assign(net, Expr.make_constant(data_type=otype, val=2))
        with if2.else_body() as _:
            if3 = _.add_if(c)
            with if3.then_body() as _:
                _.add_assign(net, Expr.make_constant(data_type=otype, val=3))

ent1.connect(o, net)

ent1.write_vhdl()
ent1.write_verilog()
