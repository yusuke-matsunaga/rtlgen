#! /usr/bin/env python3

"""

:file: process_test.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2022 Yusuke Matsunaga, All rights reserved.
"""

from rtlgen import EntityMgr
from rtlgen import DataType
from rtlgen import Expr


mgr = EntityMgr()

bv = DataType.bitvector_type(4)

ent = mgr.add_entity('process_test')

clock = ent.add_input_port(name='clock')
reset = ent.add_input_port(name='reset')

proc = ent.add_process(clock=clock, clock_pol="positive",
                       asyncctl=reset, asyncctl_pol="positive")

x = ent.add_net(name='x', data_type=bv, reg_type=True)
y = ent.add_net(name='y', data_type=bv, reg_type=True)

proc.asyncctl_body.add_assign(x, Expr.make_constant(data_type=bv, val=0))

proc.body.add_assign(x, x + Expr.make_constant(data_type=bv, val=1))
if_stmt = proc.body.add_if(x == Expr.make_constant(data_type=bv, val=13))
if_stmt.then_body.add_assign(x, Expr.make_constant(data_type=bv, val=0))
if_stmt.then_body.add_assign(y, y + Expr.make_constant(data_type=bv, val=1))
assert not proc.body.is_null
assert not if_stmt.then_body.is_null
assert if_stmt.else_body.is_null

ent.write_verilog()
ent.write_vhdl()
