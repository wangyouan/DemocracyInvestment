#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step05_append_some_dependent_variable
# @Date: 2020/5/23
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m OrganizeData.PrepareRegressionData.step04_preprocessing_patent_data
"""

import os

import numpy as np
import pandas as pd
from pandas import DataFrame
from scipy.stats.mstats import winsorize

from Constants import Constants as const

if __name__ == '__main__':
    # append rd expense variables
    ctat_df: DataFrame = pd.read_csv(
        os.path.join(const.DATABASE_PATH, 'Compustat', '198706_202003_global_compustat_all_fina_data.zip'),
        usecols=['at', 'gvkey', 'fyear', 'ppent', 'capx', 'che', 'ibc', 'dp', 'dvc', 'dvp', 'emp', 'sale', 'ebit',
                 'prstkc', 'ib'], dtype={'gvkey': str}
    ).rename(columns={'fyear': const.YEAR}).sort_values(const.YEAR, ascending=True).drop_duplicates(
        subset=[const.GVKEY, const.YEAR], keep='last')
    ctat_df.loc[:, 'lag_at'] = ctat_df.groupby('gvkey')['at'].shift(1)
    ctat_df.loc[:, 'CAPEX_AT'] = ctat_df['capx'] / ctat_df['lag_at']
    ctat_df.loc[:, 'TANGIBILITY'] = ctat_df['ppent'] / ctat_df['lag_at']
    ctat_df.loc[:, 'CASH_FLOW'] = (ctat_df['ibc'] + ctat_df['dp']) / ctat_df['lag_at']
    ctat_df.loc[:, 'CASH_HOLDING'] = ctat_df['che'] / ctat_df['lag_at']
    ctat_df.loc[:, 'PAYOUT_RATIO'] = ctat_df[['dvc', 'dvp', 'prstkc']].sum(axis=1, min_count=1) / ctat_df[
        'ib']
    ctat_df.loc[:, 'EMP_LN'] = ctat_df['emp'].apply(np.log)
    ctat_df.loc[:, 'EMP_AT'] = ctat_df['emp'] / ctat_df['lag_at']
    ctat_df.loc[:, 'ROA'] = ctat_df['ebit'] / ctat_df['lag_at']
    ctat_df.loc[:, 'ROS'] = ctat_df['ebit'] / ctat_df['sale']
    ctat_df_valid: DataFrame = ctat_df.drop(['lag_at'], axis=1).replace([np.inf, -np.inf], np.nan)
    for key in ['CAPEX_AT', 'TANGIBILITY', 'CASH_FLOW', 'CASH_HOLDING', 'PAYOUT_RATIO', 'EMP_LN', 'EMP_AT', 'ROA',
                'ROS']:
        ctat_df_valid.loc[ctat_df_valid[key].notnull(), '{}_win'.format(key)] = winsorize(ctat_df_valid[key].dropna(),
                                                                                          limits=(0.01, 0.01))

    reg_df: DataFrame = pd.read_pickle(
        os.path.join(const.TEMP_PATH, '20200525_democracy_innovation_preliminary_reg_data.pkl'))

    reg_df_2: DataFrame = reg_df.merge(ctat_df_valid, on=[const.GVKEY, const.YEAR], how='left')
    ctat_df.loc[:, const.YEAR] -= 1
    reg_df_3: DataFrame = reg_df_2.merge(ctat_df_valid, on=[const.GVKEY, const.YEAR], how='left', suffixes=['', '_1'])
    reg_df_3.to_pickle(os.path.join(const.TEMP_PATH, '20200525_democracy_investment_regression_data.pkl'))
    reg_df_3.to_stata(os.path.join(const.RESULT_PATH, '20200525_democracy_investment_regression_data.dta'),
                      write_index=False)
