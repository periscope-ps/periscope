import orngFSS

class Fss():

    """
    Class responsible for feature subset selection.
    """
    def __init__(self):
        pass

    def filtering(self, data, margin=0.0):
        """
        Returns selected subset. 
        """
        fdata = orngFSS.FilterRelief(margin=margin)
        newdata = fdata(data)
        return newdata

    def checkAttRelevance(self, data, margin):
        print "Before feature subset selection (%d attributes):" % len(data.domain.attributes)
        old = orngFSS.attMeasure(data)
        for i in old:
            print "%5.3f %s" % (i[1], i[0])
        print "\nRelevance of best attributes"
        new = orngFSS.attMeasure(Fss.filtering(self, data, margin))
        for j in new:
            print "%5.3f %s" % (j[1], j[0])
