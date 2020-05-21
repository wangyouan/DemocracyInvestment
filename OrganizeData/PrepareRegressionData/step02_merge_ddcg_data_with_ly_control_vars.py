#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step02_merge_ddcg_data_with_ly_control_vars
# @Date: 2020/5/15
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m OrganizeData.PrepareRegressionData.step02_merge_ddcg_data_with_ly_control_vars
"""

import os

import pandas as pd
from pandas import DataFrame

from Constants import Constants as const

if __name__ == '__main__':
    ddcg_df: DataFrame = pd.read_pickle(os.path.join(const.TEMP_PATH, '20200515_country_year_democracy_measure.pkl'))
    ROOT_PATH = '/home/zigan/Documents/wangyouan/research/FxVolatilityCSR'
    DATA_PATH = os.path.join(ROOT_PATH, 'data')
    ly_ctrl_df: DataFrame = pd.read_pickle(os.path.join(DATA_PATH, 'LiYan', 'fx_volatility.pkl')).drop(
        ['country'], axis=1)
    ly_ctrl_df[const.WB_CODE] = ly_ctrl_df['loc'].replace({'TWN': 'TAW', 'ARE': 'UAE', 'ROU': 'ROM',
                                                           'SGP': 'SIN', 'SRB': 'SER'})
    ddcg_with_ctrl: DataFrame = ddcg_df.merge(ly_ctrl_df, on=[const.WB_CODE, const.YEAR], how='left')
    ddcg_with_ctrl.to_pickle(os.path.join(const.TEMP_PATH, '20200515_democracy_with_ctrl.pkl'))
