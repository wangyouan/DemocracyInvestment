#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step03_merge_innovation_data
# @Date: 2020/5/21
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m OrganizeData.PrepareRegressionData.step03_merge_innovation_data
"""

import os

import pandas as pd
from pandas import DataFrame
from scipy.stats.mstats import winsorize

from Constants import Constants as const

if __name__ == '__main__':
    ddcg_df: DataFrame = pd.read_pickle(os.path.join(const.TEMP_PATH, '20200515_democracy_with_ctrl.pkl'))
    innovation_df: DataFrame = pd.read_pickle(
        os.path.join(const.TEMP_PATH, '20200522_innovation_related_variables.pkl'))
    for key in ['R_D_LN', 'R_D_RATIO', 'cite_us_ln', 'patent_us_ln', 'patent_home_ln', 'cite_home_ln']:
        innovation_df.loc[innovation_df[key].notnull(), '{}_win'.format(key)] = winsorize(innovation_df[key].dropna(),
                                                                                          limits=(0.01, 0.01))

    ddcg_df2: DataFrame = ddcg_df.merge(innovation_df.drop(['isin', 'sedol'], axis=1), on=[const.GVKEY, const.YEAR],
                                        how='left')
    innovation_df.loc[:, const.YEAR] -= 1
    ddcg_df3: DataFrame = ddcg_df2.merge(innovation_df.drop(['isin', 'sedol'], axis=1), on=[const.GVKEY, const.YEAR],
                                         how='left', suffixes=['', '_1'])
    ddcg_df3.to_pickle(os.path.join(const.TEMP_PATH, '20200525_democracy_innovation_preliminary_reg_data.pkl'))
    # ddcg_df3.to_stata(os.path.join(const.RESULT_PATH, '20200525_democracy_innovation_preliminary_reg_data.dta'),
    #                   write_index=False)
