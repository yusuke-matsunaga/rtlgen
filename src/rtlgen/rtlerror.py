#! /usr/bin/env python3

"""

:file: rtlerror.py
:author: Yusuke Matsunaga (松永 裕介)
:copyright: Copyright (C) 2022 Yusuke Matsunaga, All rights reserved.
"""


class RtlError(Exception):
    """Rtlgen の生成する例外"""

    def __init__(self, message):
        self.message = message
