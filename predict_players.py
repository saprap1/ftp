# -*- coding: utf-8 -*-

'''
Some resources:
    https://towardsdatascience.com/a-beginners-guide-to-linear-regression-in-python-with-scikit-learn-83a8f7ae2b4f
    This link to do calculations: https://www.dataquest.io/blog/machine-learning-tutorial/
'''

import openpyxl as op
import os
import pandas as pd
import random
import numpy as np
import matplotlib.pyplot as plt
import random
import sys

from sklearn import model_selection
from sklearn.metrics import roc_auc_score, auc, roc_curve
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.linear_model import SGDRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

# go through each of the files in that specific year, return X data and Y data
# use a sliding window so that a few games will correspond to the following fantasy score
def collect_data(files):
    
    X_return = []       # X values to get returned
    X_collect = []      # Collect several games into one list
    Y = []              # Fantasy points
    
    for file in files:
        # define the sliding window
        # I've tried a window of [0,1,2,3] and [0,1,2,3,4]
        # first option does better (lowers error but raises variance) for TE
        # second does better for QB and WR
        # RB stays the same
        window = [0, 1, 2, 3]

        # get data from workbook
        wb = op.load_workbook(file)
        ws = wb['Sheet1']
        data = pd.DataFrame(ws.values)
        games = data.values[1:]
        num_games = len(games)
        
        # gather all the data from this one file into X_return and Y
        while True:
            X_collect = []
            
            # No more games to check, exit loop
            if window[-1] >= num_games:
                break
            
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

            # Move window up by 1
            for i in range(0,len(window)):
                window[i] += 1

    return X_return, Y

'''
Takes in the year that we are going to look into and the lists for the filenames
by position. We take in the lists so we can add to them and return them instead
of making copies/trying to append sets of lists together/etc.
'''
def organize_players(year, qb_files, wr_files, rb_files, te_files, k_files):
    directory_str = year + "_data/"
    directory = os.fsencode(directory_str)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        # organize the files in the directory by the position that they're in
        if "_QB_" in filename:
            qb_files.append(directory_str + filename)
        elif "_RB_" in filename:
            rb_files.append(directory_str + filename)
        elif "_WR_" in filename:
            wr_files.append(directory_str + filename)
        elif "_TE_" in filename:
            te_files.append(directory_str + filename)
        elif "_K_" in filename:
            k_files.append(directory_str + filename)
            
    return qb_files, wr_files, rb_files, te_files, k_files

def split_data(files, training, testing):
    # for each player, call the helper function here
    train = (len(files)*7)//10   # get 70 percent of players
    # add the training set
    training += files[:train]
    # add the testing set
    testing += files[train:]
    return training, testing

if __name__ == "__main__":
    
    print("Running program... Retrieving files...")

    # need to initialize these because they are added to in the functions
    qb_files = []
    wr_files = []
    rb_files = []
    te_files = []
    k_files = []
    
    qb_train = []
    qb_test = []
    wr_train = []
    wr_test = []
    rb_train = []
    rb_test = []
    te_train = []
    te_test = []
    k_train = []
    k_test = []
    
    # get all the 2017 files
    qb_files, wr_files, rb_files, te_files, k_files = organize_players("2017", qb_files, wr_files, rb_files, te_files, k_files)
    qb_train, qb_test = split_data(qb_files, qb_train, qb_test)
    wr_train, wr_test = split_data(wr_files, wr_train, wr_test)
    rb_train, rb_test = split_data(rb_files, rb_train, rb_test)
    te_train, te_test = split_data(te_files, te_train, te_test)
    k_train, k_test = split_data(k_files, k_train, k_test)
    
    # get all the 2018 files
    qb_files, wr_files, rb_files, te_files, k_files = organize_players("2018", qb_files, wr_files, rb_files, te_files, k_files)
    qb_train, qb_test = split_data(qb_files, qb_train, qb_test)
    wr_train, wr_test = split_data(wr_files, wr_train, wr_test)
    rb_train, rb_test = split_data(rb_files, rb_train, rb_test)
    te_train, te_test = split_data(te_files, te_train, te_test)
    k_train, k_test = split_data(k_files, k_train, k_test)

    print("Done splitting files.")
    
    #print(qb_files)
    #print(wr_files)
    #print(rb_files)
    #print(te_files)
    
    # 70% of data goes to X_train and Y_train
    # 30% of data goes to X_test and Y_test
    #print(len(qb_train), qb_train)
    #print(len(qb_test), qb_test)
    print("Collecting data for each position...")
    qb_X_train, qb_Y_train = collect_data(qb_train)
    qb_X_test, qb_Y_test = collect_data(qb_test)
    wr_X_train, wr_Y_train = collect_data(wr_train)
    wr_X_test, wr_Y_test = collect_data(wr_test)
    rb_X_train, rb_Y_train = collect_data(rb_train)
    rb_X_test, rb_Y_test = collect_data(rb_test)
    te_X_train, te_Y_train = collect_data(te_train)
    te_X_test, te_Y_test = collect_data(te_test)
    k_X_train, k_Y_train = collect_data(k_train)
    k_X_test, k_Y_test = collect_data(k_test)
    
    print("Done splitting data for each position.")

    # Sanity check to make sure all the training sets are the same length and all the testing sets are the same length!
    '''
    print("QB Train", len(qb_X_train), len(qb_Y_train), "QB Test", len(qb_X_test), len(qb_Y_test))
    print("WR Train", len(wr_X_train), len(wr_Y_train), "WR Test", len(wr_X_test), len(wr_Y_test))
    print("RB Train", len(rb_X_train), len(rb_Y_train), "RB Test", len(rb_X_test), len(rb_Y_test))
    print("TE Train", len(te_X_train), len(te_Y_train), "TE Test", len(te_X_test), len(te_Y_test))
    print("K Train", len(k_X_train), len(k_Y_train), "K Test", len(k_X_test), len(k_Y_test))
    '''
    #sys.exit(0)
    #print(len(qb_X_test), qb_X_test)
    #print(len(qb_Y_train), qb_Y_train)
    #print(len(qb_Y_test), qb_Y_test)
    
    while True:
        response = input("Which model would you like to build? <linear_regression, random_forest, sgd> <QB, WR, RB, TE, K> \nType quit to cancel.\n> ")
        
        if response == 'quit':
            break
        else:
            response = response.split(" ")
            model_type = response[0]
            pos = response[1]
            x_train, y_train, x_test, y_test = [], [], [], []
            if pos.lower() == 'qb':
                x_train = qb_X_train
                y_train = qb_Y_train
                x_test = qb_X_test
                y_test = qb_Y_test
            elif pos.lower() == 'wr':
                x_train = wr_X_train
                y_train = wr_Y_train
                x_test = wr_X_test
                y_test = wr_Y_test
            elif pos.lower() == 'rb':
                x_train = rb_X_train
                y_train = rb_Y_train
                x_test = rb_X_test
                y_test = rb_Y_test
            elif pos.lower() == 'te':
                x_train = te_X_train
                y_train = te_Y_train
                x_test = te_X_test
                y_test = te_Y_test
            elif pos.lower() == 'k':
                x_train = k_X_train
                y_train = k_Y_train
                x_test = k_X_test
                y_test = k_Y_test
            else:
                print("Position does not exist.")
                continue
            
            if model_type == "linear_regression":
                print("-------------------Linear Regression Model for {}-------------------".format(pos.upper()))
                model = linear_model.LinearRegression()
                model.fit(x_train, y_train)
                y_pred = model.predict(x_test)
                # The mean squared error
                print("\tMean squared error: %.2f"
                    % mean_squared_error(y_test, y_pred))
                # Explained variance score: 1 is perfect prediction
                print('\tVariance score: %.2f' % r2_score(y_test, y_pred))
                plt.scatter(y_test, y_pred)
                plt.title("{} Model Results".format(pos.upper()))
                plt.xlabel("Actual scores")
                plt.ylabel("Predicted scores")
                plt.show()
            elif model_type == "random_forest":
                print("-------------------Random Forest Model for {}-------------------".format(pos.upper()))
                # rf = RandomForestClassifier(n_estimators=100)
                # rf.fit(x_train, y_train)
                # y_pred = rf.predict(x_test)
                # print(accuracy_score(y_test, y_pred))
                # print(classification_report(y_test, y_pred))
            elif model_type == "sgd":
                print("-------------------SGD Regressor Model for {}-------------------".format(pos.upper()))
                # default ordinary least squares loss with l2 regularization
                # start with 100 epochs
                # can also try learning_rate='optimal'
                #sgd_model = SGDRegressor(max_iter=100, learning_rate='adaptive')
                sgd_model = SGDRegressor()
                
                # use a pipeline to keep track of transforms; be sure to scale data
                #pl = make_pipeline(StandardScaler(), sgd_model)
                #pl.fit(x_train, y_train)
                sgd_model.fit(x_train, y_train)
                print(sgd_model.score(x_test, y_test))



'''   
        arrClass = []
        for i in range (0, len(qb_Y_pred)):
            if (abs(qb_Y_pred[i]-qb_Y_test[i])<=5):
                arrClass.append("T")
            else:
                arrClass.append("F")
                
                
        #splitNum = len(arrClass//2)
        
        xTrain = qb_X_test[:200]
        xTest = qb_X_test[200:]
        
        yTrain = arrClass[:200]
        yTest = arrClass[200:]
        
        qb_model2 = RandomForestClassifier(n_estimators=100)
        qb_model2.fit(xTrain, yTrain)
        qb_Y_pred2 = qb_model2.predict(xTest)

        
        
        #rf = RandomForestClassifier(n_estimators=100)
        qb_model2 = RandomForestClassifier(n_estimators=100)
        qb_model2.fit(qb_X_test, arrClass)
        qb_Y_pred2 = qb_model2.predict(qb_X_test)
        print(qb_Y_pred2)
        

        print(accuracy_score(yTest, qb_Y_pred2))
        #print(confusion_matrix(yTest, qb_Y_pred2))
        print(classification_report(yTest, qb_Y_pred2))
'''
    # Add more x variables to improve accuracy (i.e. height and weight, missed games?, injuries?)
    # Maybe increase sliding window to improve accuracy? (maybe window of 5)
    # 
    #
    # How reliable is this player to be within this score?    
    #   probability of being above or below a certain score (boom or bust/true or false)
    #       -- Logistic regression
    #       -- Confusion matrix
    #   how good is our prediction within 2 points of the actual (valiating model)
    #   ex) I'm 80% certain that this player is going to get within __ points
    # how often are our predctions too low/lower?
    # our prediction vs espn's prediction and which one is better
    # --> future: recording predicted values each week of the players to compare our model vs espn
    #
    