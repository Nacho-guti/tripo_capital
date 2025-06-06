# -*- coding: utf-8 -*-

import collections
import os

import pandas as pd


from typing import List, Mapping, Union, Optional, Iterable


class DataLoader(object):

    ''' Custom general data loader for irregular 
            financial timeseries.

        args
        ----
            
            :param filepath: data path (relative or absolute). Since we use
                [os] any path-like expression should be parsed correctly.

            :param rf: riskfree rate. Introduced as a free variable because it
                is evaluated separately.

        '''

        INTERNAL_BUFFER_SIZE: int = int(50)

        def __init__(self, rf: float):
            
            self.rf = rf
            self.buffer: collections.deque[os.PathLike] = collections.deque(maxlen = self.INTERNAL_BUFFER_SIZE)


        def push_back(self, pack: Union[os.PathLike, Iterable[os.PathLike]) -> None:
            
            ''' Queues filenames to buffer.
                
                args
                ----

                    :param pack: either individual or some iterable (e.g., list)
                        packet of filenames to be processed.
            '''

            if isinstance(pack, collections.abc.Iterable) and len(pack) >= 1:     
                for filename in pack:
                    self.buffer.append(filename)

            else:
                self.buffer.append(pack)


        def kill(self) -> None:

            ''' Kills open processes, frees resources '''
            
            self.buffer.clear()


    def load(self):

        ''' I/O operations leveraging internal buffer logic. 
                
            The idea is that we construct rich enough data structures (i.e., mappings)
            to fully describe each asset, and store them in a buffer.

            Because processing is neither complex nor extensive, we mostly perform
            it here, only to clean up after ourselves later on if needed.
        '''
       
        timeseries: collections.deque[Mapping] = collections.deque(maxlen = self.INTERNAL_BUFFER_SIZE)

        while self.buffer:
            filepath: os.PathLike = self.buffer.popleft()
            data:pd.DataFrame = self.preprocess(filepath)

            timeseries.append(data)

        return timeseries

    def preprocess(self, filepath: os.PathLike) -> pd.DataFrame:
        
        ''' Performs data preprocessing. It mostly involves index manipulations 
                for convenience, since the main intent is to load data only. '''

        data: pd.DataFrame = pd.read_excel(io = filepath, index_col = 0, parse_dates = True)
        data = data[data.index >= data.index.max() - pd.DateOffset(years = 3)]
        data.sort_index(inplace = True)

        return data













