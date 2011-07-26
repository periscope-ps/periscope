import orange

class Knn():


    def __init__(self):
        pass

    def learner(self, data, k):
        return orange.kNNLearner(data, k)
