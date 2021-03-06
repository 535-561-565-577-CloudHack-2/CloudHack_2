# Use this file to setup the database consumer that stores the ride information in the database
# Code for Ride Matching Consumer

import pika
import os 
import time
import json
import sys
import pymongo

def main():
    def store_callback(ch, method, properties, body):
        ride_details = json.loads(body)
        print(" [x] Received %r" % body.decode())
        
        myclient = pymongo.MongoClient("mongodb")
        mydb = myclient["ride_details_db"] # create DB  
        rides = mydb["ride_details"] # create collection

        print(mydb.list_collection_names())
        x = rides.insert_one(ride_details)
        print(" [x] Record %r inserted into DB with ID: %r\n" % (method.delivery_tag, x.inserted_id))



    started = False
    while not started:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitMQ_server"))
            started = True
        except pika.exceptions.AMQPConnectionError as exc:
            print("Failed to connect to RabbitMQ service. Message wont be sent. Waiting for sometime..")
            time.sleep(5)

    channel = connection.channel()

    channel.queue_declare(queue='database', durable=True)

    channel.basic_consume(
        queue='database', 
        auto_ack=True, 
        on_message_callback=store_callback
    )

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

