from newblipp.unis_client import *
from newblipp.ms_client import *

meta = {"parameters": {"collectionInterval": 1,
                       "datumSchema": "http://unis.incntre.iu.edu/schema/20120709/datum#"},

        "id": "1234",
        "eventType": "nl:tools:calipers:summary:write",
        "subject": {"href": "http://127.0.0.1/nodes/dtn01",
                    "rel": "full",
                    "task_id": "XXX",
                    "type": "network",
                    "src": "localhost",
                    "dst": "localhost",
                    "stream_id": "24567:56343"}
}
        
data = [{"mid": "1234",
         "data": [
            {"ts": 143234212.3242,
             "_sample": 4,
             "sum_v": 3432532.342,
             "min_v": 1231241,
             "max_v": 3523523,
             "count": 39102}
            ]
         }]

ms = MSInstance("http://localhost:80")
unis = UNISInstance("http://localhost:80")

print meta
unis.post_metadata(meta)

ms.post_events("http://127.0.0.1/metadata/1234", 10000, 10000)

print data
ms.post_data(data)

