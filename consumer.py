#
#
# Author: Aniruddha Gokhale
# CS4287-5287: Principles of Cloud Computing, Vanderbilt University
#
# Created: Sept 6, 2020
#
# Purpose:
#
#    Demonstrate the use of Kafka Python streaming APIs.
#    In this example, demonstrate Kafka streaming API to build a consumer.
#

import os   # need this for popen
import time # for sleep
from kafka import KafkaConsumer  # consumer of events
import json
#import couchdb
from couchbase.cluster import Cluster, ClusterOptions, QueryOptions
#from couchbase_core.cluster import PasswordAuthenticator


# We can make this more sophisticated/elegant but for now it is just
# hardcoded to the setup I have on my local VMs

# acquire the consumer
# (you will need to change this to your bootstrap server's IP addr)
consumer = KafkaConsumer (bootstrap_servers="129.114.25.235:9092")

# subscribe to topic
#couch = couchdb.Server("http://admin:group11@129.114.26.26:5984/")

cluster = Cluster('couchbase://129.114.27.101', authenticator=PasswordAuthenticator('group11', 'group11')))
bucket = cluster.bucket('default')
coll = bucket.default_collection()

consumer.subscribe (topics=["utilizations1"])


#db = couch["utilizations"]

# we keep reading and printing
i = 0
for msg in consumer:
    # what we get is a record. From this record, we are interested in printing
    # the contents of the value field. We are sure that we get only the
    # utilizations topic because that is the only topic we subscribed to.
    # Otherwise we will need to demultiplex the incoming data according to the
    # topic coming in.
    #
    # convert the value field into string (ASCII)
    #
    # Note that I am not showing code to obtain the incoming data as JSON
    # nor am I showing any code to connect to a backend database sink to
    # dump the incoming data. You will have to do that for the assignment.
    msg = str(msg.value, 'ascii')
    msg = json.loads(msg)
    print(msg[0])
    bucket.upsert('Data Piece ' + str(i), msg[0])
    #db.save(msg[0])

# we are done. As such, we are not going to get here as the above loop
# is a forever loop.
consumer.close ()
