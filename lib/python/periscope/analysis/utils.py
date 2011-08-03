import bayes
import tree
import knn
import orange, orngTest, orngStat

class Utils():
    """
    Implements analysis of the data set and comparison of methods such as Naive Bayes, Decision
    trees and K Nearest Neighbors.
    """

    def __init__(self):
        self.b = bayes.Bayes()
        self.t = tree.DecisionTree()
        self.k = knn.Knn()


    def getmethod(self, data, method):
        if method == "bayes":
            return self.b.learner(data)
        elif method == "tree":
            return self.t.learner(data)
        elif method == "knn":
            return self.k.learner(data, k=21)
        else:
            return None
        
    def accuracy(self, data, method, size, detailed=False):
        """
        Provides classification accuracy of the chosen method in testing data.
        """
        classifier = Utils.getmethod(self, data, method)
        if classifier is None:
            print "Unkown method"
            return
        accuracy = 0
        for i in range(1, size):
            c = classifier(data[i])
            if data[i].getclass() == c:
                accuracy += 1
        print "Accuracy for %s: %5.1f%s " % (method, (accuracy * 100)/size, '%')
        print "-------"
        print
        return accuracy
    
    def testingclassifier(self, data, method, size, detailed=False, prnt=True):
        """
        Provides total number of misclassifications from a given method
        If detailed equals true, prints instance's information as well
        """
        classifier = Utils.getmethod(self, data, method)
        if classifier is None:
            print "Unkown method"
            return
        misclass = 0
        for i in range(1, size):
            c = classifier(data[i])
            if data[i].getclass() != c:
                if detailed:
                    print data[i]
                    print "Original class: ", data[i].getclass(), "Instance classified as: ", c
                misclass += 1
        if prnt:
            print "Total number of misclassified instances using method %s: %d " %(method, misclass)
            print "Percentage: ", "%5.1f%s " % ((misclass * 100)/size, '%')
            print "-------"
            print
        return misclass

       
    def missingvalues(self, data):
        """
        Calculates the percentage of missing values per attribute within a data set
        """
        natt = len(data.domain.attributes)
        missing = [0.] * natt
        for i in data:
            for j in range(natt):
                if i[j].isSpecial():
                    missing[j] += 1
        missing = map(lambda x, l=len(data):x/l*100., missing)
        atts = data.domain.attributes
        print "Percentage of missing values per attribute:"
        for i in range(natt):
            print "  %5.1f%s %s" % (missing[i], '%', atts[i].name)
        print "-------"
        print
        
    def prob_misclassification(self, data, size, method, below, above, detailed):
        """
        Prints class assignment probabilities of misclassified instances that are below and above parameterized thresholds.
        Prints probability values if "detailed" is true and only the number and percentage of misclassification for each class, otherwise.
        """
        classifier = Utils.getmethod(self, data, method)
        if classifier is None:
            print "Invalid method '%s' given as parameter" % (method)
            return
        misclass = 0
        print "Existing Classes:", data.domain.classVar.values
        print
        print "Using method %s (calcutating misclassification with probabilities below %5.2f and above %5.2f)" % (method, below, above)
        for i in range(0, len(data.domain.classVar.values)):
            print "Probabilities for", data.domain.classVar.values[i], "..." 
            for j in range(0, size - 1):
                p = classifier(data[j], orange.GetProbabilities)
                if (((data[j].getclass() != data.domain.classVar.values[i]) & (p[i] > above)) or ((data[j].getclass() == data.domain.classVar.values[i]) & (p[i] < below))): 
                    if detailed:
                        print "%d: %5.3f (originally %s)" % (j, p[i], data[j].getclass())
                    misclass += 1
            print "Total number of misclassifications:", misclass
            print "Percentage of misclassified instances: ", "%5.1f%s " % ((misclass * 100)/size, '%')
        print "-------"
        print
        return misclass

    def choosingmethod(self, data):
        """
        Chooses a method based on the least misclassification index. Prints a message if there are results are even. 
        """
        size = len(data)
        bscore = self.testingclassifier(data, "bayes", size, False, False)
        tscore = self.testingclassifier(data, "tree", size, False, False)
        #kscore = self.testingclassifier(data, "knn", size, False, False)
        kscore = 10000000
        if (bscore < tscore) & (bscore < kscore):
            chosen = "bayes"
        elif (tscore < bscore) & (tscore < kscore):
            chosen = "tree"
        elif (kscore < bscore) & (kscore < tscore):
            chosen = "knn"
        else:
            print "More than one method has the lowest number of misclassifications."
        print "Method suggested (has the lowest overall number of misclassifications): %s" % (chosen)
        print "-------"
        print
