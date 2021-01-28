#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 20:07:16 2021

@author: JayMessina
https://www.fantasyfootballdatapros.com/blog/ml/1
"""

import pandas as pd
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
from matplotlib import pyplot as plt
import warnings
from sklearn.metrics import mean_squared_error
import math
from sklearn.utils import shuffle
from sklearn.model_selection import ShuffleSplit

def transform_columns(df, new_column_list):
        df = df[['Player','Tm', 'Age', 'G','FantPt'] + new_column_list + ['FL']]
        return df

def main():
    #warnings.filterwarnings('ignore')
    #import our CSV file
    df = pd.read_csv('ff.csv')
    #drop unneccessary columns
    df.drop(['Rk', '2PM', '2PP', 'DKPt', 'FDPt', 'VBD', 'PosRank', 'OvRank', 'PPR', 'Fmb', 'GS'], axis=1, inplace=True)
    #fix name formatting
    df['Player'] = df['Player'].apply(lambda x: x.split('*')[0]).apply(lambda x: x.split('\\')[0])
    
    #rename columns
    df.rename({
        'TD': 'PassingTD',
        'TD.1': 'RushingTD',
        'TD.2': 'ReceivingTD',
        'TD.3': 'TotalTD',
        'Yds': 'PassingYDs',
        'Yds.1': 'RushingYDs',
        'Yds.2': 'ReceivingYDs',
        'Att': 'PassingAtt',
        'Att.1': 'RushingAtt'
    }, axis=1, inplace=True)
    
    #seperate dataframes based off position
    rb_df = df[df['FantPos'] == 'RB']
    qb_df = df[df['FantPos'] == 'QB']
    wr_df = df[df['FantPos'] == 'WR']
    te_df = df[df['FantPos'] == 'TE']
    
    
    
    rushing_columns = ['RushingAtt', 'RushingYDs', 'Y/A', 'RushingTD']
    receiving_columns = ['Tgt', 'Rec', 'ReceivingYDs', 'Y/R', 'ReceivingTD']
    
    
    
    rb_df = transform_columns(rb_df, rushing_columns+receiving_columns)
    
    rb_df['FantasyPoints'] = (rb_df['RushingYDs']*0.1 + rb_df['RushingTD']*6+ rb_df['ReceivingYDs']*0.1 + rb_df ['ReceivingTD']*6 - rb_df['FL']*2)
    rb_df['Total Usage'] = (rb_df['RushingAtt'] + rb_df['Tgt'])
    rb_df = rb_df[rb_df['RushingAtt'] > 20]
    
    
    x = rb_df['Total Usage'].values.reshape(-1, 1)
    y = rb_df['FantasyPoints'].values.reshape(-1, 1)
    
    xName = rb_df['Player'].values.reshape(-1, 1)
    #yName = rb_df['FantasyPoints'].values.reshape(-1, 1)
    
    
    print(rb_df)
    #print(xName)
    
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)
    
    name_train, name_test = train_test_split(xName, test_size=0.2, random_state=0)
    
    #print(name_train)
    #print(name_test)
    
    regressor = LinearRegression()  
    regressor.fit(x_train, y_train) #training the algorithm
    y_pred = regressor.predict(x_test)
    
    
    
    #print(y_pred)
    
    df = pd.DataFrame({'Name': name_test.flatten(),'Actual': y_test.flatten(), 'Predicted': y_pred.flatten()})
    
    print(df)
    
    plt.scatter(x_test, y_test,  color='gray')
    plt.plot(x_test, y_pred, color='red', linewidth=2)
    plt.xlabel('Usage')
    plt.ylabel('Total FantasyPoints')
    plt.show()
    
    #print(y_pred.flatten())
    
    fig, ax = plt.subplots()

    plt.scatter(x_test, y_test,  color='gray')
    plt.plot(x_test, y_pred, color='red', linewidth=2)
    
    #plot the vertical distance between y_test and y_pred
    ax.vlines(x_test, y_test, y_pred)
    
    plt.xlabel('Usage')
    plt.ylabel('Total FantasyPoints')
    plt.show()
    
    mse = mean_squared_error(y_test,y_pred)
    rmse = math.sqrt(mse)
    rmse
    
    #>>26.049902859860676
main()