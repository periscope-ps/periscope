#COLLECTION_INTERVAL=1
#REPORTING_INTERVAL=10
#COLLECTION_TIME=0  # 0 is forever

#SLEEP_FACTOR=1 # decimal between 0 and 1 - what percentage of the time until the
               # next collection or reporting time should the process sleep
               # a higher number decreases cpu utilization at the possible
               # of expense accurate measurement timing
               # Going from 0 to 1 takes CPU utilization from 100% to 0.1%
               ### It would be interesting to see how much it being 1 actually
                 # effects accuracy of the collection/reporting interval

# UNIS_URL="http://monitor.damslab.org/"
# MS_URL="http://monitor.damslab.org/"

# PROC_DIR="/proc/"

# COLL_SIZE=30000
# COLL_TTL=15000

# # not sure about these guys
# COLL_SIZES={"iowait":10000,
#             "idle":1000}


# COLL_TTLS={"iowait":80000,
#            "swirq":10000}

# KWARGS={"proc_dir":"/proc"
#         }

EVENT_TYPES={
    'user':"ps:tools:blipp:linux:cpu:utilization:user",
    'system':"ps:tools:blipp:linux:cpu:utilization:system",
    'nice':"ps:tools:blipp:linux:cpu:utilization:nice",
    'iowait':"ps:tools:blipp:linux:cpu:utilization:iowait",
    'hwirq':"ps:tools:blipp:linux:cpu:utilization:hwirq",
    'swirq':"ps:tools:blipp:linux:cpu:utilization:swirq",
    'steal':"ps:tools:blipp:linux:cpu:utilization:steal",
    'guest':"ps:tools:blipp:linux:cpu:utilization:guest",
    'idle':"ps:tools:blipp:linux:cpu:utilization:idle",
    'onemin':"ps:tools:blipp:linux:cpu:load:onemin",
    'fivemin':"ps:tools:blipp:linux:cpu:load:fivemin",
    'fifteenmin':"ps:tools:blipp:linux:cpu:load:fifteenmin"    
    }
