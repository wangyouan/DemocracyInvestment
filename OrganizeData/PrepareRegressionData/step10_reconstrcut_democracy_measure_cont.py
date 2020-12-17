#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step10_reconstrcut_democracy_measure_cont
# @Date: 2020/12/11
# @Author: Mark Wang
# @Email: wangyouan@gamil.com


"""
http://147.8.118.96:8888/notebooks/Project/Democracy/democracy_construction_redo.ipynb

python -m OrganizeData.PrepareRegressionData.step10_reconstrcut_democracy_measure_cont
"""

import os

import numpy as np
import pandas as pd
from pandas import DataFrame

if __name__ == '__main__':
    # Load Data (CNTS) -- Unrest
    cnts_df = pd.read_excel('./Data/2020 Special Student Edition (data thu 2016).xlsx',
                            usecols=['World Bank Code', 'Year', 'Riots'])
    cnts_df = cnts_df[1:]
    cnts_df = cnts_df.rename(columns={'World Bank Code': 'country_iso3', 'Year': 'year', 'Riots': 'DOMESTIC_UNREST'})
    cnts_df.loc[:, 'country_iso3'] = cnts_df.loc[:, 'country_iso3'].replace({'SIN': 'SGP', 'ROM': 'ROU', 'SER': 'SRB'})
    cnts_df['year'] = cnts_df['year'].astype(int)
    cnts_df['DOMESTIC_UNREST'] = cnts_df['DOMESTIC_UNREST'].astype(float)

    # demo cnts information
    demo_df: DataFrame = pd.read_pickle(os.path.join('Data', '20201217_worldscope_add_democracy_data.pkl'))
    demo_cnts_df: DataFrame = demo_df.merge(cnts_df, on=['country_iso3', 'year'], how='left')
    demo_cnts_df['DOMESTIC_UNREST_DUMMY'] = (demo_cnts_df['DOMESTIC_UNREST'] > 0).astype(int)

    # construct democracy measure
    demo_cnts_df['DEMOCRACY1'] = ((demo_cnts_df['DEMOC_FREE_HOUSE'] == 1) & (demo_cnts_df['POLITY_IV_SCORE'] > 0))
    demo_cnts_df.loc[demo_cnts_df['POLITY_IV_SCORE'].isnull(), 'DEMOCRACY1'] = np.nan
    demo_cnts_df['DEMOCRACY2'] = ((demo_cnts_df['DEMOC_FREE_HOUSE'] == 1) & (
            (demo_cnts_df['DEMOC_BMR'] == 1) | (demo_cnts_df['DEMOC_CGV'] == 1)))
    demo_cnts_df.loc[(demo_cnts_df['DEMOC_BMR'].isnull()) & (demo_cnts_df['DEMOC_CGV'].isnull()), 'DEMOCRACY2'] = np.nan
    demo_cnts_df.loc[:, 'DEMOCRACY'] = demo_cnts_df['DEMOCRACY1'].fillna(demo_cnts_df['DEMOCRACY2']).fillna(
        demo_cnts_df['DEMOC_FREE_HOUSE'])

    # load ddcg data
    ddcg_df = pd.read_csv('./Data/DDCGdata_final.csv', encoding='latin1',
                          usecols=['wbcode', 'year', 'region', 'dem', 'demreg']).rename(
        columns={'wbcode': 'country_iso3', 'dem': 'DEMOC_DDCG',
                 'demreg': 'DEMOC_REG_DDCG'})
    ddcg_df.loc[:, 'country_iso3'] = ddcg_df['country_iso3'].replace(
        {'SIN': 'SGP', 'UAE': 'ARE', 'SER': 'SRB', 'ROM': 'ROU', 'BRU': 'BRN', 'ZAR': 'DRC',
         'FJI': 'FIJ', 'GRD': 'GRN', 'KNA': 'SKN', 'VCT': 'SVG', 'VUT': 'VAN',
         })
    tmp_ddcg_df = ddcg_df.loc[ddcg_df['country_iso3'] == 'SRB'].replace({'SRB': 'MNE'})
    ddcg_df = ddcg_df.append(tmp_ddcg_df, ignore_index=True)

    # merge ddcg with democracy data
    democracy_df: DataFrame = demo_cnts_df.merge(ddcg_df, on=['country_iso3', 'year'], how='left')
    democracy_df.loc[:, 'region'] = democracy_df.groupby('country_iso3')['region'].ffill()
    democracy_df.loc[:, 'region'] = democracy_df.groupby('country_iso3')['region'].bfill()
    democracy_df2 = democracy_df.copy()
    region_dict = {'MCO': 'ECA', 'LIE': 'ECA', 'DRC': 'AFR', 'DDR': 'ECA', 'SSD': 'AFR'}
    for key in region_dict:
        democracy_df2.loc[democracy_df2['country_iso3'] == key, 'region'] = region_dict[key]

    country_code = ['AND', 'TLS', "KOS", 'MSI', 'FSM', 'PAL', 'YMD', 'SNM', 'SSD', 'TUV', 'VDR', 'SEY', 'MDG', 'SNV',
                    'MAD', 'BRU']
    democracy_df2 = democracy_df2.loc[~democracy_df2['country_iso3'].isin(country_code)]

    region_democ_sum_series = democracy_df2.groupby(['region', 'year'])['DEMOCRACY'].sum().rename(
        'REGION_DEMOC_SUM')
    region_unrest_sum_series = democracy_df2.groupby(['region', 'year'])['DOMESTIC_UNREST_DUMMY'].sum().rename(
        'REGION_UNREST_SUM')
    region_country_num_series = democracy_df2.groupby(['region', 'year'])['country_iso3'].count().rename(
        'REGION_COUNTRY_NUM')
    democracy_df2 = democracy_df2.merge(region_democ_sum_series, how='left', on=['region', 'year']).merge(
        region_unrest_sum_series, how='left', on=['region', 'year']).merge(region_country_num_series, how='left',
                                                                           on=['region', 'year'])

    # Leave out self
    democracy_df2['REGION_DEMOC'] = (democracy_df2['REGION_DEMOC_SUM'] - democracy_df2['DEMOCRACY']) / \
                                    (democracy_df2['REGION_COUNTRY_NUM'] - 1)

    democracy_df2['REGION_UNREST'] = (democracy_df2['REGION_UNREST_SUM'] - democracy_df2['DOMESTIC_UNREST_DUMMY']) / \
                                     (democracy_df2['REGION_COUNTRY_NUM'] - 1)

    # Year of Change
    democracy_df3 = democracy_df2.sort_values(by=['country_iso3', 'year'], ascending=[True, True])
    democracy_df3['DEMOC_CHANGE'] = democracy_df3.groupby('country_iso3')['DEMOCRACY'].diff()
    democracy_df3['DEMOC_CHANGE'] = (
            (democracy_df3['DEMOC_CHANGE'] != 0) & (democracy_df3['DEMOC_CHANGE'].notnull())).astype(int)

    democracy_df4 = democracy_df3.sort_values(by=['country_iso3', 'year'], ascending=[True, True])
    democracy_df4 = democracy_df4.set_index(['country_iso3', 'year'])
    for i in [3, 5, 10]:
        democracy_df4['DEMOC_WINDOW{0}'.format(i)] = 0
        for country_iso3, year in democracy_df4[democracy_df4['DEMOC_CHANGE'] == 1].index.values:
            democracy_df4.loc[(country_iso3, slice(year - i, year + i)), ['DEMOC_WINDOW{0}'.format(i)]] = 1
    democracy_df5 = democracy_df4.reset_index(drop=False)
    democracy_df5.to_pickle(os.path.join('democracy_measure_country_level.pkl'))
    democracy_df5.to_stata(os.path.join('democracy_measure_country_level.dta'), write_index=False)
    country_control_df = pd.read_pickle(
        '/home/zigan/Documents/LIYan/DataMiningVersion2/OLS/Data/ForeignExchange/' + \
        'Innovation/AddCountryControls/country_control.pkl'
    ).rename(columns={'loc': 'country_iso3'})
    democracy_df5_with_ctrls: DataFrame = democracy_df5.merge(country_control_df, on=['country_iso3', 'year'],
                                                              how='left')
    democracy_df5_with_ctrls.to_pickle(os.path.join('democracy_measure_country_level.pkl'))
    democracy_df5_with_ctrls.to_stata(os.path.join('democracy_measure_country_level.dta'), write_index=False)

    # merge with worldscope data
    worldcope_df: DataFrame = pd.read_pickle(
        '/home/zigan/Documents/LIYan/DataBase/Worldscope/worldscope_firm_characteristic.pkl')

    ws_demo_df: DataFrame = worldcope_df.merge(democracy_df5, on=['country_iso3', 'year'])
    ws_demo_df.to_pickle(os.path.join('worldscope_with_democracy_data.pkl'))
