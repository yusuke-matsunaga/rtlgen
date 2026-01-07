library IEEE;
use IEEE.std_logic_1164.all;

entity ent1 is
  port (
    port1 : in  std_logic;
    port2 : in  std_logic;
    port3 : in  std_logic_vector(15 downto 0);
    oport : out std_logic
  );
end entity ent1;
