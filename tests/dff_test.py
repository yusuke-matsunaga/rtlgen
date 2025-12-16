#! /usr/bin/env python3

"""Dffのテスト

:file: dff_test.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2022 Yusuke Matsunaga, All rights reserved.
"""

import pytest
import io
from rtlgen import EntityMgr, Expr, DataType


def test_dff1():
    mgr = EntityMgr()
    ent = mgr.add_entity('dff_test1')
    clock = ent.add_input_port(name='clock')
    data_in = ent.add_input_port(name='data_in')
    data_out = ent.add_output_port(name='data_out')
    dff = ent.add_dff(clock=clock, clock_edge='positive',
                      data_in=data_in)
    ent.connect(data_out, dff.q)

    buff = io.StringIO()
    ent.write_verilog(fout=buff)
    contents = buff.getvalue()
    buff.close()

    exp_text = """module dff_test1(
  input  clock,
  input  data_in,
  output data_out
);
  reg net1;
  always @ ( posedge clock ) begin
    net1 <= data_in;
  end

  assign data_out = net1;
endmodule // dff_test1
"""

    assert contents == exp_text

    buff = io.StringIO()
    ent.write_vhdl(fout=buff)
    contents = buff.getvalue()
    buff.close()

    exp_text = """library IEEE;
use IEEE.std_logic_1164.all;

entity dff_test1 is
  port (
    clock    : in  std_logic;
    data_in  : in  std_logic;
    data_out : out std_logic
  );
end entity dff_test1;

architecture rtl of dff_test1 is
  signal net1 : std_logic;
begin
  item1: process ( clock ) begin
    if rising_edge(clock) then
      net1 <= data_in;
    end if;
  end process item1;

  data_out <= net1;
end architecture rtl;
"""

    assert contents == exp_text


def test_dff2():
    mgr = EntityMgr()
    ent = mgr.add_entity('dff_test2')
    clock = ent.add_input_port(name='clock')
    data_in = ent.add_input_port(name='data_in')
    data_out = ent.add_output_port(name='data_out')
    reset = ent.add_input_port(name='reset')
    bit = DataType.bit_type()
    dff = ent.add_dff(clock=clock, clock_edge='positive',
                      reset=reset, reset_pol='positive',
                      reset_val=Expr.make_constant(data_type=bit, val=0),
                      data_in=data_in)
    ent.connect(data_out, dff.q)

    buff = io.StringIO()
    ent.write_verilog(fout=buff)
    contents = buff.getvalue()
    buff.close()

    exp_text = """module dff_test2(
  input  clock,
  input  data_in,
  output data_out,
  input  reset
);
  reg net1;
  always @ ( posedge clock or posedge reset ) begin
    if ( reset ) begin
      net1 <= 1'b0;
    end
    else begin
      net1 <= data_in;
    end
  end

  assign data_out = net1;
endmodule // dff_test2
"""

    assert contents == exp_text

    buff = io.StringIO()
    ent.write_vhdl(fout=buff)
    contents = buff.getvalue()
    buff.close()

    exp_text = """library IEEE;
use IEEE.std_logic_1164.all;

entity dff_test2 is
  port (
    clock    : in  std_logic;
    data_in  : in  std_logic;
    data_out : out std_logic;
    reset    : in  std_logic
  );
end entity dff_test2;

architecture rtl of dff_test2 is
  signal net1 : std_logic;
begin
  item1: process ( clock, reset ) begin
    if reset = '1' then
      net1 <= '0';
    elsif rising_edge(clock) then
      net1 <= data_in;
    end if;
  end process item1;

  data_out <= net1;
end architecture rtl;
"""

    assert contents == exp_text


def test_dff3():
    mgr = EntityMgr()
    ent = mgr.add_entity('dff_test3')
    clock = ent.add_input_port(name='clock')
    data_in = ent.add_input_port(name='data_in')
    data_out = ent.add_output_port(name='data_out')
    enable = ent.add_input_port(name='enable')
    dff = ent.add_dff(clock=clock, clock_edge='positive',
                      enable=enable, enable_pol='positive',
                      data_in=data_in)
    ent.connect(data_out, dff.q)

    buff = io.StringIO()
    ent.write_verilog(fout=buff)
    contents = buff.getvalue()
    buff.close()

    exp_text = """module dff_test3(
  input  clock,
  input  data_in,
  output data_out,
  input  enable
);
  reg net1;
  always @ ( posedge clock ) begin
    if ( enable ) begin
      net1 <= data_in;
    end
  end

  assign data_out = net1;
endmodule // dff_test3
"""

    assert contents == exp_text

    buff = io.StringIO()
    ent.write_vhdl(fout=buff)
    contents = buff.getvalue()
    buff.close()

    exp_text = """library IEEE;
use IEEE.std_logic_1164.all;

entity dff_test3 is
  port (
    clock    : in  std_logic;
    data_in  : in  std_logic;
    data_out : out std_logic;
    enable   : in  std_logic
  );
end entity dff_test3;

architecture rtl of dff_test3 is
  signal net1 : std_logic;
begin
  item1: process ( clock ) begin
    if rising_edge(clock) and enable = '1' then
      net1 <= data_in;
    end if;
  end process item1;

  data_out <= net1;
end architecture rtl;
"""

    assert contents == exp_text


def test_dff4():
    mgr = EntityMgr()
    ent = mgr.add_entity('dff_test4')
    clock = ent.add_input_port(name='clock')
    data_in = ent.add_input_port(name='data_in')
    data_out = ent.add_output_port(name='data_out')
    reset = ent.add_input_port(name='reset')
    bit = DataType.bit_type()
    enable = ent.add_input_port(name='enable')
    dff = ent.add_dff(clock=clock, clock_edge='negative',
                      reset=reset, reset_pol='negative',
                      reset_val=Expr.make_constant(data_type=bit, val=0),
                      enable=enable, enable_pol='negative',
                      data_in=data_in)
    ent.connect(data_out, dff.q)

    buff = io.StringIO()
    ent.write_verilog(fout=buff)
    contents = buff.getvalue()
    buff.close()

    exp_text = """module dff_test4(
  input  clock,
  input  data_in,
  output data_out,
  input  reset,
  input  enable
);
  reg net1;
  always @ ( negedge clock or negedge reset ) begin
    if ( !reset ) begin
      net1 <= 1'b0;
    end
    else if ( !enable ) begin
      net1 <= data_in;
    end
  end

  assign data_out = net1;
endmodule // dff_test4
"""

    assert contents == exp_text

    buff = io.StringIO()
    ent.write_vhdl(fout=buff)
    contents = buff.getvalue()
    buff.close()

    exp_text = """library IEEE;
use IEEE.std_logic_1164.all;

entity dff_test4 is
  port (
    clock    : in  std_logic;
    data_in  : in  std_logic;
    data_out : out std_logic;
    reset    : in  std_logic;
    enable   : in  std_logic
  );
end entity dff_test4;

architecture rtl of dff_test4 is
  signal net1 : std_logic;
begin
  item1: process ( clock, reset ) begin
    if reset = '0' then
      net1 <= '0';
    elsif falling_edge(clock) and enable = '0' then
      net1 <= data_in;
    end if;
  end process item1;

  data_out <= net1;
end architecture rtl;
"""

    assert contents == exp_text
