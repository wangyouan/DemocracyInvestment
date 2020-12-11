#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step10_reconstruct_democracy_measure
# @Date: 2020/12/10
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m OrganizeData.PrepareRegressionData.step10_reconstruct_democracy_measure
"""

import os

import pandas as pd
from pandas import DataFrame

from Constants import Constants as const

if __name__ == '__main__':
    ws_df: DataFrame = pd.read_pickle(os.path.join(const.DATA_PATH, 'worldscope_firm_characteristic.pkl'))
    fh_df: DataFrame = pd.read_pickle(
        os.path.join(const.TEMP_PATH, '20201210_fh_rankings_1973_2018.pkl')).drop_duplicates(
        subset=['scode', 'year'], keep='first').rename(columns={'scode': 'country_iso3'}).replace(const.SCODE2ISO_DICT)
    fh_df.loc[:, 'DEMOC_FREE_HOUSE'] = fh_df['status'].apply(lambda x: int(x in {'PF', 'F', 'PF ', 'F '}))
    p5_df: DataFrame = pd.read_pickle(os.path.join(const.TEMP_PATH, '20201210_p5_v2018.pkl')).drop_duplicates(
        subset=['scode', 'year'], keep='first').rename(columns={'scode': 'country_iso3', 'democ': 'DEMOC_POLITY_IV',
                                                                'autoc': 'AUTOC_POLITY_IV', 'xrcomp': 'COMP_EXEC_RCT',
                                                                'xropen': 'OPEN_EXEC_RCT', 'xconst': 'CONS_EXEC',
                                                                'parcomp': 'COMP_PAR'}).replace(const.SCODE2ISO_DICT)

    # Load Data (BMR)
    bmr_df = pd.read_csv(os.path.join(const.DATA_PATH, 'democracy_BMR.csv'),
                         usecols=['abbreviation', 'year', 'democracy'])[:-1]
    bmr_df.columns = ['country_iso3', 'year', 'DEMOC_BMR']
    bmr_df.loc[:, 'country_iso3'] = bmr_df['country_iso3'].replace(const.SCODE2ISO_DICT).replace(
        {'UK': 'GBR', 'ADO': 'AND', 'SMA': 'SMR', 'ICE': 'ISL'})
    bmr_df['year'] = bmr_df['year'].astype(int)

    # Load Data (CGV)
    use_cols = ['qogctylett', 'year', 'democracy']
    cgv_df = pd.read_excel(os.path.join(const.DATA_PATH, 'democracy_CGV.xls')).loc[:, use_cols]
    cgv_df.columns = ['country_iso3', 'year', 'DEMOC_CGV']
    cgv_df['year'] = cgv_df['year'].astype(int)

    # merge_data
    democracy_df: DataFrame = fh_df.loc[:, ['country_iso3', const.YEAR, 'DEMOC_FREE_HOUSE']].merge(
        p5_df.loc[:, ['country_iso3', const.YEAR, 'DEMOC_POLITY_IV', 'AUTOC_POLITY_IV', 'COMP_EXEC_RCT',
                      'OPEN_EXEC_RCT', 'CONS_EXEC', 'COMP_PAR']], on=['country_iso3', const.YEAR], how='left').merge(
        bmr_df, on=['country_iso3', const.YEAR], how='left').merge(cgv_df, on=['country_iso3', const.YEAR])

    democracy_df.to_pickle(os.path.join(const.TEMP_PATH, '20201211_merged_democracy_measures.pkl'))
