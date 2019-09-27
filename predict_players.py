# -*- coding: utf-8 -*-

'''
Some resources:
    https://towardsdatascience.com/a-beginners-guide-to-linear-regression-in-python-with-scikit-learn-83a8f7ae2b4f

train = 2017 data
test = 2018 data

# don't do 2017 as training and 2018 as testing because if there's a slight difference, could overtrain on this one thing
# Maybe stick with 70% 30% (pretty standard) in each directory

'''

import openpyxl
import os
import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt
import random

def collect_data():
    # for each player, call the helper function here
    pass
    

# go through each of the files in that specific year, return X data and Y data
def collect_data_helper(year, position):
    # define the sliding windowp
    window = [0, 1, 2, 3]
    
    X_return = []       # X values to get returned
    X_collect = []      # Collect several games into one list
    Y = []              # Fantasy points
    isCollecting = True
    
    # testing on Tom Brady :|
    file = "2017_data/Tom_Brady_QB_2017.xlsx"
    data = pd.read_excel(file, index_col=0)
    games = data.values
    num_games = len(games)
    
    while isCollecting:
        X_collect = []
        for i in window:
            one_game = list(games[i])
            # end of windowv (fantasy points) goes to Y
            if (i == window[-1]):
                fp = one_game[-1]
                Y.append(fp)
            else:                
                stats = one_game[:(len(one_game)-1)]
                # extend X_collect
                X_collect += stats
        
        # add the results from this window to the final X
        X_return.append(X_collect)
       # print(X_return)
        #print(Y)
        
        # Move window up by 1
        for i in range(0,len(window)):
            window[i] += 1
            
        # No more games to check, exit loop
        if window[-1] == num_games:
            isCollecting = False
        
    return X_return, Y
    

if __name__ == "__main__":
    file = "2017_data/Tom_Brady_QB_2017.xlsx"
    data = pd.read_excel(file, index_col=0)
    
    X_qb, Y_qb = collect_data_helper(2018, "QB")
    
    # sanity check (X and Y should be the same length)
    assert(len(X_qb) == len(Y_qb))
    print(len(X_qb), len(Y_qb))
    for i in range(0, len(X_qb)):
        print("X", X_qb[i], "\nY", Y_qb[i])
    
    '''
    data.plot(x='pass_yds', y='fantasy points', style='o')
    plt.show()
    '''
    
    # list of all the data values (no column names), EXCLUDING fantasy points
    #X = data.drop(columns=["fantasy points"]).values
    
    
    
    