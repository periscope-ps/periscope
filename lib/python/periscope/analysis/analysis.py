import os, sys, time
import orange
import utils
import orngTest, orngStat, orngTree

inputfile = os.getcwd() + "\\data\\jobs.tab"
data = orange.ExampleTable(inputfile)
size = len(data)

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
    


#For some unkown reason, this code is not handling OO calls. It breaks usually at the crossvalidation method call (that is a built-in method).
# It is working here though.
def evaluation(data, folds):
    """
    Evaluates Bayes and DT and prints results for 4 different metrics: Correspondence analysis,
    Information score, Brier score and Area under the ROC curve.
    """
    bayes = orange.BayesLearner()
    tree = orngTree.TreeLearner(mForPruning=2)
    bayes.name = "bayes"
    tree.name = "tree"
    learners = [bayes, tree]
    print "Statistical measures per learner (using %d-fold cross-validation):" % (folds)
    results = orngTest.crossValidation(learners, data, folds)
    print "Learner   CA      IS      Brier     AUC"
    for i in range(len(learners)):
        print "%-8s %5.3f  %5.3f  %5.3f  %5.3f" % (learners[i].name, orngStat.CA(results)[i], orngStat.IS(results)[i], orngStat.BrierScore(results)[i], orngStat.AUC(results)[i])
    print "-------"
    print

# Compares bayes and tree providing statistical measures for each
evaluation(data, 10)

# Evaluates and suggests a method according to the data
ut.choosingmethod(data)
