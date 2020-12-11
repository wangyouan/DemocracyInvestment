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

    SCODE2ISO_DICT = recode_dict = {'ALG': 'DZA', 'ANG': 'AGO', 'AUL': 'AUS', 'AUS': 'AUT', 'BAH': 'BHR', 'BFO': 'BFA',
                                    'BHU': 'BTN', 'BNG': 'BGD', 'BOS': 'BIH', 'BOT': 'BWA', 'BUI': 'BDI', 'BUL': 'BGR',
                                    'CAM': 'KHM', 'CAO': 'CMR', 'CAP': 'CPV', 'CEN': 'CAF', 'CHA': 'TCD', 'CON': 'COG',
                                    'COS': 'CRI', 'CRO': 'HRV', 'CZR': 'CZE', 'DEN': 'DNK', 'DRV': 'VNM',
                                    'EQG': 'GNQ', 'ETI': 'ETH', 'ETM': 'TLS', 'FRN': 'FRA', 'GAM': 'GMB', 'GDR': 'DDR',
                                    'GFR': 'DEU', 'GMY': 'DEU', 'GRG': 'GEO', 'GUA': 'GTM', 'GUI': 'GIN',
                                    'HAI': 'HTI', 'HON': 'HND', 'INS': 'IDN', 'IRE': 'IRL', 'IVO': 'CIV', 'KUW': 'KWT',
                                    'KYR': 'KGZ', 'KZK': 'KAZ', 'LAT': 'LVA', 'LEB': 'LBN', 'LES': 'LSO',
                                    'LIB': 'LBY', 'LIT': 'LTU', 'MAA': 'MRT', 'MAC': 'MKD', 'MAG': 'MDG', 'MAL': 'MYS',
                                    'MAS': 'MUS', 'MAW': 'MWI', 'MLD': 'MDA', 'MON': 'MNG', 'MOR': 'MAR',
                                    'MYA': 'MMR', 'MZM': 'MOZ', 'NEP': 'NPL', 'NEW': 'NZL', 'NIG': 'NGA', 'NIR': 'NER',
                                    'NTH': 'NLD', 'OMA': 'OMN', 'PAR': 'PRY', 'PHI': 'PHL', 'POR': 'PRT',
                                    'ROK': 'KOR', 'RUM': 'ROU', 'RVN': 'VDR', 'SAF': 'ZAF', 'SAL': 'SLV', 'SER': 'SRB',
                                    'SIE': 'SLE', 'SIN': 'SGP', 'SLO': 'SVK', 'SOL': 'SLB', 'SPN': 'ESP',
                                    'SRI': 'LKA', 'SUD': 'SDN', 'SWA': 'SWZ', 'SWD': 'SWE', 'TAJ': 'TJK', 'TAW': 'TWN',
                                    'TAZ': 'TZA', 'THI': 'THA', 'TOG': 'TGO', 'TRI': 'TTO', 'UAE': 'ARE',
                                    'UKG': 'GBR', 'URU': 'URY', 'USR': 'SUN', 'VIE': 'VNM', 'YAR': 'YEM', 'YGS': 'SCG',
                                    'YPR': 'YMD', 'YUG': 'SRB', 'ZAI': 'COD', 'ZAM': 'ZMB', 'ZIM': 'ZWE', }
