#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step09_check_worldscope_data_coverage
# @Date: 2020/12/10
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

import os

import pandas as pd
from pandas import DataFrame

from Constants import Constants as const

if __name__ == '__main__':
    # obtain fh country code coverage
    fh_df: DataFrame = pd.read_excel(os.path.join(const.DATA_PATH, 'fh_rankings_1973_2018.xlsx'), sheet_name='Data')
    fh_df.loc[:, 'scode'] = fh_df['scode'].replace(const.SCODE2ISO_DICT).replace(
        {'ROM': 'ROU', 'AAB': 'ATG', 'BAR': 'BRB', 'BHM': 'BHS', 'CDI': 'CIV', 'DMA': 'DOM', 'ICE': 'ISL', 'MNC': 'MCO',
         'MNG': 'MNE', 'SLU': 'LCA', 'SWZ': 'CHE', 'SLV': 'SNV'})
    fh_df.to_pickle(os.path.join(const.TEMP_PATH, '20201210_fh_rankings_1973_2018.pkl'))
    fh_country_group: DataFrame = fh_df.loc[:, ['scode', 'year', 'country']].groupby(['scode', 'country'])
    fh_start_year = fh_country_group['year'].min()
    fh_end_year = fh_country_group['year'].max()
    fh_country_coverage = DataFrame({'start_year': fh_start_year, 'end_year': fh_end_year}).reset_index(drop=False)

    # obtain Policy IV country code coverage
    p5_df: DataFrame = pd.read_excel(os.path.join(const.DATA_PATH, 'p5v2018.xls'))
    p5_df.loc[:, 'scode'] = p5_df['scode'].replace(const.SCODE2ISO_DICT).replace(
        {'MNT': 'MNE', 'PKS': 'PAK', 'SWZ': 'CHE', 'SLV': 'SNV'})
    p5_df.to_pickle(os.path.join(const.TEMP_PATH, '20201210_p5_v2018.pkl'))

    p5_country_group: DataFrame = p5_df.loc[:, ['scode', 'year', 'country']].groupby(['scode', 'country'])
    p5_start_year = p5_country_group['year'].min()
    p5_end_year = p5_country_group['year'].max()
    p5_country_coverage = DataFrame({'start_year': p5_start_year, 'end_year': p5_end_year}).reset_index(drop=False)

    p5_fh_combined_df: DataFrame = p5_country_coverage.merge(fh_country_coverage, on=['scode'], suffixes=['_p5', '_fh'],
                                                             how='outer')

    # obtain Worldscope country code coverage
    wc_df_coverage: DataFrame = pd.read_pickle(os.path.join(const.DATA_PATH, 'worldscope_data_country_coverage.pkl'))
    merged_df: DataFrame = wc_df_coverage.merge(p5_fh_combined_df, left_on=['country_iso3'], right_on=['scode'],
                                                how='left')
    merged_df.to_excel(os.path.join(const.RESULT_PATH, '20201210_worldscope_country_data_coverage.xlsx'), index=False)
