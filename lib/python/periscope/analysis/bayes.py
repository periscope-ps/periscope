import orange, orngBayes

class Bayes():


    def __init__(self):
        pass

    def learner(self, data):
        return orange.BayesLearner(data)

    def print_model(self, data):
        """
        # Bayes model from the data set
        """
        orngBayes.printModel(learner(data))
