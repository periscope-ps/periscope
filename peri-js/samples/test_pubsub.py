import os
from subprocess import call
import json

with open('nodes.json', 'r') as data_file:
    json_file = json.load(data_file)
    node = json.dumps(json_file)

with open('services.json', 'r') as data_file:
    json_file = json.load(data_file)
    service = json.dumps(json_file)

with open('measurements.json', 'r') as data_file:
    json_file = json.load(data_file)
    measurement = json.dumps(json_file)

with open('ports.json', 'r') as data_file:
    json_file = json.load(data_file)
    port = json.dumps(json_file)

with open('links.json', 'r') as data_file:
    json_file = json.load(data_file)
    link = json.dumps(json_file)

with open('domains.json', 'r') as data_file:
    json_file = json.load(data_file)
    domain = json.dumps(json_file)

with open('metadatas.json', 'r') as data_file:
    json_file = json.load(data_file)
    metadata = json.dumps(json_file)

with open('data1.json', 'r') as data_file:
    json_file = json.load(data_file)
    data1 = json.dumps(json_file)

with open('data2.json', 'r') as data_file:
    json_file = json.load(data_file)
    data2 = json.dumps(json_file)

print "\033[31mPublishing \033[36m3\033[31m to nodes\033[0m"
call(["curl", "-H", "Content-Type: application/perfsonar+json", "--data", node, "http://dev.incntre.iu.edu:8888/nodes"])

print "\033[35mPublishing id \033[36m4\033[35m to services\033[0m"
call(["curl", "-H", "Content-Type: application/perfsonar+json", "--data", service, "http://dev.incntre.iu.edu:8888/services"])

print "\033[34mPublishing id \033[36m2\033[34m to measurements\033[0m"
call(["curl", "-H", "Content-Type: application/perfsonar+json", "--data", measurement, "http://dev.incntre.iu.edu:8888/measurements"])

print "\033[34mPublishing id \033[36m2\033[34m to ports\033[0m"
call(["curl", "-H", "Content-Type: application/perfsonar+json", "--data", port, "http://dev.incntre.iu.edu:8888/ports"])

print "\033[34mPublishing id \033[36m2\033[34m to links\033[0m"
call(["curl", "-H", "Content-Type: application/perfsonar+json", "--data", link, "http://dev.incntre.iu.edu:8888/links"])

print "\033[34mPublishing id \033[36m2\033[34m to domains\033[0m"
call(["curl", "-H", "Content-Type: application/perfsonar+json", "--data", domain, "http://dev.incntre.iu.edu:8888/domains"])

print "\033[34mPublishing id \033[36m2\033[34m to metadata\033[0m"
call(["curl", "-H", "Content-Type: application/perfsonar+json", "--data", metadata, "http://dev.incntre.iu.edu:8888/metadata"])

print "\033[34mPublishing id \033[36m2\033[34m to data1\033[0m"
call(["curl", "-H", "Content-Type: application/perfsonar+json", "--data", data1, "http://dev.incntre.iu.edu:8888/data"])

print "\033[34mPublishing id \033[36m2\033[34m to data2\033[0m"
call(["curl", "-H", "Content-Type: application/perfsonar+json", "--data", data2, "http://dev.incntre.iu.edu:8888/data"])
