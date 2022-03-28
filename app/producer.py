from flask import Flask, request
import pika
import json


app = Flask(__name__)

@app.route("/")
def index():
    return "OK"


@app.route('/new_ride', methods=['POST'])
def add():
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
    channel.queue_declare(queue='task_queue', durable=True)

    sleep_time = request.json['time']
    # .get('time')
    # .form.get('time')

    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=str(sleep_time),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))

    connection.close()
    return " [x] Sent: %s" % str(sleep_time)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5000')