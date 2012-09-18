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

#COLL_SIZE=30000
#COLL_TTL=15000

KWARGS={"proc_dir":"/proc"
        }

EVENT_TYPES={
    "free":"ps:tools:blipp:linux:memory:utilization:free",
    "used":"ps:tools:blipp:linux:memory:utilization:used",
    "buffer":"ps:tools:blipp:linux:memory:utilization:buffer",
    "cache":"ps:tools:blipp:linux:memory:utilization:cache",
    "kernel":"ps:tools:blipp:linux:memory:utilization:kernel"
    }
