
import os  # need this for popen
import time  # for sleep
import requests
import json
from kafka import KafkaProducer  # producer of events
from datetime import datetime

# Getting the current date and time
dt = datetime.now()

# getting the timestamp
ts = datetime.timestamp(dt)

# We can make this more sophisticated/elegant but for now it is just
# hardcoded to the setup I have on my local VMs

# acquire the producer
# (you will need to change this to your bootstrap server's IP addr)
producer = KafkaProducer (bootstrap_servers="129.114.25.235",
                                        acks=1)  # wait for leader to write to log

# say we send the contents 100 times after a sleep of 1 sec in between
for i in range(100):
    # get the output of the top command
    url = "https://odds.p.rapidapi.com/v4/sports/upcoming/odds"

    querystring = {"regions": "us", "oddsFormat": "decimal"}

    headers = {
        "X-RapidAPI-Key": "da7419996emsh0f8783ada86b441p12bbe7jsn453aa0a455d5",
        "X-RapidAPI-Host": "odds.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    contentText = response.json()

    content = json.dumps(contentText)

    content += ", {\"date\" : \""
    content += str(dt)
    content += "\"}"

    # read the contents that we wish to send as topic content
    # contents = process.read ()

    # send the contents under topic utilizations. Note that it expects
    # the contents in bytes so we convert it to bytes.
    #
    # Note that here I am not serializing the contents into JSON or anything
    # as such but just taking the output as received and sending it as bytes
    # You will need to modify it to send a JSON structure, say something
    # like <timestamp, contents of top>
    #
    producer.send ("utilizations1", value=bytes (content, 'ascii'))
    producer.flush ()   # try to empty the sending buffer

    # sleep a second
    time.sleep(1)

# we are done
producer.close ()
