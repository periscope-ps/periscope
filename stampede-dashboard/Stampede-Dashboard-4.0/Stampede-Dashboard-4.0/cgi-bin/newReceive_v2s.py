#!/usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.
from __future__ import division

import sys
from sys import argv
import time

import Queue
import calendar
from lineIO import JsonOutput
from lineIO import LineProducer
import pika
from sqlalchemy import BigInteger
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import create_engine
from sqlalchemy.types import Float
import threading

from time import gmtime, strftime

class Recieve(threading.Thread):
    """
    Reciever Class:

        Attributes:
            max_size: maximum priority queue (Q) size.
            json_name: Filename for the .json output.
            QName: Queue that this receiver will listen to.
            host: hostname of the server. By default it is the 'localhost'.
            connection: Necessary during opening a connection to the server via pika.
            channel: Necessary during opening a connection to the server via pika.
    """


    def __init__ (self,host='localhost', max_size=200000000, json_name='Output.json', exchangeName = 'eventRoute', bindKey = 'stampede.job_inst.#'):

        """
        A constructor for our Receiver class responsible for:
        1) Setting maximum queue size at receiving end during parsing.
        2) Setting up JSON output file.
        3) Setting up connections with the server, creation of queues and exchange.
        4) Setting up the database table titled "JSON" to store needed statistics.

        Arguments:
            host: The hostname.
            maxSize: Maximum size of the priority queue that we use in parsing.
            json_name: Name of JSON file we'll output to.
            exchangeName: The desired name for the exchange.
        """
        threading.Thread.__init__(self)

        self.init_map =  { 'stampede.job_inst.#' : self.init_job_inst }

        self.recalculate_map =  {'stampede.job_inst.#' : self.recalculate_job_inst}
        #functions should be added incrementally if we are implementing more event handlers

        #Declaring queue size, output file name, host name and the queue we'll
        #listen to with this receiver.
        self.Q = Queue.PriorityQueue(max_size)
        self.JsonObj = JsonOutput(json_name)
        self.host = host

        #Taghrid.start
        self.exchange = exchangeName
        self.bindKey = bindKey
        self.init_map[self.bindKey]()
        #Taghrid.end


        #Establishing connection with the server.
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=self.host))
        self.channel = self.connection.channel()

        #Creating a topic exchange.
        self.channel.exchange_declare(exchange=exchangeName,
                         type='topic')

        #Getting a random queue name.
        randomize = self.channel.queue_declare(exclusive=True)
        self.random_name = randomize.method.queue

        #Binding the queue to the routing key.
        self.channel.queue_bind(exchange=exchangeName,
                   queue=self.random_name,
                   routing_key=bindKey)

    #Taghrid.start
    def init_job_inst(self):
        """
        Code moved from init
        """
         #Initiliazing starting, successful, failure-ended, terminated and running jobs.
        #Also initializing duration and job count variables.
        self.starting = 0
        self.successful = 0
        self.failing = 0
        self.running = 0
        self.terminated = 0

        #[main/pre/post]Duration: [main/pre/post]Sum / [main/pre/post]Count
        #[Float Division]
        self.preDuration = 0.0
        self.mainDuration = 0.0
        self.postDuration = 0.0

        #[main/pre/post]Sum: Total sum of all durations of [main/pre/post] processing stages.
        self.preSum = 0.0
        self.mainSum = 0.0
        self.postSum = 0.0

        #[main/pre/post]Count: No. of jobs that successfully executed the
        #[main/pre/post]-processing stage.
        self.preCount = 0
        self.mainCount = 0
        self.postCount = 0

        #Three dictionaries for the buffering of pending jobs in either
        #pre, main and post processing stages that have not yet finished.
        self.preDict = {}
        self.mainDict = {}
        self.postDict = {}

        #Creation of table, engine and establishing database connection.
        self.engine = create_engine('sqlite:///jsonout.db', echo=False)

        self.metadata = MetaData()

        self.json = Table('JSONOUT', self.metadata,
             Column('id', Integer, primary_key=True),
             Column('Running', BigInteger),
             Column('Successful', BigInteger),
             Column('Failure', BigInteger),
             Column('PreDuration', Float),
             Column('MainDuration', Float),
             Column('PostDuration', Float),
             #Added this week!
             Column ('Latest', BigInteger),
             Column ('job_inst_id',BigInteger))

        self.metadata.create_all(self.engine)
    #Taghrid.end

    def run(self):
        """
        Creation of LineProducer object in order to parse at the receiving end
        into JSON file.
        Initiates calls to recalculate and printAll methods.
        Starts consuming on the passed queue (waiting for messages to receive)
        """
        #Creation of LineProducer object.
        lineProd = LineProducer(self.Q)


        print ' [*] Waiting for messages...'

        def callback(ch, method, properties, body):
            #body: the actual body of the message that we need to parse + format to a JSON object.
            #print " [x] Received", body, " @: ", strftime("%a, %d %b %Y %H:%M:%S", gmtime())

            #The basic steps are simple enough: 1) Parse a line received to a dictionary,
            dict = lineProd.parse_line(self,body)
            #Taghrid.start
            self.recalculate_map[self.bindKey](dict)
            #Taghrid.end
            printAll(self)

            #2) Pass the dictionary to the priority queue.
            lineProd.run(dict)

            if not self.Q.empty():
                self.JsonObj.put(self.Q.get())

        self.channel.basic_consume(callback,
                              queue=self.random_name,
                              no_ack=True)
        self.channel.start_consuming()

    #moved to be a method in the class
    def recalculate_job_inst(self,dict):
        """
        Calculates running, successful, failing, terminated and starting processes.
        Initiates call to the average duration function.
        Assigns these values to the database table titled "JSON".

        Arguments:
        dict: Dictionary containing parsed line from .bp file.
        """

        #Catch all job_inst events.
        if dict['event'].rfind("stampede.job_inst") is not -1:
            #Send these events to the average-duration calculation function.
            self.averageDur(dict)
        #Catch events that have the prototypes job_inst.main.start and .end:
        if dict['event'].rfind("stampede.job_inst.main.start") is not -1:
            self.starting += 1
        elif dict['event'].rfind("stampede.job_inst.main.end") is not -1:
            try:
                if dict['status'].rfind("-1") is not -1:
                    self.failing += 1
                else:
                    self.successful += 1
            #So as to prevent raising a 'KeyError' exception
            except:
                pass
        elif dict['event'].rfind ("stampede.job_inst.main.term") is not -1:
            self.terminated += 1

        self.running = self.starting - (self.failing + self.successful)

        if self.running < 0 :
            self.running = 0

        #Modified this week!
        #print "Timestamp: " , dict['ts'], ", Epoch: ", getSeconds(self,dict['ts']) , ", ts after getsecs: " , time.ctime(getSeconds(self,dict['ts']))
        conn = self.engine.connect()
        insertjson = self.json.insert()
        result = conn.execute(insertjson,Running=self.running, Successful=self.successful,
        Failure=self.failing, PreDuration=self.preDuration, MainDuration = self.mainDuration,
        PostDuration = self.postDuration,Latest = getSeconds(self,dict['ts']),
        job_inst_id = dict['job_inst.id'])
        result.close()

    def averageDur (self, event):
        """
        Calculates pre, main and post average durations and stores the results in
        preDuration, mainDuration and postDuration. Alters contents of preDict, mainDict
        and postDict.
        """
        try:
            #What is the scheduling ID?
            eventID = (event['job_inst.id']).strip("\n")

            #Is it a start event? If so, what is its type?
            if event['event'].rfind(".start") is not -1:
                #Putting this new entry to the corresponding dictionary of ids:timestamps.
                if event['event'].rfind(".pre") is not -1:
                    self.preDict[eventID] = getSeconds(self,event['ts'])
                elif event['event'].rfind(".main") is not -1:
                    self.mainDict[eventID] = getSeconds(self,event['ts'])
                    #print "Starting timestamp : " ,self.mainDict[eventID]
                elif event['event'].rfind(".post") is not -1:
                    self.postDict[eventID] = getSeconds(self,event['ts'])

            #Is it an end or termination event?
            elif event['event'].rfind(".end") is not -1 or event['event'].rfind(".term") is not -1:
            #See if event has already been recorded with us as starting and now it's ended,
            #so calculate its duration, increment count, consider it in the average,
            #and delete the event's entry from the corresponding dictionary:
                if eventID in self.preDict:
                    #Take the absolute value: Better be safe than sorry!
                    duration = abs(getSeconds(self,event['ts']) - self.preDict[eventID])
                    self.preCount += 1
                    self.preSum = self.preSum + duration
                    self.preDuration = self.preSum / self.preCount
                    del self.preDict[eventID]

                elif eventID in self.mainDict:
                    duration = abs(getSeconds(self,event['ts']) - self.mainDict[eventID])
                    self.mainCount += 1
                    self.mainSum = (self.mainSum + duration)
                    self.mainDuration = self.mainSum / self.mainCount
                    del self.mainDict[eventID]

                elif eventID in self.postDict:
                    duration = abs(getSeconds(self,event['ts']) - self.postDict[eventID])
                    self.postCount += 1
                    self.postSum = self.postSum + duration
                    self.postDuration = self.postSum / self.postCount
                    del self.postDict[eventID]
        except:
            pass
            print "KeyError exception in event with timestamp : ",event['ts']

def getSeconds (self,timestamp):
    """
    Returns the timestamp as seconds from the epoch.
    """
    return calendar.timegm(time.strptime(timestamp, r'%Y-%m-%dT%H:%M:%S.%fZ'))

def printAll(self):
    """
    Prints current statistics.
    """
    print "Running :",self.running," Starting: " ,self.starting,
    print " Successful: ",self.successful," Failing: ",self.failing,
    print " Terminated: ", self.terminated,
    print "Pre: ",self.preDuration, " Main: ",self.mainDuration, " Post: ",self.postDuration
    print "************************************************"

def usage():
    print "Some arguments are missing!"
    print "Usage: $python newReceive.py [HOSTNAME][MAX_SIZE] [OUTPUT_FILENAME] [EXCHANGE NAME]"
    print "[ROUTING KEY]"
    print ""

if __name__ == "__main__":
    answer = ''
    while len(argv) != 6:
        usage()
        answer = raw_input ("Would you still like to run the program with default arguments? Y/N")
        if answer is 'Y':
            if len(argv) < 2:
                print "Running with default arguments..."
                receiver = Recieve()
                receiver.start()
                break
            else:
                print "Running with the arguments you provided only which were:"
                print argv[1:]
                print ""
                receiver = Recieve(argv[1])
                receiver.start()
                break
        else:
            sys.exit(1)

    if answer is not 'Y':
        print "Running with the arguments you provided only which were:"
        print argv[1:]
        receiver = Recieve(*argv[1:])
        receiver.start()
    else:
        sys.exit(1)
