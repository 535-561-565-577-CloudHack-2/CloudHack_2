# Code for Ride Matching Consumer
import requests
import pika
import os 
import time

def ride_matching_callback(ch, method, proerties, body):
    print(" [x] Received %r" % body.decode())
    time.sleep(body.time)
    print(" [x] Done %r" % body.task_id)

server_ip = os.environ.get('server_ip')
server_port = os.environ.get('server_port')
consumer_id = os.environ.get('consumer_id')

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

register = requests.post(server_ip+'/new_ride_matching_consumer', data={'consumer_id': consumer_id})

channel.queue_declare(queue='ride_match')

channel.basic_consume(queue='ride_match', \
                    auto_ack=True, \
                    on_message_callback=ride_matching_callback)

