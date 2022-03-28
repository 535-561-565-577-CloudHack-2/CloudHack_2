from flask import Flask, request
import pika
import json


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

    
    # connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    except pika.exceptions.AMQPConnectionError as exc:
        return "Failed to connect to RabbitMQ service. Message wont be sent."

    # except Exception as e:
    #     return str(e)
    
    channel = connection.channel()
    channel.queue_declare(queue='ride_match', durable=True)
    channel.queue_declare(queue='database', durable=True)

    sleep_time = request.json['time']
    # .get('time')
    # .form.get('time')

    channel.basic_publish(
        exchange='',
        routing_key='ride_match',
        body=json.dumps(request.json),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))

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
    return json.dumps(REGITRATION_LIST)
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5000')