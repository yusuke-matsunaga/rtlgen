#! /usr/bin/env python3

"""線形有限状態機械を作る関数

:file: lfsm.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2024 Yusuke Matsunaga, All rights reserved.
"""

from rtlgen.entity import Entity
from rtlgen.data_type import DataType
from rtlgen.expr import Expr


def add_linear_fsm(ent, *,
                   k,
                   clock, clock_pol,
                   reset, reset_pol,
                   start):
    """線形に遷移する有限状態機械を追加する．
    :param Entity ent:       エンティティ
    :param int    k:         running 状態数
    :param Net    clock:     クロック信号名
    :param str    clock_pol: クロック信号のアクティブエッジ('positive'か'negative')
    :param Net    reset:     リセット信号
    :param str    reset_pol: リセット信号のアクティブエッジ('positive'か'negative')
    :param Net    start:     スタート信号   

    結果として (running, output) を返す．
    仕様は以下の通り．
    * wire                running: running 状態を表すフラグ
    * wire [log_k - 1: 0] count:   running 状態中のカウント
    
    * k個の running state と一つの idle state を持つ．
    * start 信号で running state に遷移する．
    * running state を K回遷移すると idle state に戻る．
    * running state にいる間は running 信号をアサートする．
    """

    # log(k) の計算
    log_k = 0
    while (1 << log_k) < k:
        log_k += 1

    # カウンタのデータ型
    count_type = DataType.bitvector_type(log_k)
    
    # 内部変数
    _running = ent.add_net(reg_type=True)
    _count = ent.add_net(data_type=count_type)

    # プロセスの生成
    main_proc = ent.add_clocked_process(clock=clock, clock_pol=clock_pol,
                                        asyncctl=reset, asyncctl_pol=reset_pol)

    # 定数
    bit_0 = Expr.make_constant(val=0)
    bit_1 = Expr.make_constant(val=1)
    count_0 = Expr.make_constant(val=0, data_type=count_type)
    count_1 = Expr.make_constant(val=1, data_type=count_type)
    count_max = Expr.make_constant(val=(k - 1), data_type=count_type)

    # リセット動作
    with main_proc.asyncctl_body() as _:
        _.add_assign(_running, bit_0)
        
    # 通常動作
    # if ( _running ) { // if_1
    #     counter <= counter + 1
    #     if ( _count == count_max ) { // if_2
    #         _running <= 0
    #     }
    # }
    # else if ( start ) { // if_3
    #     _running <= 1
    #     _count <= 0
    # }
    with main_proc.body() as _:
        if_1 = _.add_if(_running)
        with if_1.then_body() as _:
            _.add_assign(_count, _count + count_1)
            if_2 = _.add_if(_count == count_max)
            with if_2.then_body() as _:
                _.add_assign(_running, bit_0)
        with if_1.else_body() as _:
            if_3 = _.add_if(start)
            with if_3.then_body() as _:
                _.add_assign(_running, bit_1)
                _.add_assign(_count, count_0)

    return (_running, _count)


# Entity のメンバ関数に追加する．
Entity.add_linear_fsm = add_linear_fsm
