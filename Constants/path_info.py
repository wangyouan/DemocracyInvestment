#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: path_info
# @Date: 2020/5/12
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

import os

class PathInfo(object):
    ROOT_PATH = '/home/zigan/Documents/wangyouan/research/DemocracyInvestment'

    DATA_PATH = os.path.join(ROOT_PATH, 'data')
    TEMP_PATH = os.path.join(ROOT_PATH, 'temp')
    RESULT_PATH = os.path.join(ROOT_PATH, 'output')

    PRE_ROOT_PATH = '/home/zigan/Documents/wangyouan/research/PoliticalConnections'
    PRE_DATA_PATH = os.path.join(PRE_ROOT_PATH, 'data')
    PRE_TEMP_PATH = os.path.join(PRE_ROOT_PATH, 'temp')
    PRE_RESULT_PATH = os.path.join(PRE_ROOT_PATH, 'output')

    STATA_PATH = os.path.join(ROOT_PATH, 'stata')
    STATA_RESULT_PATH = os.path.join(STATA_PATH, 'result')
    STATA_CODE_PATH = os.path.join(STATA_PATH, 'code')

    DATABASE_PATH = '/home/zigan/Documents/wangyouan/database'
