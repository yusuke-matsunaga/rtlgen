#! /usr/bin/env python3

"""

:file: sample1.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2021 Yusuke Matsunaga, All rights reserved.
"""

from rtlgen import DataType
from rtlgen import EntityMgr

# データタイプの定義
bit_type = DataType.bit_type()  # 1ビット
bv16_type = DataType.bitvector_type(16)  # 16ビットのビットベクタ

mgr = EntityMgr()

# エンティティの生成
name = 'ent1'
entity = mgr.add_entity(name)

# 1ビットの入力ポート'port1'の追加
port1 = entity.add_input_port(data_type=bit_type, name='port1')
# 1ビットの入力ポート'port2'の追加
port2 = entity.add_input_port(data_type=bit_type, name='port2')
# 16ビットのビットベクタの入力ポート'port3'の追加
port3 = entity.add_input_port(data_type=bv16_type, name='port3')
# 16ビットのビットベクタの入力ポート'port4'の追加
port4 = entity.add_input_port(data_type=bv16_type, name='port4')
# 1ビットの出力ポート'oport1'の追加
port5 = entity.add_output_port(data_type=bit_type, name='oport1')
# 16ビットの出力ポート'oport2'の追加
port6 = entity.add_output_port(data_type=bv16_type, name='oport2')

# 論理式の生成
expr = port1 & port2
# その論理式を port5 のソースに設定
entity.connect(port5, expr)

# ネットの生成
net1 = entity.add_net(data_type=bv16_type, name='net1')
entity.connect(net1, port3 + port4)

# そのネットをport6に接続
entity.connect(port6, net1)

# VHDL出力
with open("ent1.vhdl", "wt") as fout1:
    entity.write_vhdl(fout=fout1)

# Verilog-HDL出力
with open("ent1.v", "wt") as fout2:
    entity.write_verilog(fout=fout2)
