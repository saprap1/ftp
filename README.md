# TO DO LIST
* Add more x variables to improve accuracy (i.e. height and weight, missed games?, injuries?, pre-season rank of defense?, remove players with less than certain points or snaps?, played in last three consecutive games?)
* Maybe increase sliding window to improve accuracy? (maybe window of 5)

<<<<<<< HEAD
# To do list

1. Have spreadsheets all set with data displayed correctly
2. For ML, make 2017 the training data, and 2018 the test data
3. Loop through 2017 spread sheets and make X array be their data, Y array be their fantasy points that week
4. For windows make it 3 games data and the next (4th) game the Y. So as an example, the first three games would be paired with the 4th. The 2nd-4th game would be paired with the 5th exc. 
5. Do steps 3 and 4 but for 2018. These windows are all in put in an array so it's 2D.
6. Now that windows are set and paired off. Need this code steps to evaluate:
```python
    #can do other classifiers but this should be good
    rf = RandomForestClassifier(n_estimators=100)
    
    rf.fit(X_train, Y_train)
    predictions = rf.predict(X_validation) 
    
    y_predict_probabilities = rf.predict_proba(X_validation)[:,1]
    
    fpr, tpr, _ = roc_curve(pred1, y_predict_probabilities)
    aucurve = roc_auc_score(pred1, y_predict_probabilities)
    
    print("Area under curve")
    print(aucurve)
    
    print("True amount in validation ", countVal)
    print("True amount in pred ", countPred)
    
    print("accuracy")
    print(accuracy_score(Y_validation, predictions))
    print(confusion_matrix(Y_validation, predictions))
    print(classification_report(Y_validation, predictions))

```
7. Problem I see arising could be that it is predicting categories instead of how many points. My honors project was categories and this will need to be points so that is something to look into.

# Next Steps
1. Add kicker data into all_players spreadsheet
2. For RB add rush attempts, Y/A, targets, receptions, Y/R
3. For WR and TE add targets, reception, Y/R
4. For QB add Y/A and AY/A

# Future
1. Add defense ranking each week
2. Add espn projected point
3. Run ML and compare our prediction vs espn
=======

* How reliable is this player to be within this score?    
* probability of being above or below a certain score (boom or bust/true or false)
    -- Logistic regression
    -- Confusion matrix
* how good is our prediction within 2 points of the actual (valiating model)
    * ex) I'm 80% certain that this player is going to get within __ points
* how often are our predctions too low/lower?
* our prediction vs espn's prediction and which one is better


* --> future: recording predicted values each week of the players to compare our model vs espn
    
>>>>>>> machine-learning
