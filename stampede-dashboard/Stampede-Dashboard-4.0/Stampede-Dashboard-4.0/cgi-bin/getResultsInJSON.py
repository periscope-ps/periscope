#!/usr/bin/python

from __future__ import division
import cgi
from sqlalchemy import BigInteger
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.exc import OperationalError
from sqlalchemy.types import Float
from sqlalchemy.orm import sessionmaker

# Required header that tells the browser how to render the HTML.
print "Content-Type: application/json\n\n"

#Setting up things...
engine = create_engine('sqlite:///jsonout.db', echo=False)
metadata = MetaData()

#Table setup...
json = Table('JSONOUT', metadata,
           Column('id', Integer, primary_key=True),
           Column('Running', BigInteger),
           Column('Successful', BigInteger),
           Column('Failure', BigInteger),
           Column('PreDuration', Float),
           Column('MainDuration', Float),
           Column('PostDuration', Float),
           Column ('Latest', BigInteger),
           Column ('job_inst_id', BigInteger))
try:

    metadata.create_all(engine)
    conn = engine.connect()
    #conn.isolation_level = "IMMEDIATE"
    #Creating a select statement to select the last data stored in to send to the browser...
    selectlast = select([func.max(json.c.id), json.c.Running, json.c.Successful,
                        json.c.Failure, json.c.PreDuration, json.c.MainDuration, json.c.PostDuration, json.c.Latest,
                        json.c.job_inst_id])
    result = conn.execute(selectlast)

    #Fetching the selected row...
    table = result.fetchone()

    #Printing the JSON object...
    print '{"Running": ', table['Running'], ',"Successful": ', table['Successful'], ',"Failure": ', table['Failure'],
    print ',"PreDuration": ', table['PreDuration'], ',"MainDuration" :', table['MainDuration'], ',"PostDuration": ',
    print table['PostDuration'], ',"Timestamp": ', table['Latest'], ',"job_inst_id":"', table['job_inst_id'], '"}'

    #Printing the returned result...
    #print table
    result.close()
except OperationalError:
    print ""
