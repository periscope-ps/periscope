import orange, orngTree

class DecisionTree():


    def __init__(self):
        pass

    def learner(self, data):
        return orngTree.TreeLearner(data, sameMajorityPruning=1, mForPruning=2)
       
    def print_tree(self, data, visual):
        """
        Decision Tree from the data set
        """
        tree = learner(data)
        orngTree.printTxt(tree)
        if visual: # visual equals true allows plotting a visual tree. A .dot file is written into the current directory.
            orngTree.printDot(tree, fileName='tree.dot', internalNodeShape="ellipse", leafShape="box")

