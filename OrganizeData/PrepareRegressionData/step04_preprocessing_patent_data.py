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

    po_innovation_df['patent_home_ln'] = np.log(po_innovation_df['pat_app']).replace([np.inf, -np.inf], np.nan)
    po_innovation_df['cite_home_ln'] = np.log(po_innovation_df['cite_app']).replace([np.inf, -np.inf], np.nan)
    home_patent_columns = ['patent_home_ln', 'cite_home_ln']
    po_innovation_df.loc[notall_null, home_patent_columns] = \
        po_innovation_df.loc[notall_null, home_patent_columns].fillna(0).values

    po_innovation_df2 = pd.read_pickle(os.path.join(const.DATA_PATH, 'innovation', 'po_innovation_data.pkl'))
    po_innovation_df2 = po_innovation_df2.loc[:, ['gvkey', 'year', 'isin', 'gen1sum_isin_app', 'ori1sum_isin_app',
                                                  'bt_explore_60rate_appyr', 'bt_exploit_60rate_appyr']].copy()
    data_df: DataFrame = po_innovation_df.merge(po_innovation_df2, how='outer', on=['isin', 'year']).rename(
        columns={'bt_explore_60rate_appyr': 'explore_rate', 'bt_exploit_60rate_appyr': 'exploit_rate',
                 'gen1sum_isin_app': 'generality', 'ori1sum_isin_app': 'originality'})

    # Append US citation information
    us_citation_df: DataFrame = pd.read_pickle(os.path.join(const.DATA_PATH, 'innovation', 'us_citation.pkl')).rename(
        columns={'patnum': 'patent_us'})
    data_df2: DataFrame = data_df.merge(us_citation_df, how='left', on=['gvkey', 'year'])
    data_df2.loc[:, 'patent_us_ln'] = np.log(data_df2['patent_us']).replace([np.inf, -np.inf], np.nan)
    data_df2.loc[:, 'cite_us_ln'] = np.log(data_df2['cite_all']).replace([np.inf, -np.inf], np.nan)

    us_innovation_columns = ['patent_us_ln', 'cite_us_ln']
    notall_null = data_df2[us_innovation_columns].notnull().max(axis=1) == 1
    data_df2.loc[notall_null, us_innovation_columns] = \
        data_df2.loc[notall_null, us_innovation_columns].fillna(0).values
    data_df2.loc[:, const.GVKEY] = data_df2.groupby('isin')[const.GVKEY].bfill()
    data_df2.loc[:, const.GVKEY] = data_df2.groupby('isin')[const.GVKEY].ffill()
    data_df3: DataFrame = data_df2.dropna(subset=['gvkey'])

    # append rd expense variables
    ctat_df: DataFrame = pd.read_csv(
        os.path.join(const.DATABASE_PATH, 'Compustat', '198706_202003_global_compustat_all_fina_data.zip'),
        usecols=['xrd', 'at', 'gvkey', 'fyear'], dtype={'gvkey': str}
    ).rename(columns={'fyear': const.YEAR}).sort_values(const.YEAR, ascending=True).drop_duplicates(
        subset=[const.GVKEY, const.YEAR], keep='last')
    ctat_df.loc[:, 'R_D_LN'] = ctat_df['xrd'].apply(np.log).replace([np.inf, -np.inf], np.nan).fillna(0)
    ctat_df.loc[:, 'lag_at'] = ctat_df.groupby('gvkey')['at'].shift(1)
    ctat_df.loc[:, 'R_D_RATIO'] = (ctat_df['xrd'] / ctat_df['lag_at']).replace([np.inf, -np.inf], np.nan).fillna(0)

    data_df4: DataFrame = data_df3.merge(ctat_df.loc[:, [const.GVKEY, const.YEAR, 'R_D_LN', 'lag_at', 'R_D_RATIO']],
                                         on=[const.GVKEY, const.YEAR], how='outer')
    data_df4.to_pickle(os.path.join(const.TEMP_PATH, '20200525_innovation_related_variables.pkl'))
