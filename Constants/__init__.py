#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Filename: __init__.py
# @Date: 2020/5/12
# @Author: Mark Wang
# @Email: wangyouan@gamil.com

from Constants.path_info import PathInfo


class Constants(PathInfo):
    # common identifier
    YEAR = 'year'
    CUSIP = 'cusip'
    TICKER = 'tic'
    CUSIP8 = 'cusip8'
    CUSIP6 = 'cusip6'
    GVKEY = 'gvkey'
    CIK = 'cik'

    SIC_CODE = 'sic'
    WB_CODE = 'wbcode'
    COUNTRY_NAME = 'country'

    # Democracy measure
    DEM_CGV = 'demCGV'
    DEM_BMR = 'demBMR'
    DEM_ANRR = 'dem'
    DEM_PS = 'demPS'
    DEM_POL = 'demPOL'
    DEM_FH = 'demFH'

    # Country variable
    UNREST = 'unrest'
    GINV_RATIO = 'ginv'  # Gross investment as a share of GDP
    PER_PRI = 'lp_bl'  # Percentage of population with at most primary (Barro-Lee)
    PER_SEC = 'ls_bl'  # Percentage of population with at most secondary (Barro-Lee)
    PER_TER = 'lh_bl'  # Percentage of population with tertiary education (Barro-Lee)
    GDP_LN = 'y'
    TAX_RATIO = 'lgov'
    CHILD_MOTALITY_RATE = 'lmort'

    # regional variable
    REGIONAL_GDP_PC = 'yreg'
    REGIONAL_UNREST = 'unrestreg'
