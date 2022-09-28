README

PA1 - 

This directory contains sample code for the producer and consumer of Kafka topic.
We use the Linux "top" command in the producer process and send its output to a
Kafka broker. A consumer then pulls the incoming message and prints it.

Producer and consumer processes have hardcoded IP addresses as of now to my
setup but this will need to be modified. It will be better to get these as an argument
on the command line when you invoke the code.

First, obtain young01.pem, reiser01.pem, and producer.py from Kavi Palmer, Joseph Reiser, or Lauren Young.
Next, navigate to the directory containing young01.pem to access VM2 by
           ssh -i young01.pem cc@127.114.25.235

Next, go into the kafka directory
           cd kafka_2.13-3.2.1
           
Now, start up the ZooKeeper server           
           bin/zookeeper-server-start.sh config/zookeeper.properties

Now, start up the Kafka broker 0 in VM2
           bin/kafka-server-start.sh config/server.properties
           
Now, access VM3 by
           ssh -i reiser01.pem cc@127.114.26.26

Now, start up the Kafka broker 1 in VM3
           bin/kafka-server-start.sh config/server.properties

Open up another terminal in VM2. Run
           python3 consumer.py

Now, in your own VM1.i, run 
           python3 producer.py

At this point, your terminal in VM2 running consumer.py should see a flow of data coming from the producer.py being run in VM1.

Ensure that your server.properties file in your VM1.i Kafka is pointing to the ZooKeeper at VM2 (127.114.25.235, 10.56.3.161)
