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

import numpy as np
import pandas as pd
from pandas import DataFrame

from Constants import Constants as const

if __name__ == '__main__':
    # Load Freedom House data and Polity IV data
    fh_df: DataFrame = pd.read_pickle(
        os.path.join(const.TEMP_PATH, '20201210_fh_rankings_1973_2018.pkl')).drop_duplicates(
        subset=['scode', 'year'], keep='first').rename(columns={'scode': 'country_iso3'})
    fh_df.loc[:, 'DEMOC_FREE_HOUSE'] = fh_df['status'].apply(lambda x: int(x in {'PF', 'F', 'PF ', 'F '}))
    p5_df: DataFrame = pd.read_pickle(os.path.join(const.TEMP_PATH, '20201210_p5_v2018.pkl')).drop_duplicates(
        subset=['scode', 'year'], keep='first').rename(
        columns={'scode': 'country_iso3', 'democ': 'DEMOC_POLITY_IV', 'autoc': 'AUTOC_POLITY_IV',
                 'xrcomp': 'COMP_EXEC_RCT', 'xropen': 'OPEN_EXEC_RCT', 'xconst': 'CONS_EXEC', 'parcomp': 'COMP_PAR',
                 'polity2': 'POLITY_IV_SCORE'}).replace([-66, -88, -99], np.nan).replace({-77: 0})

    # Load Data (BMR)
    bmr_df = pd.read_csv(os.path.join(const.DATA_PATH, 'democracy_BMR.csv')).dropna(subset=['democracy'])
    bmr_df.loc[bmr_df['country'] == 'MONTENEGRO', 'abbreviation'] = 'MNE'
    bmr_df.loc[:, 'country_iso3'] = bmr_df['abbreviation'].replace({'ROM': 'ROU', 'SWD': 'SWE'}).fillna(
        bmr_df['abbreviation_undp'])
    bmr_df = bmr_df.drop_duplicates(subset=['country_iso3', 'year'])
    bmr_df['year'] = bmr_df['year'].astype(int)

    # Load Data (CGV)
    use_cols = ['qogctylett', 'year', 'democracy']
    cgv_df = pd.read_excel(os.path.join(const.DATA_PATH, 'democracy_CGV.xls')).loc[:, use_cols]
    cgv_df.columns = ['country_iso3', 'year', 'DEMOC_CGV']
    cgv_df['year'] = cgv_df['year'].astype(int)

    # merge_data
    democracy_df: DataFrame = fh_df.loc[:, ['country_iso3', const.YEAR, 'DEMOC_FREE_HOUSE']].merge(
        p5_df.loc[:, ['country_iso3', const.YEAR, 'DEMOC_POLITY_IV', 'AUTOC_POLITY_IV', 'COMP_EXEC_RCT',
                      'POLITY_IV_SCORE', 'OPEN_EXEC_RCT', 'CONS_EXEC', 'COMP_PAR']],
        on=['country_iso3', const.YEAR], how='left').merge(
        bmr_df.loc[:, ['country_iso3', 'year', 'DEMOC_BMR']], on=['country_iso3', 'year'], how='left').merge(
        cgv_df, on=['country_iso3', const.YEAR], how='left')

    democracy_df.to_pickle(os.path.join(const.TEMP_PATH, '20201217_merged_democracy_measures.pkl'))

    # get ws country coverage
    ws_df: DataFrame = pd.read_pickle(os.path.join(const.DATA_PATH, 'worldscope_firm_characteristic.pkl'))
    ws_country_df: DataFrame = ws_df.loc[:, ['country_iso3']].drop_duplicates()
    ws_country_df.loc[:, 'ws_data'] = 1
    ws_demo_df: DataFrame = ws_country_df.merge(democracy_df, on=['country_iso3'], how='left')

    # check country list information
    # ['VIR', 'VGB', 'TWN', 'SVN', 'PSE', 'PRI', 'CYM', 'JEY', 'IMN', 'HKG', 'GIB', 'GGY', 'FRO', 'FLK', 'CUW', 'COK',
    # 'BMU', 'AIA']
    country_list = list()
    for i in ws_demo_df.country_iso3.unique():
        country_df = ws_demo_df.loc[ws_demo_df['country_iso3'] == i].copy()
        if country_df.loc[~country_df['DEMOC_FREE_HOUSE'].isnull()].empty:
            country_list.append(i)
    pd.to_pickle(country_list, os.path.join(const.TEMP_PATH, '20201217_country_invalid_information.pkl'))

    ws_demo_valid_df: DataFrame = ws_demo_df.loc[~ws_demo_df['country_iso3'].isin(country_list)].copy()

    ws_demo_valid_df.drop(['ws_data'], axis=1).to_pickle(
        os.path.join(const.TEMP_PATH, '20201217_worldscope_add_democracy_data.pkl'))
