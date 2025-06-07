# -*- coding: utf-8 -*-

import os
import collections


import utils
from loader import *


if __name__ == '__main__':
    PATH: os.PathLike = os.getcwd() + '/data/raw'

    targets: List[str] = [
            'alternatives',
            'bonds',
            'cash',
            'equities'
        ]

    filepaths: List[os.PathLike] = utils._flat_file_search(
            path = PATH, condition = ('xls', 'xlsx')
        )
    print((filepaths))


    loader = DataLoader()
    loader.push_back(pack = filepaths)

    timeseries: collections.deque[pd.DataFrame] = loader.load()


    for ts in timeseries:
        print(ts.describe())
   
