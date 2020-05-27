#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step06_remove_some_useless_data
# @Date: 2020/5/25
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m OrganizeData.PrepareRegressionData.step06_remove_some_useless_data
"""

import os

import pandas as pd
from pandas import DataFrame

from Constants import Constants as const

if __name__ == '__main__':
    reg_df: DataFrame = pd.read_pickle(
        os.path.join(const.TEMP_PATH, '20200525_democracy_investment_regression_data.pkl'))
    cite_related_vars = "cite_home_ln_1 patent_home_ln_1 patent_us_ln_1 cite_us_ln_1 exploit_rate_1 " \
                        "explore_rate_1 originality_1 generality_1".split(' ')
    reg_df_valid: DataFrame = reg_df.loc[reg_df['country_name'] != 'United States'].copy()
    valid_data_list = list()
    for c in reg_df_valid['country_name'].drop_duplicates():
        tmp_df: DataFrame = reg_df_valid.loc[reg_df_valid['country_name'] == c].copy()
        if tmp_df.dropna(subset=cite_related_vars, how='all').empty:
            continue
        else:
            valid_data_list.append(tmp_df)

    valid_reg_df: DataFrame = pd.concat(valid_data_list)
    valid_reg_df.to_pickle(os.path.join(const.TEMP_PATH, '20200525_demoinnovation_data_file.pkl'))
    valid_reg_df.to_stata(os.path.join(const.RESULT_PATH, '20200525_demoinnovation_data_file.dta'), write_index=False)