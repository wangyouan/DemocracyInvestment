#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step03_merge_innovation_data
# @Date: 2020/5/21
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m OrganizeData.PrepareRegressionData.step03_merge_innovation_data
"""

import os

import pandas as pd
from pandas import DataFrame

from Constants import Constants as const

if __name__ == '__main__':
    ddcg_df: DataFrame = pd.read_pickle(os.path.join(const.TEMP_PATH, '20200515_democracy_with_ctrl.pkl'))
    po_innovation_df: DataFrame = pd.read_pickle(
        os.path.join(const.DATA_PATH, 'innovation', '20191016_worldscope_po_innovation_data.pkl'))
    us_citation_df: DataFrame = pd.read_pickle(os.path.join(const.DATA_PATH, 'innovation', 'us_citation.pkl'))
    us_patent_df: DataFrame = pd.read_pickle(os.path.join(const.DATA_PATH, 'innovation', 'us_patent.pkl'))
    ctat_global_df: DataFrame = pd.read_csv(
        os.path.join(const.DATABASE_PATH, 'Compustat', '198706_202003_global_compustat_all_firms.zip'),
        dtype={'gvkey': str}, usecols=[const.GVKEY, 'fyear', 'isin']).rename(
        columns={'fyear': const.YEAR}).drop_duplicates(subset=[const.GVKEY, const.YEAR], keep='last')
    ddcg_df_isin: DataFrame = ddcg_df.merge(ctat_global_df, on=[const.GVKEY, const.YEAR], how='left')
    ddcg_df_patent: DataFrame = ddcg_df_isin.merge(us_patent_df, on=[const.GVKEY, const.YEAR], how='left')
    ddcg_df_patent_1: DataFrame = ddcg_df_patent.merge(us_patent_df, on=[const.GVKEY, const.YEAR], how='left',
                                                       suffixes=['', '_1'])
    
