import settings

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

KWARGS={"proc_dir":"/proc",
        "unis_url":settings.UNIS_URL,
        "subject":settings.SUBJECT
        }

EVENT_TYPES={
    "packets_in":"ps:tools:blipp:linux:network:ip:utilization:packets:in",
    "packets_out":"ps:tools:blipp:linux:network:ip:utilization:packets:out",
    "bytes_in":"ps:tools:blipp:linux:network:utilization:bytes:in",
    "bytes_out":"ps:tools:blipp:linux:network:utilization:bytes:out",    
    "errors":"ps:tools:blipp:linux:network:ip:utilization:errors",
    "drops":"ps:tools:blipp:linux:network:ip:utilization:drops",
    "tcp_segments_in":"ps:tools:blipp:linux:network:tcp:utilization:segments:in",
    "tcp_segments_out":"ps:tools:blipp:linux:network:tcp:utilization:segments:out",    
    "tcp_retrans":"ps:tools:blipp:linux:network:tcp:utilization:retrans",
    "datagrams_in":"ps:tools:blipp:linux:network:udp:utilization:datagrams:in",
    "datagrams_out":"ps:tools:blipp:linux:network:udp:utilization:datagrams:out"    
    }
