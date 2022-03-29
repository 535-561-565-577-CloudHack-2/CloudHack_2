from flask import Flask, request
import pika
import json
import time

app = Flask(__name__)

REGITRATION_LIST = []

@app.route("/")
def index():
    return "OK"


@app.route('/new_ride', methods=['POST'])
def new_ride():
    """
    POST req body

    {
        "pickup": "string:optional",
        "destination": "string:optional",
        "time": "float - seconds:required",
        "cost": "float:optional",
        "seats": "integer:optional"
    }

    """

    started = False
    while not started:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitMQ_server"))
            started = True
        except pika.exceptions.AMQPConnectionError as exc:
            print("Failed to connect to RabbitMQ service. Message wont be sent. Waiting for sometime..")
            time.sleep(5)

    # except Exception as e:
    #     return str(e)
    
    channel = connection.channel()
    channel.queue_declare(queue='ride_match', durable=True)
    channel.queue_declare(queue='database', durable=True)

    sleep_time = request.json['time']
    # .get('time')
    # .form.get('time')

    print(" [x] Received %r" % request.json)
    
    print(" [x] Publishing to ride match queue")
    channel.basic_publish(
        exchange='',
        routing_key='ride_match',
        body=json.dumps(request.json),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))

    print(" [x] Publishing to database")
    channel.basic_publish(
        exchange='',
        routing_key='database',
        body=json.dumps(request.json),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))

    connection.close()
    return " [x] Sent: %s" % json.dumps(request.json)


@app.route('/new_ride_matching_consumer', methods=['POST']) 
def register():
    """
    POST request body format

    {
        "consumer_id": "integer",
        "name": "string"
    }

    """
    global REGITRATION_LIST

    ip_address = request.remote_addr

    registration = {"name": request.json.get('consumer_id'), "ip_address": ip_address}
    REGITRATION_LIST.append(registration)
    print("REGITRATION_LIST: ", REGITRATION_LIST)

    return json.dumps(REGITRATION_LIST)
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5000')