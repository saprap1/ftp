# TO DO LIST
* try different models?
* decide on best model
* return the top 10 names
* cron job/VM to run automatically
* clean data because it is a mess lol
* possible a twitter bot?


So far:
WITHOUT STANDARDSCALAR()
* Linear Regression() for WR gives 0.75 accuracy
* Ridge (solver='sag') for WR gives 0.73 accuracy
* Ridge () for WR gives 0.73 accuracy
* Ridge (solver='svd') for WR gives 0.73 accuracy

* Ridge (solver='sag') for QB gives 0.49 accuracy
* Ridge () for QB gives 0.46 accuracy
* Ridge (solver='svd') for QB gives 0.46 accuracy
* Linear Regression() for QB gives 0.45 accuracy

* Ridge (solver='sag') for RB gives 0.73 accuracy
* Linear Regression() for RB gives 0.72 accuracy
* Ridge (solver='svd') for RB gives 0.72 accuracy 
* Ridge () for RB gives 0.72 accuracy

* Linear Regression() for TE gives 0.89 accuracy
* Ridge (solver='sag') for TE gives 0.88 accuracy
* Ridge (solver='svd') for TE gives 0.88 accuracy
* Ridge () for TE gives 0.87 accuracy


WITH STANDARDSCALAR():
* Linear Regression() for WR gives 0.75 accuracy
* Linear Regression() for QB gives 0.40 accuracy
* Linear Regression() for RB gives 0.72 accuracy
* Linear Regression() for TE gives 0.89 accuracy

* Add more x variables to improve accuracy (i.e. height and weight, missed games?, injuries?, pre-season rank of defense?, remove players with less than certain points or snaps?, played in last three consecutive games?)
* Maybe increase sliding window to improve accuracy? (maybe window of 5)


* How reliable is this player to be within this score?    
* probability of being above or below a certain score (boom or bust/true or false)
    -- Logistic regression
    -- Confusion matrix
* how good is our prediction within 2 points of the actual (valiating model)
    * ex) I'm 80% certain that this player is going to get within __ points
* how often are our predctions too low/lower?
* our prediction vs espn's prediction and which one is better


* --> future: recording predicted values each week of the players to compare our model vs espn
    
