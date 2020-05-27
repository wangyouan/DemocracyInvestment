#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step07_construct_capex_related_variables
# @Date: 2020/5/27
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

import os

import numpy as np
import pandas as pd
from pandas import DataFrame
from scipy.stats.mstats import winsorize

from Constants import Constants as const

if __name__ == '__main__':
    reg_df: DataFrame = pd.read_pickle(os.path.join(const.TEMP_PATH, '20200525_demoinnovation_data_file.pkl'))
    reg_df.loc[:, 'CAPEX_LN_1'] = reg_df['capx_1'].apply(np.log)
    reg_df.loc[:, 'CAPEX_LAGPPENT_1'] = reg_df['capx_1'] / reg_df['ppent']
    reg_df: DataFrame = reg_df.replace([np.inf, -np.inf], np.nan)
    reg_df.loc[reg_df['CAPEX_LN_1'].notnull(), 'CAPEX_LN_win_1'] = winsorize(reg_df['CAPEX_LN_1'].dropna(),
                                                                             (0.01, 0.01))
    reg_df.loc[reg_df['CAPEX_LAGPPENT_1'].notnull(), 'CAPEX_LAGPPENT_win_1'] = winsorize(
        reg_df['CAPEX_LAGPPENT_1'].dropna(), (0.01, 0.01))

    reg_dfs = list()
    for c in reg_df['country_name'].drop_duplicates():
        tmp_df: DataFrame = reg_df.loc[reg_df['country_name'] == c].copy()
        if tmp_df['dem'].drop_duplicates().size == 1:
            tmp_df.loc[:, 'dem_change'] = 0
        else:
            tmp_df.loc[:, 'dem_change'] = 1
        reg_dfs.append(tmp_df)

    reg_df2: DataFrame = pd.concat(reg_dfs)
    reg_df2.to_pickle(os.path.join(const.TEMP_PATH, '20200527_demoinvestment_reg_data_file.pkl'))
    reg_df2.to_stata(os.path.join(const.RESULT_PATH, '20200527_demoinvestment_reg_data_file.dta'), write_index=False)
