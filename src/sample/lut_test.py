#! /usr/bin/env python3

"""

:file: lut_test.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2022 Yusuke Matsunaga, All rights reserved.
"""

from rtlgen import EntityMgr
from rtlgen import DataType
from rtlgen import Expr

mgr = EntityMgr()

ent1 = mgr.add_entity('lut1')

ibw = 3
obw = 8
input_type = DataType.bitvector_type(ibw)
output_type = DataType.bitvector_type(obw)

input = ent1.add_input_port(name='input', data_type=input_type)
output = ent1.add_output_port(name='output', data_type=output_type)

lut = ent1.add_lut(input_bw=ibw, data_type=output_type)
for i in range(1 << ibw):
    indata = Expr.make_constant(data_type=input_type, val=i)
    outdata = Expr.make_constant(data_type=output_type, val=(1 << i))
    lut.add_data(indata, outdata)

ent1.connect(lut.input, input)
ent1.connect(output, lut.output)

ent1.write_verilog()

ent2 = mgr.add_entity('lut2')

ibw = 4
obw = 3
input_type = DataType.bitvector_type(ibw)
output_type = DataType.bitvector_type(obw)

input = ent2.add_input_port(name='input', data_type=input_type)
output = ent2.add_output_port(name='output', data_type=output_type)

lut2 = ent2.add_lut(input=input, data_type=output_type)

for i in range(1 << ibw):
    indata = Expr.make_constant(data_type=input_type, val=i)
    for j in range(ibw, -1, -1):
        if i & (1 << j):
            val = j + 1
            break
    else:
        val = 0
    outdata = Expr.make_constant(data_type=output_type, val=val)
    lut2.add_data(indata, outdata)

ent2.connect(output, lut2.output)

ent2.write_verilog()
