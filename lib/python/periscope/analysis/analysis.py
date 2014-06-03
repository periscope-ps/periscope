import os, sys, time
import orange
import utils
import orngTest, orngStat, orngTree

""" This is a temporary file, it is being used to
test and print the current implemented classifiers.
The way learners and classifiers will be called will be replaced
by dataIO.py file
"""

inputfile = os.getcwd() + "\\data\\jobs.tab"
data = orange.ExampleTable(inputfile)
size = len(data)

# For feature subset selection
#fss = fss.Fss()
#fss.checkAttRelevance(data, 0.0)

learners = ["bayes", "tree"]

ut = utils.Utils()

# Get the percentage of missing values per attribute within a data set
ut.missingvalues(data)


for i in learners:
    print "ANALYZING NEW METHOD..."
    print
    ut = utils.Utils()
    # Number and percentage of misclassification for a given method. If last attribute is true, prints the whole instance info.
    ut.testingclassifier(data, i, size, False)
    # Classifier accuracy from a given method. Possible options so far: "bayes", "tree" , and "knn" 
    ut.accuracy(data, i, size)
    # Proabilities assigned to misclassified instances that are above or below given thresholds. If last attribute is true, prints details.
    ut.prob_misclassification(data, size, i, 0.05, 0.95, False)
    

# Evaluates and suggests a method according to the data
ut.choosingmethod(data)
