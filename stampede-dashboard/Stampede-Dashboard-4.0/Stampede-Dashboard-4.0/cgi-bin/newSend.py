#! /usr/bin/python

import sys
from sys import argv

from lineIO import LineProducer
import pika
import threading

class Send(threading.Thread):
    """
    RabbitMQ Sender class

    Attributes:
        host: hostname of the server. By default it is the 'localhost'.
        connection: Necessary during opening a connection to the server via pika.
        channel: Necessary during opening a connection to the server via pika.
    """
    def __init__(self, host='localhost'):
        """
        A constructor for our Sender class responsible for setting up 
        connections with the server.

        Arguments:
            host: The hostname.
        """

        threading.Thread.__init__(self)

        self.host = host
       
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()

    def startSending (self, fileName = 'source.bp', exchangeName = 'eventRoute'):
        """
        Opens file, parses for particular events that are then given
        a particular routing key before being sent. Receiver subscribes only
        to a particular routing key.

        Arguments:
            fileName: name of the .bp log file we're working with.
            exchangeName: The desired name for the exchange.
        """

        #Creating a TOPIC exchange with the provided name.
        self.channel.exchange_declare(exchange=exchangeName,
                         type='topic')

        
        f = open(fileName, "r")
        for line in f:
            #Because the parse_line function in LineProducer is static,
            #we simply use it to get a dictionary from the line. 
            dict = LineProducer.parse_line(self,line)

            #We now simply send the line with the event as the routing key.
            self.send (line,dict['event'],exchangeName)

    def send(self, msgToBeSent, routingKey = 'stampede.job_inst.#',exchangeName = 'eventRoute'):
        """
        Sends message (msgToBeSent) over RabbitMQ with given key [routingKey] over desig
        -nated exchange [exchangeName].

        Arguments:
            msgToBeSent: body of the message
            routingKey: On which queue it should send.
            exchangeName: The name of the exchange.
        """
            
        self.channel.basic_publish(exchange=exchangeName, routing_key=routingKey, body=msgToBeSent)

    def __del__(self):
        """
        A destructor for our Sender class.
        """
        self.connection.close()


def usage():
    print "Some arguments are missing!"
    print "Usage: $python newSend.py [HOSTNAME][SOURCE FILENAME][EXCHANGE]"
    print ""

if __name__ == "__main__":
    answer = ''
    while len(argv) !=4:
        usage()
        answer = raw_input ("Would you still like to run the program with default arguments? Y/N")
        if answer is 'Y':
            if len(argv) < 2:
                print "Running with default arguments..."
                sender = Send() # unpack the arguments
                sender.start()
                sender.startSending()
                break
            else:
                print "Running with the arguments you provided only which were:"
                print argv[1:]
                print ""
                sender = Send(argv[1])
                sender.start()
                sender.startSending(*argv[2:])
                break
        else:
            sys.exit(1)

    if answer is not 'Y':
        print "Running with the arguments you provided only which were:"
        print argv[1:]
        sender = Send(argv[1]) # unpack the arguments
        sender.start()
        sender.startSending(*argv[2:])
    else:
        sys.exit(1)
        


