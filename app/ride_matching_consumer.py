# Code for Ride Matching Consumer
import requests
import pika
import os 
import time
import json
import sys

def main():
    server_ip = os.environ.get('PRODUCER_ADDRESS')
    # server_port = os.environ.get('server_port')
    consumer_id = os.environ.get('CONSUMER_ID')

    def ride_matching_callback(ch, method, properties, body):
        ride_details = json.loads(body)
        print(" [x] Received %r" % body.decode())
        # print(" [x] Time is: %r" % ride_details['time'])
        time.sleep(ride_details['time'])
        print(" [x] Task %r done by %r" %  (method.delivery_tag, consumer_id))

    try:
        print("server_ip", server_ip)
        register = requests.post(server_ip+'/new_ride_matching_consumer', json={'consumer_id': consumer_id, "name": "Rabbit"}, verify=False)

        if(register.status_code == 200):
            started = False
            while not started:
                try:
                    connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitMQ_server"))
                    started = True
                except pika.exceptions.AMQPConnectionError as exc:
                    print("Failed to connect to RabbitMQ service. Message wont be sent. Waiting for sometime..")
                    time.sleep(5)

            channel = connection.channel()

            channel.queue_declare(queue='ride_match', durable=True)

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
        print('Exception in Main: ' + str(e))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

