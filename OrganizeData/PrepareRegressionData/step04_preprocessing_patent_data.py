#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step04_preprocessing_patent_data
# @Date: 2020/5/22
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m OrganizeData.PrepareRegressionData.step04_preprocessing_patent_data
"""

import os

import numpy as np
import pandas as pd
from pandas import DataFrame

from Constants import Constants as const

if __name__ == '__main__':
    po_innovation_df: DataFrame = pd.read_pickle(
        os.path.join(const.DATA_PATH, 'innovation', '20191016_worldscope_po_innovation_data.pkl')).dropna(
        subset=['pat_prio', 'cite_prio', 'pat_app', 'cite_app'], how='all')
    home_patent_columns = ['pat_app', 'cite_app']
    notall_null = po_innovation_df[home_patent_columns].notnull().max(axis=1) == 1
    po_innovation_df.loc[notall_null, home_patent_columns] = \
        po_innovation_df.loc[notall_null, home_patent_columns].fillna(0).values
    po_innovation_df['patent_home_ln'] = np.log(data_df['pat_app']).replace([np.inf, -np.inf], np.nan)
    data_df['cite_home_ln'] = np.log(data_df['cite_app']).replace([np.inf, -np.inf], np.nan)
    home_patent_columns = ['patent_home_ln', 'cite_home_ln']
    data_df.loc[notall_null, home_patent_columns] = \
        data_df.loc[notall_null, home_patent_columns].fillna(0).values

    data_df['patent_home_ln_1'] = data_df[['gvkey', 'patent_home_ln']].groupby('gvkey').shift(-1).values
    data_df['cite_home_ln_1'] = data_df[['gvkey', 'cite_home_ln']].groupby('gvkey').shift(-1).values