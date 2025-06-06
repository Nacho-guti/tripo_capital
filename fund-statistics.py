# -*- coding: utf-8 -*-

import os


import pandas as pd
import numpy as np


from typing import List, Mapping, Optional, Union


def _compute_fund_statistics(filepath: Union[str, os.PathLike], rf: float) -> Mapping[str, float]:

    ''' Computes basic fund statistics (Sharpe ratio, mean returns, volatility,
            CAGR ...) and data features (length, timespan, and the like).

        args
        ----

            :param filepath: data pahts (relative or absolute). Since we use
                    [os] any path-like expression should be parsed correctly.

            :param rf: riskfree rate. Introduced as a free variable because it
                    is evaluated separately.

    '''

    data: pd.DataFrame = pd.read_excel(io = filepath)

    data['Date'] = pd.to_datetime(arg = data['Date'], errors = 'coerce', format = '%m/%d/%Y')
    data.set_index(keys = 'Date', drop = True, inplace = True)
    
    data = data[data.index >= '2022-01-01'].sort_index(inplace = True)
    

    print(data.describe())







if __name__ == '__main__':
    CWD: os.PathLike = os.getcwd()
    path: os.PathLike = os.path.join(
        CWD, 'data/raw/bonds/ish_glob_bond_etf.xlsx'
    )

    rf: float = float(.5)

    _compute_fund_statistics(filepath = path, rf = rf)

    print(path)


