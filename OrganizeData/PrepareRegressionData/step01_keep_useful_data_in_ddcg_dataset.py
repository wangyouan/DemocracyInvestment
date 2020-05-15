#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: step01_keep_useful_data_in_ddcg_dataset
# @Date: 2020/5/15
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

"""
python -m OrganizeData.PrepareRegressionData.step01_keep_useful_data_in_ddcg_dataset
"""

import os

import pandas as pd
from pandas import DataFrame

from Constants import Constants as const

USEFUL_VARS = ['elev', 'distr', 'distcr', 'distc', 'cen_lon', 'lgov', 'lsecenr', 'lmort', 'y', 'loginvpc', 'ltfp',
               'ltrade2', 'lprienr', 'cen_lat', 'demPOL_exrec', 'demPOL_xconst', 'demPOL_parcomp', 'cen_cr', 'cen_c',
               'demPS', 'demPOL', 'demFH', 'year', 'wbcode', 'taxratio', 'rtfpna', 'sov4', 'sov3', 'sov2', 'sov1',
               'secenr', 'unrestreg', 'tradewbreg', 'yreg', 'region_initreg_year', 'regionINITREG', 'regionREG',
               'region60', 'regionDA', 'rtrend6', 'rtrend5', 'rtrend4', 'rtrend3', 'rtrend2', 'rtrend1', 'prienr',
               'PopulationtotalSPPOPTOTL', 'Populationages1564oftota', 'Populationages014oftotal', 'lh_bl', 'ls_bl',
               'lp_bl', 'unrest', 'NAME', 'unrestn', 'LON', 'LAT', 'marketref', 'incomequint50s_year', 'yearrev',
               'yeardem', 'ginv', 'region', 'wbcode2', 'gdp1960', 'GDPpercapitaconstantLCUN',
               'gdppercapitaconstant2000us', 'tradewb', 'revevent', 'demevent', 'demFH_pr', 'demFH_cl', 'demext',
               'InitReg', 'demCGV', 'demBMR', 'dem', 'rever', 'democ', 'country_name', 'country', 'mortnew', 'demreg',
               'demregREGIME', 'demreg60', 'demregDA', 'areakm2', 'pop95', 'totalliabilities', 'totalassets', 'nfa',
               'gfa', 'nfagdp', 'troppop', 'pop100cr', 'pop100km', 'lcr100km', 'lc100km', 'tropicar']

if __name__ == '__main__':
    ddcg_df: DataFrame = pd.read_stata(os.path.join(const.DATA_PATH, 'ddcg', 'DDCGdata_final.dta'))
    ddcg_valid_df: DataFrame = ddcg_df.loc[:, USEFUL_VARS].copy()
    ddcg_valid_df.to_pickle(os.path.join(const.TEMP_PATH, '20200515_country_year_democracy_measure.pkl'))
