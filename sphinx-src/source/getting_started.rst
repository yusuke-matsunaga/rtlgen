rtlgen の使い方
===================

1. データ型
------------

rtlgen では以下のデータ型を用いることができる．

* BitType: 1ビット型．VHDLの std_logic と同一．
* BitVectorType: 多ビットベクタ型．VHDLの std_logic_vector と同一．
* SignedBitVectorType: 符号付き多ビットベクタ型．
* ArrayType: 同一のデータ型の配列構造
* RecordType: 異なるデータ型から構成されるレコード構造

現状は ArrayType, RecordType はサポートしていない．

これらのクラスは rtlgen パッケージには import されていないので
ユーザーが直接参照することはできない．そのため下記のクラスメソッドを用
いる．

::

   from rtlgen import DataType

   # BitType の生成
   type1 = DataType.bit_type()

   # BitVectorType の生成
   size = 8
   type2 = DataType.bitvector_type(size)

   # SignedBitVectorType の生成
   size = 16
   type3 = DataType.signed_bitvector_type(size)


2. RTLの構成要素
----------------

2.1. エンティティ
^^^^^^^^^^^^^^^^^^

エンティティ(entity)は VHDL の entity，Verilog-HDL の module に対応す
るものであり，
すべての構成要素を格納する器の役割を持つ．
また，階層設計でサブモジュールとして用いられる場合の外部インターフェイ
ス情報としてポートを持つ．

エンティティを生成するには EntityMgr クラスのインスタンスに対して
``add_entity()`` を呼び出す．
このときにエンティティ名を引数として渡す必要がある．
同じ EntityMgr 上ではエンティティ名は重複できない．
重複した名前のエンティティを作ろうとするとエラーとなる．

::

   from rtlgen import EntityMgr

   # マネージャを生成する．
   mgr = EntityMgr()

   # エンティティを生成する．
   ent1 = mgr.add_entity('ent')

   # 同名のエンティティの生成はエラーとなる．
   ent2 = mgr.add_entity('ent')

この ``ent1`` に対する VHDL 出力は次の様になる．

::

   library IEEE;
   use IEEE.std_logic_1164.all;

   entity ent is
   end entity ent;

   architecture rtl of ent is
   begin
   end architecture rtl;

Verilog-HDL 出力は次の様になる．

::

   module ent;
   endmodule // ent

もちろん，空のエンティティなので空の記述が得られる．


2.2. ポート
^^^^^^^^^^^

ポートはエンティティの外部インターフェイスを能わすものであり，
以下の３種類がある．

* InputPort: 入力ポート
* OutputPort: 出力ポート
* InoutPort: 入出力ポート

ポートは前述の任意のデータタイプ(DataType)を持つことができる．
また，ポートは必ず名前を持たなければならない．
これはインスタンスとして用いる際のポート割当時に名前を用いるためである．
通常のVHDLやVerilog-HDLで用いられる順序に基づいた割当は rtlgen では
行えない仕様となっている．

::

   from rtlgen import EntityMgr, DataType

   # マネージャを生成する．
   mgr = EntityMgr()

   # エンティティを生成する．
   ent1 = mgr.add_entity('ent')

   # 入力ポートの生成
   # data_type は BitType が仮定される．
   iport1 = ent1.add_input_port(name='input1')

   # 16ビットのビットベクタ型
   bv16 = DataType.bitvector_type(16)

   # 出力ポートの生成
   oport1 = ent1.add_output_port(name='output1', data_type=bv16)

   # 入出力ポートの生成
   bport1 = ent1.add_inout_port(name='inout1')

VHDL 出力

::

   library IEEE;
   use IEEE.std_logic_1164.all;

   entity ent is
     port (
       input1  : in  std_logic;
       output1 : out std_logic_vector(15 downto 0);
       inout1  : out std_logic
     );
   end entity ent;

   architecture rtl of ent is
   begin
   end architecture rtl;

Verilog-HDL 出力

::

    module ent(
      input         input1,
      output [15:0] output1,
      output        inout1
    );
    endmodule // ent


2.3 ネット
^^^^^^^^^^

ネットは要素間を接続する配線であり，VHDLの signal，Verilog-HDL の wire
などに対応する．
ポートと同様に任意のデータタイプ(DataType)を持つことができる．
また名前を持つこともできるが，ネットの場合は名前は必須ではない．
無名のネットは出力時に他の要素を重複しない一意の名前を割り当てられる．

::

   from rtlgen import EntityMgr, DataType

   # マネージャを生成する．
   mgr = EntityMgr()

   # エンティティを生成する．
   ent1 = mgr.add_entity('ent')

   # 入力ポートの生成
   # data_type は BitType が仮定される．
   iport1 = ent1.add_input_port(name='input1')

   # 16ビットのビットベクタ型
   bv16 = DataType.bitvector_type(16)

   iport2 = ent1.add_input_port(name='input2')

   # 出力ポートの生成
   oport1 = ent1.add_output_port(name='output1', data_type=bv16)

   # 入出力ポートの生成
   bport1 = ent1.add_inout_port(name='inout1')

   # 無名のネットの生成
   # data_type は BitType が仮定される．
   net1 = ent1.add_net()

   # 16ビットの 'net1' というネットの生成
   net2 = ent1.add_net(name='net1', data_type=bv16)

   # iport2 をソースとするネットの生成
   # data_type は iport2 の data_type が仮定される．
   net3 = ent1.add_net(src=iport2)

VHDL 出力

::

   library IEEE;
   use IEEE.std_logic_1164.all;

   entity ent is
     port (
       input1  : in  std_logic;
       input2  : in  std_logic_vector(15 downto 0);
       output1 : out std_logic_vector(15 downto 0);
       inout1  : out std_logic
     );
   end entity ent;

   architecture rtl of ent is
     signal net2 : std_logic;
     signal net1 : std_logic_vector(15 downto 0);
     signal net3 : std_logic_vector(15 downto 0);
   begin
     net3 <= input2;
   end architecture rtl;


Verilog-HDL 出力

::

   module ent(
     input         input1,
     input  [15:0] input2,
     output [15:0] output1,
     output        inout1
   );
     wire        net2;
     wire [15:0] net1;
     wire [15:0] net3;
     assign net3 = input2;
   endmodule // ent

出力例より明らかなように無名のネットは ``netXX`` という形式で新たな名
前が割り当てられる(この形式は任意の形式に変更するすることができる)．
ただし，この例ではすでに ``net1`` という名前のネットが存在するので
新規に割り当てられる名前は ``net2`` , ``net3`` となっている．

ネットの生成時に ``src`` パラメータでソースを指定した場合には
そのネットに対する割当文が自動生成される．

上の例の ``net3`` の記述は以下と等価である．

::

   net3 = ent1.add_net(data_type=bv16)
   ent1.connect(net3, iport2)

``Entity.connect`` はネットやポートの接続を行う．


2.4 式
^^^^^^^

VHDLやVerilog-HDLで使用可能な式はほぼ同じ形で使用することができる．

+--------------------------------------------------+--------+--------------------------+
| 生成用のクラスメソッド                           | 演算子 | 説明                     |
+==================================================+========+==========================+
| ``make_not(opr1)``                               | ``~``  | 否定演算                 |
+--------------------------------------------------+--------+--------------------------+
| ``make_and(opr1, opr2)``                         | ``&``  | AND演算                  |
+--------------------------------------------------+--------+--------------------------+
| ``make_or(opr1, opr2)``                          | ``|``  | OR演算                   |
+--------------------------------------------------+--------+--------------------------+
| ``make_xor(opr1, opr2)``                         | ``^``  | XOR演算                  |
+--------------------------------------------------+--------+--------------------------+
| ``make_nand(opr1, opr2)``                        |        | NAND演算                 |
+--------------------------------------------------+--------+--------------------------+
| ``make_nor(opr1, opr2)``                         |        | NOR演算                  |
+--------------------------------------------------+--------+--------------------------+
| ``make_xnor(opr1, opr2)``                        |        | XNOR演算                 |
+--------------------------------------------------+--------+--------------------------+
| ``make_uminus(opr1)``                            | ``-``  | 単項マイナス演算         |
+--------------------------------------------------+--------+--------------------------+
| ``make_add(opr1, opr2)``                         | ``+``  | 加算                     |
+--------------------------------------------------+--------+--------------------------+
| ``make_sub(opr1, opr2)``                         | ``-``  | 減算                     |
+--------------------------------------------------+--------+--------------------------+
| ``make_mul(opr1, opr2)``                         | ``*``  | 乗算                     |
+--------------------------------------------------+--------+--------------------------+
| ``make_div(opr1, opr2)``                         | ``/``  | 除算                     |
+--------------------------------------------------+--------+--------------------------+
| ``make_mod(opr1, opr2)``                         | ``%``  | 剰余算                   |
+--------------------------------------------------+--------+--------------------------+
| ``make_lsft(opr1, opr2)``                        |        | 左シフト演算             |
+--------------------------------------------------+--------+--------------------------+
| ``make_rsft(opr1, opr2)``                        |        | 右シフト演算             |
+--------------------------------------------------+--------+--------------------------+
| ``make_eq(opr1, opr2)``                          | ``==`` | 等価比較演算             |
+--------------------------------------------------+--------+--------------------------+
| ``make_ne(opr1, opr2)``                          | ``!=`` | 非等価比較演算           |
+--------------------------------------------------+--------+--------------------------+
| ``make_lt(opr1, opr2)``                          | ``<``  | 小なり比較演算           |
+--------------------------------------------------+--------+--------------------------+
| ``make_gt(opr1, opr2)``                          | ``>``  | 大なり比較演算           |
+--------------------------------------------------+--------+--------------------------+
| ``make_le(opr1, opr2)``                          | ``<=`` | 小なりイコール比較演算   |
+--------------------------------------------------+--------+--------------------------+
| ``make_ge(opr1, opr2)``                          | ``>=`` | 大なりイコール比較演算   |
+--------------------------------------------------+--------+--------------------------+
| ``make_constant(data_type, val)``                |        | 任意のデータタイプの定数 |
+--------------------------------------------------+--------+--------------------------+
| ``make_intconstant(val)``                        |        | 整数型の定数             |
+--------------------------------------------------+--------+--------------------------+
| ``bit_select(primary, index)``                   |        | ビット選択               |
+--------------------------------------------------+--------+--------------------------+
| ``part_select(primary, left, right, direction)`` |        | 範囲選択                 |
+--------------------------------------------------+--------+--------------------------+
| ``concat(expr_list)``                            |        | 連結演算                 |
+--------------------------------------------------+--------+--------------------------+
| ``multi_concat(rep_num, expr_list)``             |        | 繰り返し連結演算         |
+--------------------------------------------------+--------+--------------------------+
| ``extension(src, dst_size)``                     |        | ビット幅拡張             |
+--------------------------------------------------+--------+--------------------------+
| ``sign_extension(src, dst_size)``                |        | 符号付きビット幅拡張     |
+--------------------------------------------------+--------+--------------------------+

一部の演算は Python の演算子にオーバーロードしているので Python の式と
同様にインラインで生成することができる．
各演算の詳細はクラス一覧を参照のこと．

::

   from rtlgen import EntityMgr, DataType, Expr

   mgr = EntityMgr()
   ent1 = mgr.add_entity('ent')

   iport1 = ent1.add_input_port(name='input1')

   bv16 = DataType.bitvector_type(16)

   iport2 = ent1.add_input_port(name='input2', data_type=bv16)
   iport3 = ent1.add_input_port(name='input3', data_type=bv16)

   oport1 = ent1.add_output_port(name='output1', data_type=bv16)
   oport2 = ent1.add_output_port(name='output2')

   # iport2 と iport3 の16ビットの加算結果を oport1 に接続する．
   ent1.connect(oport1, iport2 + iport3)

   # iport2 の 3 ビット目を選択する．
   bit3 = Expr.bit_select(iport2, 3)

   # bit3 と iport1 の XOR を oport2 に接続する．
   ent1.connect(oport2, bit3 ^ iport1)

VHDL 出力

::

   library IEEE;
   use IEEE.std_logic_1164.all;

   entity ent is
     port (
       input1  : in  std_logic;
       input2  : in  std_logic_vector(15 downto 0);
       input3  : in  std_logic_vector(15 downto 0);
       output1 : out std_logic_vector(15 downto 0);
       output2 : out std_logic
     );
   end entity ent;

   architecture rtl of ent is
   begin
     output1 <= (input2 + input3);
     output2 <= (input2(3) ^ input1);
   end architecture rtl;


Verilog-HDL 出力

::

   module ent(
     input         input1,
     input  [15:0] input2,
     input  [15:0] input3,
     output [15:0] output1,
     output        output2
   );
     assign output1 = (input2 + input3);
     assign output2 = (input2[3] ^ input1);
   endmodule // ent


この例では ``+`` と ``^`` は Python の演算子をそのまま用いて式を作って
いる．
ビット選択は Python に相当する演算子がないので ``Expr.bit_select()``
関数で生成している．
この結果の ``bit3`` は Python 上では ``Expr`` というクラス（の派生クラ
ス）のインスタンスになっている．
そのため，VHDLやVerilog-HDLの出力では明示的には現れない．


2.5 インスタンス
^^^^^^^^^^^^^^^^

他のエンティティを部品としてインスタンス化する．
そのためにはインスタンス化するエンティティを定義しておく必要がある．
ただし，そのエンティティの内部アーキテクチャの定義は必要はない．
具体的には ``Entity.add_inst()`` 関数を用いる．

::

   from rtlgen import EntityMgr

   mgr = EntityMgr()

   # 2入力ANDゲートのエンティティを作る．
   and_gate = mgr.add_entity('and')
   i1 = and_gate.add_input_port(name='input1')
   i2 = and_gate.add_input_port(name='input2')
   o = and_gate.add_output_port(name='output')
   and_gate.connect(o, i1 & i2)

   # ANDゲートを2つつなげたエンティティを作る．
   ent1 = mgr.add_entity('ent')
   iport1 = ent1.add_input_port(name='input1')
   iport2 = ent1.add_input_port(name='input2')
   iport3 = ent1.add_input_port(name='input3')
   oport = ent1.add_output_port(name='output1')

   # ANDゲートのインスタンスを生成する．
   and1 = ent1.add_inst(and_gate)
   and2 = ent1.add_inst(and_gate)

   # 接続する．
   # インスタンスのポートは '.<ポート名>'
   # でアクセスできる．
   ent1.connect(and1.input1, iport1)
   ent1.connect(and1.input2, iport2)
   ent1.connect(and2.input1, and1.output)
   ent1.connect(and2.input2, iport3)
   ent1.connect(oport, and2.output)

この例では ``and_gate`` 内部の結線を行っているが，
以下の出力例には現れない．
実際， ``ent1`` の出力のためだけなら不必要である．

VHDL 出力

::

   library IEEE;
   use IEEE.std_logic_1164.all;

   entity ent is
     port (
       input1  : in  std_logic;
       input2  : in  std_logic;
       input3  : in  std_logic;
       output1 : out std_logic
     );
   end entity ent;

   architecture rtl of ent is
     component and is
       port (
         input1 : in  std_logic;
         input2 : in  std_logic;
         output : out std_logic
       );
     end component and;

     signal net1 : std_logic;
     signal net2 : std_logic;
     signal net3 : std_logic;
     signal net4 : std_logic;
     signal net5 : std_logic;
     signal net6 : std_logic;
   begin
       item1: and port map(
       input1 => net1,
       input2 => net2,
       output => net3
     );

     item2: and port map(
       input1 => net4,
       input2 => net5,
       output => net6
     );

     net1    <= input1;
     net2    <= input2;
     net4    <= net3;
     net5    <= input3;
     output1 <= net6;
   end architecture rtl;

Verilog-HDL 出力

::

   module ent(
     input  input1,
     input  input2,
     input  input3,
     output output1
   );
     wire net1;
     wire net2;
     wire net3;
     wire net4;
     wire net5;
     wire net6;
     and item1(.input1(net1), .input2(net2), .output(net3));
     and item2(.input1(net4), .input2(net5), .output(net6));
     assign net1    = input1;
     assign net2    = input2;
     assign net4    = net3;
     assign net5    = input3;
     assign output1 = net6;
   endmodule // ent


2.6 順序回路用プロセス
^^^^^^^^^^^^^^^^^^^^^^^

RTL記述の一般的なスタイルではエンティティ直下には
if文やcase文のような動作記述を置くことができない．
そのために「プロセス」と呼ばれる構成要素を用いて
その中で動作記述を行う．
同期式順序回路を記述するためには ``Entity.add_clocked_process()``
を用いる．
``add_clocked_process`` の引数は以下の通り．

+------------------+----------+------------------+--------------------+
| パラメータ名     | 型       | 説明             | 省略(デフォルト値) |
+==================+==========+==================+====================+
| ``name``         | str      | 名前             | 可(None)           |
+------------------+----------+------------------+--------------------+
| ``clock``        | Expr     | クロック信号線   | 不可               |
+------------------+----------+------------------+--------------------+
| ``clock_pol``    | str      | クロックの極性   | 不可               |
+------------------+----------+------------------+--------------------+
| ``asyncctl``     | Expr     | 非同期制御信号線 | 可(None)           |
+------------------+----------+------------------+--------------------+
| ``asyncctl_pol`` | str      | 非同期制御の極性 | 可(None)           |
+------------------+----------+------------------+--------------------+

すべてのパラメータは名前付きのオプション引数である．
クロックと非同期制御が省略された場合には組み合わせ回路用の
プロセスが生成される．
このメソッドは ``ClockedProcess`` クラスのオブジェクトを返す．

``ClockedProcess`` クラスのメンバは以下の通り

+---------------------------+----------------+----------------------------------------------+
| メンバ名                  | 型             | 説明                                         |
+===========================+================+==============================================+
| ``add_async_stmt(stmt)``  | 関数           | 非同期制御ブロックにステートメントを追加する |
+---------------------------+----------------+----------------------------------------------+
| ``add_body_stmt(stmt)``   | 関数           | 本体ブロックにステートメントを追加する．     |
+---------------------------+----------------+----------------------------------------------+
| ``clock``                 | Expr           | クロック信号線                               |
+---------------------------+----------------+----------------------------------------------+
| ``clock_pol``             | str            | クロックの極性                               |
+---------------------------+----------------+----------------------------------------------+
| ``asyncctl``              | Expr           | 非同期制御信号線                             |
+---------------------------+----------------+----------------------------------------------+
| ``asyncctl_pol``          | str            | 非同期制御の極性                             |
+---------------------------+----------------+----------------------------------------------+
| ``process_body()``        | StmtContext    | 全体のブロック                               |
+---------------------------+----------------+----------------------------------------------+
+---------------------------+----------------+----------------------------------------------+
| ``asyncctl_body()``       | StmtContext    | 非同期制御ブロック                           |
+---------------------------+----------------+----------------------------------------------+
| ``body``                  | StmtContext    | 本体ブロック                                 |
+---------------------------+----------------+----------------------------------------------+

クラス ``StmtContext`` はステートメントブロックを表すクラスである．
通常はこのクラスに対してステートメントを追加することになる．
ただし， ``add_async_stmt()`` や ``add_body_stmt()`` を使って
ステートメントを追加することもできる．
注意が必要なのは ``body()`` と ``process_body()`` で，
もしも非同期制御がない場合はこの2つは同じものとなるが，
非同期制御がある場合は ``process_body()`` は非同期制御も含んだ全体のブ
ロックを表し，
``body()`` が非同期制御以外の本体のブロックを表す．
通常は ``process_body()`` を明示的に使う必要はない．

以下の例はイネーブル信号付きの1ビットのD-FFの記述例である．
(D-FFは別途 ``add_dff()`` で作成することもできる)
``with`` 構文に関しては2.8.4の ``StmtContext`` を参照のこと
::

   from rtlgen import EntityMgr, Expr

   mgr = EntityMgr()

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

この ``ent1`` に対する VHDL 出力は以下の様になる．

::

   library IEEE;
   use IEEE.std_logic_1164.all;

   entity dff1 is
     port (
       data_in : in  std_logic;
       enable  : in  std_logic;
       clock   : in  std_logic;
       q       : out std_logic
     );
   end entity dff1;

   architecture rtl of dff1 is
     signal net1 : std_logic;
   begin
     item1: process ( clock ) begin
       if rising_edge(clock) then
         if enable then
           net1 <= data_in;
         end if;
       end if;
     end process item1;

     q <= net1;
   end architecture rtl;

同様に ``ent1`` に対する Verilog-HDL 出力は以下の様になる．

::

   module dff1(
     input  data_in,
     input  enable,
     input  clock,
     output q
   );
     reg net1;

     always @( posedge clock ) begin
       if ( enable ) begin
         net1 <= data_in;
       end
     end

     assign q = net1;
   endmodule // dff1

次の例は ``asyncctl`` を用いた非同期リセット付きのD-FFの記述例である．
(繰り返すがD-FFなら後述の ``add_dff()`` を用いたほうが簡単に記述できる)

::

   # ~~省略~~

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

VHDL出力

::

   library IEEE;
   use IEEE.std_logic_1164.all;

   entity dff2 is
     port (
       data_in : in  std_logic;
       reset   : in  std_logic;
       clock   : in  std_logic;
       q       : out std_logic
     );
   end entity dff2;

   architecture rtl of dff2 is
     signal net1 : std_logic;
   begin
     item1: process ( clock, reset ) begin
       if reset = '0' then
         net1 <= '0';
       elsif rising_edge(clock) then
         net1 <= data_in;
       end if;
     end process item1;

     q <= net1;
   end architecture rtl;

Verilog-HDL 出力

::

   module dff2(
     input  data_in,
     input  reset,
     input  clock,
     output q
   );
     reg net1;

     always @( posedge clock or negedge reset ) begin
       if ( !reset ) begin
         net1 <= 1'b0;
       end
       else begin
         net1 <= data_in;
       end
     end

     assign q = net1;
   endmodule // dff2


2.7 組み合わせ回路用プロセス
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

if 文や case 文を用いて組み合わせ回路を記述する場合は
``Entity.add_comb_process()`` を用いる．
結果としてクラス ``CombProcess`` が返される．
内部にステートメントを追加する時には ``Process.body()`` を用い
る．

以下の例は3ビットのプライオリティエンコーダーの記述例である．

::

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

VHDL 出力

::

   library IEEE;
   use IEEE.std_logic_1164.all;

   entity comb1 is
     port (
       a : in  std_logic;
       b : in  std_logic;
       c : in  std_logic;
       o : out std_logic_vector(1 downto 0)
     );
   end entity comb1;

   architecture rtl of comb1 is
     signal net1 : std_logic;
   begin
     item1: process ( ) begin
       begin
         net1 <= "00";
         if a then
           net1 <= "01";
         else
           if b then
             net1 <= "10";
           else
             if c then
               net1 <= "11";
             end if;
           end
         end
       end
     end process item1;

     o <= net1;
   end architecture rtl;

Verilog-HDL 出力

::

   module comb1(
     input        a,
     input        b,
     input        c,
     output [1:0] o
   );
     reg net1;

     always @* begin
       net1 <= 2'b00;
       if ( a ) begin
         net1 <= 2'b01;
       end
       else begin
         if ( b ) begin
           net1 <= 2'b10;
         end
         else begin
           if ( c ) begin
             net1 <= 2'b11;
           end
         end
       end
     end

     assign o = net1;
   endmodule // comb1


2.8 ステートメント
^^^^^^^^^^^^^^^^^^^

プロセス内の動作記述を行うための構成要素でる．
直接ステートメントのクラスを生成することはせず，
クラス ``StatementBlock`` のメソッドを用いて生成する．
なお， ``StatementBlock`` は ``Process`` や ``Statement``
内部に生成されるものでこのクラス自体も直接生成することはない．

+------------------------------------+-----------------------------+
| メソッド名                         | 説明                        |
+====================================+=============================+
| ``add_assign(lhs, rhs, blocking)`` | 代入文を追加する．          |
+------------------------------------+-----------------------------+
| ``add_if(cond)``                   | IF文を追加する．            |
+------------------------------------+-----------------------------+
| ``add_case(cond)``                 | CASE文を追加する．          |
+------------------------------------+-----------------------------+

2.8.1 代入文
^^^^^^^^^^^^^^

``add_assign()`` の ``lhs`` ， ``rhs`` は ``Expr`` タイプのオブジェクト
でそれぞれ，左辺式，右辺式を指定する．
``blocking`` は ``bool`` 型の変数で ``True`` の時にブロッキング代入文
を， ``False`` の時にはノンブロッキング代入文を生成する．

2.8.2 IF文
^^^^^^^^^^^

``add_if()`` の ``cond`` は ``Expr`` タイプのオブジェクトで，
IF文の条件式を指定する．
この時点ではTHEN節もELSE節も空の状態である．

THEN節とELSE節はそれぞれ ``If.then_body()`` ，
``If.else_body()`` でアクセスすることができる．
これらは内部では ``StatementBlock`` タイプのオブジェクトとして
表されるが``If.then_body()`` ，``If.else_body()`` の返り値は
後述の ``StmtContext`` になっている．
IF文の使用例はプロセスの項を参照のこと．

2.8.3 CASE文
^^^^^^^^^^^^^

``add_case()`` の ``cond`` は ``Expr`` タイプのオブジェクトで，
CASE文の条件式を指定する．
この時点ではCASE文の本体は空の状態である．
本体にラベルを追加するには ``Case.add_label(label)``
を用いる． ``label`` はラベルを表す ``Expr``
タイプのオブジェクトを指定する．
このメソッドはこのラベルに対応するステートメントブロックの
``StmtContext`` を返す．

以下の例は4入力マルチプレクサ(セレクタ)をcase文で記述したものである．

::

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


Verilog-HDL 出力

::

   module comb1(
     input        a,
     input        b,
     input        c,
     input        d,
     input  [1:0] sel,
     output       o
   );
     reg net1;

     always @* begin
       case ( sel )
         2'b00:

           begin
             net1 <= a;
           end
         2'b01:

           begin
             net1 <= b;
           end
         2'b10:

           begin
             net1 <= c;
           end
         2'b11:

           begin
             net1 <= d;
           end
       endcase
     end

     assign o = net1;
   endmodule // comb1


2.8.4 ``StatementBlock`` と ``StmtContext``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

複数のステートメントをグループ化したものをステートメントブロックと呼ぶ．
内部ではクラス ``StatementBlock`` で表される．
通常のRTL記述ではステートメントブロック内の記述はインデントしており，
一見してブロック内の記述とわかりやすいが，
RtlGen ではインデントしていないため可読性が悪い．
そこで，Python の with 構文を使ってブロック内の記述をインデントした
Python のブロック内で記述できるようにしている．
具体的には ``with StmtContext as var:``
という記述で with ブロックを構成する．
この構文は ``:`` で終わっているので Python のブロック構造の始まりを
表している．
続く文はインデントしなければならず，インデントが終わった時点で
このブロックの終了を表す．
通常はブロックの始まりと終わりのタイミングで特定の処理
(ファイルのオープンとクローズなど)を行う目的で用いられるが，
ここではただ単にインデントを行うために用いている．
with 構文の後半の `` as var`` はブロック内でのみ有効な変数で，
ここでは対応する ``StatementBlock`` が ``var`` に代入される．
通常はこの ``StatementBlock`` に対してステートメントの追加を行う．
この変数名に関しては特に制約はないので自由に名前を付けてよいが，
ブロックがネストした時に複数の名前があるとかえって分かりづらいので，
ここで用いている例のようにすべて ``_`` にしてしまうというやり方もある．
以下にIF文の使用例を示す．

::

   ...
   if_stmt = block.add_if(cond)
   with if_stmt.then_body() as _:
     _.add_assign(x, a + 1)
     if2 = _.add_if(y)
     with if2.then_body() as _:
       _.add_assign(x, a)
   with if_stmt.else_body() as _:
     _.add_assign(x, a - 1)

の様に記述する．

``StmtContext`` は ``Process.process_body()`` ，
``Process.asyncctl_body()`` ， ``Process.body()`` ，
``CombProcess.body()`` ，
``IfStmt.then_body()`` ， ``IfStmt.else_body()`` ，
``CaseStmt.add_label()`` の結果として返される．


3. 拡張型の構成要素
--------------------

前述の構成要素を組み合わせることで合成可能なRTL記述をほぼ
自由に生成することができるが，プロセスとステートメントの記述方法
は少し煩雑である．
そこでよく用いる記述を拡張型の構成要素として用意してる．
なお，これらの拡張型はすべて RTL-gen の構成要素を用いて記述されている．
これ以外にも同様に拡張型の構成要素を追加することは容易に行える．


3.1 D-FF
^^^^^^^^^

D-FF に対応する要素を ``Entity.add_dff()`` で追加することができる．
``add_dff`` の引数は以下の通り．

+------------------+----------+-----------------------------+
| パラメータ名     | 型       | 説明                        |
+==================+==========+=============================+
| ``name``         | str      | 名前                        |
+------------------+----------+-----------------------------+
| ``data_in``      | Expr     | データ入力                  |
+------------------+----------+-----------------------------+
| ``data_type``    | DatType  | データ入出力の型            |
+------------------+----------+-----------------------------+
| ``clock``        | Expr     | クロック入力                |
+------------------+----------+-----------------------------+
| ``clock_edge``   | str      | クロックのアクティブエッジ  |
+------------------+----------+-----------------------------+
| ``reset``        | Expr     | リセット入力                |
+------------------+----------+-----------------------------+
| ``reset_pol``    | str      | リセットの極性              |
+------------------+----------+-----------------------------+
| ``reset_val``    | Expr     | リセット値                  |
+------------------+----------+-----------------------------+
| ``enable``       | Expr     | イネーブル入力              |
+------------------+----------+-----------------------------+
| ``enable_pol``   | str      | イネーブルの極性            |
+------------------+----------+-----------------------------+

これらのパラメータのうち， ``data_in`` か ``data_type``
のいずれか一方は必ず指定する必要がある．
また，``clock`` は省略されても端子は生成されて未接続となる．
それ以外の ``reset`` と ``enable`` は省略された場合には
それぞれの端子を持たない要素が生成される．

``clock_edge`` には "positive" か "negative" の文字列を与える．
それぞれ，立ち上がりエッジ，立ち下がりエッジを表す．
省略時には "positive" が指定されたものとみなす．

``reset_pol`` も "positive" か "negative" の文字列を与える．
省略時のには "positive" が指定されたものとみなす．
``reset_val`` にはリセット時の値を与える．
``reset`` が指定された場合， ``reset_val`` は必須である．

``enable_pol`` も "positive" か "negative" の文字列を与える．
省略時のには "positive" が指定されたものとみなす．

``add_dff()`` は生成した D-FF のインスタンスを表す Python オブジェクト
を返す．この D-FF の入出力端子はそれぞれ
``.data_in`` , ``.clock`` , ``.reset`` , ``.enable`` , ``.q``
でアクセスできる．

::

   from rtlgen import EntityMgr

   mgr = EntityMgr()
   ent = mgr.add_entity('dff_test1')
   clock = ent.add_input_port(name='clock')
   data_in = ent.add_input_port(name='data_in')
   data_out = ent.add_output_port(name='data_out')
   dff = ent.add_dff(clock=clock, clock_edge='positive',
                         data_in=data_in)
   ent.connect(data_out, dff.q)

この例ではデータ入出力とクロックのみをもつ簡単な D-FF
を生成している．

VHDL 出力

::

   library IEEE;
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


Verilog-HDL

::

   module dff_test1(
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


3.2 LookUp Table
^^^^^^^^^^^^^^^^^^

表引きで入力に対応した出力を返す組み合わせ回路を表す構成要素は
``Entity.add_lut`` で追加することができる．

パラメータは以下の通り．

+--------------+------------------+------------------+
| パラメータ名 | 型               | 説明             |
+==============+==================+==================+
| input_bw     | int              | 入力のビット幅   |
+--------------+------------------+------------------+
| data_type    | DataType         | 出力の型         |
+--------------+------------------+------------------+
| data_list    | list(Expr, Expr) | 表データのリスト |
+--------------+------------------+------------------+

``data_list`` は ``(入力値, 出力値)`` のリストである．
順序に関してはなんの制約もない．
回路として正しく動作するためにはすべての入力値に対して
対応する出力値を指定する必要があるが，
rtlgen ではデータの正当性の検証は行っていない．

``data_list`` を与えなかった場合は ``Lut.add_data(ival, oval)``
でデータを追加する．
ここで ``ival`` , ``oval`` はそれぞれ入力値，出力値を表す．

以下は3ビットアドレスデコーダーの例である．

::

   from rtlgen import EntityMgr, DataType, Expr

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


VHDL 出力

::

   library IEEE;
   use IEEE.std_logic_1164.all;

   entity lut1 is
     port (
       input  : in  std_logic_vector(2 downto 0);
       output : out std_logic_vector(7 downto 0)
     );
   end entity lut1;

   architecture rtl of lut1 is
     signal net1 : std_logic_vector(2 downto 0);
     signal net2 : std_logic_vector(7 downto 0);
   begin
     item1: process ( net1 ) begin
       case net1 is
         when "000"  => net2 <= "00000001";
         when "001"  => net2 <= "00000010";
         when "010"  => net2 <= "00000100";
         when "011"  => net2 <= "00001000";
         when "100"  => net2 <= "00010000";
         when "101"  => net2 <= "00100000";
         when "110"  => net2 <= "01000000";
         when "111"  => net2 <= "10000000";
         when others => null;
       end case;
     end process item1;

     net1   <= input;
     output <= net2;
   end architecture rtl;


Verilog-HDL 出力

::

   module lut1(
     input  [2:0] input,
     output [7:0] output
   );
     wire [2:0] net1;
     reg  [7:0] net2;
     always ( * ) begin
       case ( net1 )
         3'b000:  net2 <= 8'b00000001;
         3'b001:  net2 <= 8'b00000010;
         3'b010:  net2 <= 8'b00000100;
         3'b011:  net2 <= 8'b00001000;
         3'b100:  net2 <= 8'b00010000;
         3'b101:  net2 <= 8'b00100000;
         3'b110:  net2 <= 8'b01000000;
         3'b111:  net2 <= 8'b10000000;
         default: ;;
       endcase
     end

     assign net1   = input;
     assign output = net2;
   endmodule // lut1
