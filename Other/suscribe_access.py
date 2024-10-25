import paho.mqtt.client as mqtt
import serial
import string

# Define the MQTT broker settings (use your public dns)
broker_address = "ec2-3-25-206-82.ap-southeast-2.compute.amazonaws.com"
broker_port = 8883 # Port for TLS communication
# Path to the CA certificate file
ca_cert_path = "/home/govindaghr/IFN649/SBIDS/ca.crt"

ser = serial.Serial("/dev/rfcomm0", 9600)

# Callback function for connection success
def on_connect(client, userdata, flags, rc): 
	if rc == 0: 
		print("Connected successfully") 
		client.subscribe("safeBox/access") # Subscribe to a topic
	else: 
		print(f"Failed to connect, return code {rc}")
		

# Callback function for received messages
def on_message(client, userdata, message):
	msg = (message.payload.decode()).upper()
	print(f"Message received: {msg} on topic {message.topic}")
	ser.write(msg.encode())  # Send the message to the serial port


# Create a new MQTT client instance
client = mqtt.Client() 
# Set the TLS configuration to use the CA certificate
client.tls_set(ca_certs=ca_cert_path) 
# Set up the connection callback
client.on_connect = on_connect
# Set up the message callback
client.on_message = on_message
# Connect to the MQTT broker
client.connect(broker_address, broker_port) 
# Start the network loop to process callbacks and messages
client.loop_forever()
