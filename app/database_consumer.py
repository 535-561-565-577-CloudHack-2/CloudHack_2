# Use this file to setup the database consumer that stores the ride information in the database
# Code for Ride Matching Consumer

import requests
import pika
import os 
import time
import json
import sys
import pymongo

def main():
    server_ip = os.environ.get('PRODUCER_ADDRESS')
    # server_port = os.environ.get('server_port')
    consumer_id = os.environ.get('CONSUMER_ID')

    def ride_matching_callback_store(ch, method, properties, body):
        ride_details = json.loads(body)
        print(" [x] Received %r" % body.decode())
        
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["ride_details_db"] # create DB  
        rides = mydb["ride_details"] # create collection

        if rides in mydb.list_collection_names(): # check if collection exists
            x = rides.insert_one(ride_details)
            print(" [x] %r inserted into DB\n" % method.delivery_tag)
        else:
            print('Collection not created yet..')

        # ride_details = {"pickup":"", "destination": "", "time": "", "cost": "", "seats": ""}


    try:
        if(register.status_code == 200):
            try:
                connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
            except pika.exceptions.AMQPConnectionError as exc:
                print("Failed to connect to RabbitMQ service. Message wont be sent.")

            connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
            channel = connection.channel()

            # channel.queue_declare(queue='ride_match')

            channel.basic_consume(
                queue='ride_match', 
                auto_ack=True, 
                on_message_callback=ride_matching_callback
            )

            print(' [*] Waiting for messages. To exit press CTRL+C')
            channel.start_consuming()
        else:
            print('Failed Request', register.status_code)

    except Exception as e:
        print('Invalid IP Address')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

