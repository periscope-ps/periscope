#! /usr/bin/python

"""
Driver for online classification
Used for HPCC results
"""

__author__="taghrid"
__date__ ="$Apr 26, 2011 8:48:26 AM$"

import dataIO 
from classifier import OnlineClassify
import Queue

def getGenomeClusters():
    genome_clusters = {}
    genome_clusters[0] = {'total':1, 'success':0.03390805, 'fail':0.9660920,
                    'success_dur':0.002072281, 'fail_dur':0.7692308}
    genome_clusters[1] = {'total':1, 'success':0.35757651, 'fail':0.6424235,
                    'success_dur':0.037403652, 'fail_dur':0.6294321}
    genome_clusters[2] = {'total':1, 'success':0.95975185, 'fail':0.0,
                    'success_dur':0.153680692, 'fail_dur':0.0}
    genome_clusters[3] = {'total':1, 'success':1.0, 'fail':0.0,
                    'success_dur':0.706198252, 'fail_dur':0.0}

    return genome_clusters

def getCybershakeClusters():
    clusters = {}
    clusters[0] = {'total':1, 'success':0.9905501, 'fail':0.0094499,
                    'success_dur':0.14860603, 'fail_dur':0.01244232}
    clusters[1] = {'total':1, 'success':1.0, 'fail':0.0,
                    'success_dur':0.59589427, 'fail_dur':0.0}
    clusters[2] = {'total':1, 'success':1.0, 'fail':0.0,
                    'success_dur':0.07543309, 'fail_dur':0.0}
    clusters[3] = {'total':1, 'success':1.0, 'fail':0.0,
                    'success_dur':0.03580543, 'fail_dur':0.0}
    return clusters
    pass

def getPeriodClusters():
    clusters = {}
    clusters[0] = {'total':1, 'success':0.9970000, 'fail':0.001,
                    'success_dur':0.01592612, 'fail_dur':1}
    clusters[1] = {'total':1, 'success':0.8589117, 'fail':0.0,
                    'success_dur':0.76084238, 'fail_dur':0.0}
    clusters[2] = {'total':1, 'success':0.9216579, 'fail':0.0,
                    'success_dur':0.26495552, 'fail_dur':0.0}
    clusters[3] = {'total':1, 'success':0.9993701, 'fail':0.0,
                    'success_dur':0.00908431, 'fail_dur':0.0}
    return clusters
    pass

def getMontageClusters():
    clusters = {}
    clusters[0] = {'total':1, 'success':0.1201425, 'fail':0.614169767,
                    'success_dur':0.03917555, 'fail_dur':0.018751164}
    clusters[1] = {'total':1, 'success':0.3172049, 'fail':0.447983945,
                    'success_dur':0.32654543, 'fail_dur':0.620550478}
    clusters[2] = {'total':1, 'success':0.9861795, 'fail':0.009852217,
                    'success_dur':0.54322419, 'fail_dur':0.000569152}
    clusters[3] = {'total':1, 'success':0.9675831, 'fail':0.004646857,
                    'success_dur':0.08324226, 'fail_dur':0.003904176}
    return clusters
    pass

def getBroadbandClusters():
    clusters = {}
    clusters[0] = {'total':1, 'success':0.1025639, 'fail':0.8732005,
                'success_dur':0.06009692, 'fail_dur':0.22674223}
    clusters[1] = {'total':1, 'success':0.4294825, 'fail':0.08088081,
                'success_dur':0.11594987, 'fail_dur':0.16130321}
    clusters[2] = {'total':1, 'success':0.9908458, 'fail':0.004299772,
                'success_dur':0.12955751, 'fail_dur':0.09262870}
    clusters[3] = {'total':1, 'success':0.9419032, 'fail':0.00007629511,
                'success_dur':0.51498639, 'fail_dur':0.02956172}

    return clusters
    pass

def getLigoClusters():
    pass

applicationMap = {
    'genome': getGenomeClusters,
    'cybershake': getCybershakeClusters,
    'period': getPeriodClusters,
    'montage': getMontageClusters,
    'broadband': getBroadbandClusters,
    'ligo': getLigoClusters
}

def getClusters(application):
    return applicationMap[application]()




def main():
    """shared variable Heap
    producer is eventReader, fills Heap
    in the future, producer will read from message bus and fills Heap
    consumer is analysis process, reads Heap
    """
    import sys
    #application name; genome, broadband, montage, cybershake, period
    app = sys.argv[1]

    #maximum size for the shared Q
    m = int(sys.argv[2])

    #list of files to process
    filenames = sys.argv[3:]
    print filenames

    clusters = getClusters(app)

    Q = Queue.PriorityQueue(m)
    p={}
    c={}
    n = len(filenames)
    
    for i in xrange(n):
        try:
            f = open(filenames[i])
            f.close()
            p[i] = dataIO.eventProducer(filenames[i], Q)
            p[i].start()
        except:
            break
    src = dataIO.eventQueue(Q)
    src.start()
    
    sink = dataIO.printOutput()
    
    classifier = OnlineClassify(src, sink, clusters)
    classifier.run()

if __name__ == "__main__":
    main()
