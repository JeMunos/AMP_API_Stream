'''
Author: Jesse Munos
Date: October 2018

This file will define a class and associated methods needed for interfacing
with the Cisco AMP for Endpoints Streaming API.
This API is used for ingesting AMP for Endpoints event data into various SIEM
products such as ELK.

We will start by building the example code from the pika docs.
https://pika.readthedocs.io/en/stable/intro.html

Once this is complete we will modify until we have a functional stable connection.
Next we will create variables for all the needed paramters and move them to a config file. 
'''


import pika
credentials = pika.PlainCredentials('username', 'password')
#parameters = pika.ConnectionParameters(credentials=credentials)
parameters = pika.URLParameters('amqp://guest:guest@rabbit-server1:5672/%2F?backpressure_detection=t')

# Create a global channel variable to hold our channel object in
channel = None

# Step #2
def on_connected(connection):
    """Called when we are fully connected to RabbitMQ"""
    # Open a channel
    connection.channel(on_channel_open)

# Step #3
def on_channel_open(new_channel):
    """Called when our channel has opened"""
    global channel
    channel = new_channel
    channel.queue_declare(queue="test", durable=True, exclusive=False, auto_delete=False, callback=on_queue_declared)

# Step #4
def on_queue_declared(frame):
    """Called when RabbitMQ has told us our Queue has been declared, frame is the response from RabbitMQ"""
    channel.basic_consume(handle_delivery, queue='test')

# Step #5
def handle_delivery(channel, method, header, body):
    """Called when we recieve a message from RabbitMQ"""
    print(body)

# Step #1: Connect to RabbitMQ using the default parameters
parameters = pika.ConnectionParameters()
connection = pika.SeelctConnection(parameters, on_connected)

def on_open(connection):
    # Invoked when the connection is open
    pass

# Create our connection object, passing in the on_open method
connection = pika.SelectConnection(on_open_callback=on_open)

try:
    # Loop so we can communicate with RabbitMQ
    connection.ioloop.start()
except KeyboardInterrupt:
    # Gracefully close the connection
    connection.close()
    # Loop until we're fully closed, will stop on its own
    connection.ioloop.start()

    
    
