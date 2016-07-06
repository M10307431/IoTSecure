#!/usr/bin/python3

#required libraries
import sys                                 
import ssl
import socket
import paho.mqtt.client as mqtt

#called while client tries to establish connection with the server
def on_connect(client, userdata, flags, rc):
    if rc==0:
        print ("Subscriber Connection status code: "+str(rc)+" | Connection status: successful")
    elif rc==1:
        print ("Subscriber Connection status code: "+str(rc)+" | Connection status: Connection refused")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$aws/things/raspberry-pi3/shadow/update" , qos=1 )

def on_message(client, userdata, msg):
    #print("topic: "+msg.topic)
    #print("payload: "+str(msg.payload))
    print("Received message from topic: "+msg.topic+" | QoS: "+str(msg.qos))
    print("Data Received: "+str(msg.payload))

#def on_log(client, userdata, level, msg):
#    print(msg.topic+" "+str(msg.payload))
  
#called when a topic is successfully subscribed to
def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos)+"data"+str(obj))

#creating a client with client-id=mqtt-test
mqttc = mqtt.Client()

mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe
mqttc.on_message = on_message
#mqttc.on_log = on_log

awshost = "AXOX7WEKAR78O.iot.us-west-2.amazonaws.com"
awsport = 8883
clientId = "raspberry-pi3"
thingName = "raspberry-pi3"
caPath = "rootCA.crt"
certPath = "cert.pem"
keyPath = "privkey.pem"

#Configure network encryption and authentication options. Enables SSL/TLS support.
#adding client-side certificates and enabling tlsv1.2 suppomqttrt as required by aws-iot service
mqttc.tls_set(caPath,
              certfile=certPath,
              keyfile=keyPath,
              cert_reqs=ssl.CERT_REQUIRED,
              tls_version=ssl.PROTOCOL_TLSv1_2,
              ciphers=None)
print("Security policy : SSL_PROTOCOL_TLSv1_2")
#connecting to aws-account-specific-iot-endpoint
mqttc.connect(awshost, awsport, keepalive=60) #AWS IoT service hostname and portno

#automatically handles reconnecting
mqttc.loop_forever()
