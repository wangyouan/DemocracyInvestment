#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step01_merge_oecd_data
# @Date: 2020/10/11
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m CollectData.step01_merge_oecd_data
"""

import os

import pandas as pd
from pandas import DataFrame

from Constants import Constants as const

if __name__ == '__main__':
    epsi_df: DataFrame = pd.read_csv(os.path.join(const.DATA_PATH, 'oecd', 'enviromental_policy_stringency_index.csv'),
                                     usecols=['COU', 'VAR', 'Year', 'Value']).rename(columns={'Year': const.YEAR,
                                                                                              'COU': const.WB_CODE})
    epsi_df.loc[:, 'VAR'] = epsi_df['VAR'].replace(lambda x: 'ENV_POLICY_{}'.format(x))
    epsi_vars = epsi_df['VAR'].drop_duplicates()
    epsi_country_year_df = DataFrame(columns=[const.WB_CODE, const.YEAR])
    for var in epsi_vars:
        tmp_df: DataFrame = epsi_df.loc[epsi_df['VAR'] == var].rename(columns={'Value': var}).drop(['VAR'], axis=1)
        epsi_country_year_df: DataFrame = epsi_country_year_df.merge(tmp_df, on=[const.WB_CODE, const.YEAR],
                                                                     how='outer')

    et_df: DataFrame = pd.read_csv(os.path.join(const.DATA_PATH, 'oecd', 'environmental_tax.csv'),
                                   usecols=['LOCATION', 'SUBJECT', 'MEASURE', 'TIME', 'Value']).rename(
        columns={'TIME': const.YEAR, 'LOCATION': const.WB_CODE})
    et_df.loc[:, 'VAR'] = et_df.apply(lambda x: '{}_{}'.format(x['SUBJECT'], x['MEASURE']), axis=1)
    et_country_year_df = DataFrame(columns=[const.WB_CODE, const.YEAR])
    for var in et_df['VAR'].drop_duplicates():
        tmp_df: DataFrame = et_df.loc[et_df['VAR'] == var].rename(columns={'Value': var}).drop(
            ['VAR', 'SUBJECT', 'MEASURE'], axis=1)
        et_country_year_df: DataFrame = et_country_year_df.merge(tmp_df, on=[const.WB_CODE, const.YEAR],
                                                                 how='outer')

    oecd_env_df: DataFrame = et_country_year_df.merge(epsi_country_year_df, on=[const.WB_CODE, const.YEAR], how='outer')
    oecd_env_df.to_csv(os.path.join(const.RESULT_PATH, '20201011_oecd_env_regulation.csv'), index=False)
