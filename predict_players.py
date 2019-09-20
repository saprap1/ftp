# -*- coding: utf-8 -*-

'''
Some resources:
    https://towardsdatascience.com/a-beginners-guide-to-linear-regression-in-python-with-scikit-learn-83a8f7ae2b4f

train = 2017 data
test = 2018 data

'''

import openpyxl
import os
import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt
import random

# go through each of the files in that specific year, return X data and Y data
def collect_data(year, position):
    # start and end define our windows
    start = 0
    end = 0
    
    # here, get all the players in the data folder, and check the position (need to keep all the X data separate)
    file = "2017_data/Tom_Brady_QB_2017.xlsx"
    
    data = pd.read_excel(file, index_col=0)
    
    X_return = []
    X_collect = []
    
    # for each file (player) -- gotta fix this
    for i in range(0,1):
        # for each row, get all the values
        for game in data.drop(columns="fantasy points").values:
            game = list(game)
            # extend the current list
            X_collect += game
            # once we get data from 3 games into one row, add the data to the overall list
            if end - start == 2:
                start = (end+1)
                X_return.append(X_collect)
                # reset the row
                X_collect = []
            end += 1
    return X_return
    

if __name__ == "__main__":
    file = "2017_data/Tom_Brady_QB_2017.xlsx"
    data = pd.read_excel(file, index_col=0)
    
    X_qb = collect_data(2018, "QB")
    '''
    data.plot(x='pass_yds', y='fantasy points', style='o')
    plt.show()
    '''
    
    # list of all the data values (no column names), EXCLUDING fantasy points
    #X = data.drop(columns=["fantasy points"]).values
    
    
    
    