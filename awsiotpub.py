#!/usr/bin/python3

# this source is part of my Hackster.io project:  https://www.hackster.io/mariocannistra/radio-astronomy-with-rtl-sdr-raspberrypi-and-amazon-aws-iot-45b617

# use this program to test the AWS IoT certificates received by the author
# to participate to the spectrogram sharing initiative on AWS cloud

# this program will publish test mqtt messages using the AWS IoT hub
# to test this program you have to run first its companion awsiotsub.py
# that will subscribe and show all the messages sent by this program

import paho.mqtt.client as mqtt
import json
import os
import socket
import ssl
from time import sleep
from random import uniform

connflag = False

def on_connect(client, userdata, flags, rc):
    global connflag
    connflag = True
    if rc==0:
        print ("Subscriber Connection status code: "+str(rc)+" | Connection status: successful")
    elif rc==1:
        print ("Subscriber Connection status code: "+str(rc)+" | Connection status: Connection refused")

def on_message(client, userdata, msg):
    print("Received message from topic: "+msg.topic+" | QoS: "+str(msg.qos))
    print("Data Received: "+str(msg.payload))

#def on_log(client, userdata, level, buf):
#    print(msg.topic+" "+str(msg.payload))

mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message
#mqttc.on_log = on_log

awshost = "AXOX7WEKAR78O.iot.us-west-2.amazonaws.com"
awsport = 8883
clientId = "raspberry-pi3"
thingName = "raspberry-pi3"
caPath = "rootCA.crt"
certPath = "cert.pem"
keyPath = "privkey.pem"
topic = "$aws/things/raspberry-pi3/shadow/update"
mqttc.tls_set(caPath,
              certfile=certPath,
              keyfile=keyPath,
              cert_reqs=ssl.CERT_REQUIRED,
              tls_version=ssl.PROTOCOL_TLSv1_2,
              ciphers=None)
print("Security policy : SSL_PROTOCOL_TLSv1_2")

mqttc.connect(awshost, awsport, keepalive=60)

mqttc.loop_start()

cnt = 0
while True:
    sleep(5)
    cnt +=1
    if connflag == True :
        if cnt%6 == 0:
            SpO2reading = uniform(88.0, 93.9)
        else:
            SpO2reading = uniform(95.0,99.9)
        awsmsg = {'state' : {'reported' : {'action' : 'SpO2', 'result' : SpO2reading}}}
        payload = json.dumps(awsmsg)
        mqttc.publish(topic, payload, qos=1)
        print("msg sent: SpO2 " + "%.2f" % SpO2reading )
    else:
        print("waiting for connection...")
