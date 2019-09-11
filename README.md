> Usage `python3 getData.py`

#To do list

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