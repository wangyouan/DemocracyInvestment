#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step11_construct_pension_cost_information
# @Date: 2020/12/21
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m OrganizeData.PrepareRegressionData.step11_construct_pension_cost_information
"""

import os

import numpy as np
import pandas as pd
from pandas import DataFrame

from Constants import Constants as const

if __name__ == '__main__':
    # Load worldscope data
    ws_pension_df: DataFrame = pd.read_sas(
        os.path.join(const.DATABASE_PATH, 'wrds', 'tfn', 'worldscope', 'wrds_ws_pension.sas7bdat')).rename(
        columns={'year_': const.YEAR, 'ITEM18811': 'PPSC', 'ITEM18813': 'PPIC', 'ITEM18817': 'PPRPA',
                 'ITEM6008': 'isin', 'ITEM18837': 'HPSC', 'ITEM18839': 'HIC', 'ITEM18843': 'HRPA'}).loc[
                               :, [const.YEAR, 'isin', 'PPSC', 'PPIC', 'PPRPA', 'HPSC', 'HIC', 'HRPA']]
    ws_pension_df.loc[:, 'isin'] = ws_pension_df['isin'].str.decode('utf8')

    # Load worldscope company
    ws_company_df: DataFrame = pd.read_csv(
        os.path.join(os.path.join(const.DATABASE_PATH, 'WorldScope', 'worldscope_raw_data.zip')),
        usecols=['year_', 'ITEM6008', 'ITEM7011']).rename(
        columns={'year_': const.YEAR, 'ITEM6008': 'isin', 'ITEM7011': 'EMP'})

    # Merge two database
    pension_emp_df: DataFrame = ws_pension_df.dropna(subset=['isin']).merge(
        ws_company_df, on=['isin', const.YEAR], how='left').dropna(
        subset=['PPSC', 'PPIC', 'PPRPA', 'HPSC', 'HIC', 'HRPA'], how='all')
    for key in ['PPSC', 'PPIC', 'PPRPA', 'HPSC', 'HIC', 'HRPA']:
        pension_emp_df.loc[:, key] = pension_emp_df[key].fillna(0)

    # Construct variables
    pension_emp_df.loc[:, 'PENSION_COST'] = pension_emp_df['PPSC'] + pension_emp_df['PPIC'] - pension_emp_df['PPRPA']
    pension_emp_df.loc[:, 'HEALTHCARE_COST'] = pension_emp_df['HPSC'] + pension_emp_df['HIC'] - pension_emp_df['HRPA']

    pension_emp_df.loc[:, 'PENSION_COST_EMP'] = pension_emp_df['PENSION_COST'] / pension_emp_df['EMP']
    pension_emp_df.loc[:, 'HEALTHCARE_COST_EMP'] = pension_emp_df['HEALTHCARE_COST'] / pension_emp_df['EMP']

    pension_emp_df.loc[:, ['isin', const.YEAR, 'PENSION_COST', 'PENSION_COST_EMP', 'EMP', 'HEALTHCARE_COST',
                           'HEALTHCARE_COST_EMP']].replace([np.inf, -np.inf], np.nan).to_pickle(
        os.path.join(const.TEMP_PATH, '20201221_pension_healthcare_cost.pkl'))
