#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step08_construct_worldscope_data_coverage
# @Date: 2020/12/10
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
works on Li Yan's server

http://147.8.118.96:8888/notebooks/DataBase/Worldscope/check_worldscope_data.ipynb
"""

import pandas as pd
from pandas import DataFrame

if __name__ == '__main__':

    # get worldscope country coverage
    ws_df: DataFrame = pd.read_pickle('worldscope_firm_characteristic.pkl')
    ws_df.head()
    ws_df.loc[:, 'country_name'] = ws_df['country_name'].replace({"ENGLAND": 'UNITED KINGDOM'})
    country_df: DataFrame = ws_df.loc[:, ['year', 'country_name']].drop_duplicates()
    country_group = country_df.groupby(['country_name'])
    start_year = country_group['year'].min()
    start_year.name = 'start_year'
    end_year = country_group['year'].max()
    end_year.name = 'end_year'
    country_coverage: DataFrame = DataFrame([start_year, end_year]).T.reset_index(drop=False)

    # load constry iso3 data
    country_iso3_columns = {
        'name': 'country_name', 'alpha-2': 'country_iso2', 'alpha-3': 'country_iso3', 'country-code': 'country_code',
        'sub-region': 'sub_region'
    }

    country_iso3_df = pd.read_csv(
        '/home/zigan/Documents/LIYan/Project/ForeignExchange/Data/CurrencyRate/iso_country_region_code.csv',
        usecols=country_iso3_columns.keys(), dtype={'name': str, 'alpha-2': str, 'alpha-3': str, 'country-code': str}
    ).rename(columns=country_iso3_columns)
    country_iso3_df.loc[:, 'country_name'] = country_iso3_df['country_name'].str.upper().replace(
        {'ANTIGUA AND BARBUDA': 'ANTIGUA & BARBUDA', 'BOLIVIA (PLURINATIONAL STATE OF)': 'BOLIVIA',
         'BOSNIA AND HERZEGOVINA': 'BOSNIA & HERZEGOVINA', 'CZECHIA': 'CZECH REPUBLIC',
         'UNITED STATES OF AMERICA': 'UNITED STATES',
         'VENEZUELA (BOLIVARIAN REPUBLIC OF)': 'VENEZUELA', 'VIET NAM': 'VIETNAM',
         'KOREA, REPUBLIC OF': 'KOREA (SOUTH)',
         'PALESTINE, STATE OF': 'PALESTINE', 'SYRIAN ARAB REPUBLIC': 'SYRIA', 'TAIWAN, PROVINCE OF CHINA': 'TAIWAN',
         'TANZANIA, UNITED REPUBLIC OF': 'TANZANIA', 'TURKS AND CAICOS ISLANDS': 'TURKS & CAICOS ISLANDS',
         'TTRINIDAD AND TOBAGO': 'TRINIDAD & TOBAGO', 'NORTH MACEDONIA': 'MACEDONIA'
         })
    country_iso3_df.loc[54, 'country_name'] = "COTE D'IVOIRE"
    country_iso3_df.loc[57, 'country_name'] = "CURACAO"

    country_iso3_df.loc[234, 'country_name'] = "UNITED KINGDOM"

    country_coverage2: DataFrame = country_coverage.merge(country_iso3_df, on=['country_name'], how='inner')
    country_coverage2.to_pickle('worldscope_data_country_coverage.pkl')
