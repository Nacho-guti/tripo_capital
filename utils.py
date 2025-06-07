# -*- coding: utf-8 -*


import os


import functools
import warnings


from typing import List, Tuple, Union



warnings.simplefilter('always', DeprecationWarning)         # get away from this.

def deprecated(func):
    ''' pythonic deprecation wrapper '''

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
 
        warnings.warn(
                f'{func.__name__} is deprecated. Refer to source.',
                DeprecationWarning,
                stacklevel = 2
            )

        return func(*args, **kwargs)

    return wrapper

    


@deprecated
def _recursive_file_search(path: os.PathLike, condition: str) -> List[os.PathLike]:
    ''' Standard recursive file search to find all files verifying some <condition>. 
        
        There are very obvious limitations of this piece of code beyond the scope of
            this project, I am personally annoyed by it as well.'''

    goodgood: List[os.PathLike] = []

    for root, directories, filenames in os.walk(path):
        for fname in filenames:
            if fname.endswith(condition):
                goodgood.append(os.path.join(path, fname))             

    return goodgood



def _flat_file_search(path: os.PathLike, condition: Union[str, Tuple[str]]) -> List[os.PathLike]:
    ''' Standard shallow file search to find all files verifying some <condition>.
            To all my unix homies, think of terminal wildcard search command
                
                               [[ ls *<condition> ]].

        No less annoying than the previous in terms of its lack of utility
            beyond the scope of this project.

        args
        ----
            :param path: root to search, provided it is given through [os]
                should remain operating system independent.

            :param condition: file extension, typically a string or tuple of
                strings.

    '''

    goodgood: List[os.PathLike] = []

    for fname in os.listdir(path):
        if fname.endswith(condition):
            goodgood.append(os.path.join(path, fname))

    return goodgood







if __name__ == '__main__':

    DIR: os.PathLike = os.path.join(os.getcwd(), 'data', 'raw')
    print(_recursive_file_search(path = DIR, condition = ('xls', 'xlsx')))
    print(_flat_file_search(path = DIR, condition = ('xls', 'xlsx')))

    
    print(len(_recursive_file_search(path = DIR, condition = ('xls', 'xlsx'))))
    print(len(_flat_file_search(path = DIR, condition = ('xls', 'xlsx'))))


    print(os.listdir(DIR))
