import paho.mqtt.client as mqtt
import serial

ser = serial.Serial("/dev/rfcomm0", 9600)
#ser.write(str.encode('Start\r\n'))

def on_connect(client, userdata, flags, rc): # func for making connection
	print("Connected to MQTT")
	print("Connection returned result: " + str(rc) )
	client.subscribe("ifn649/LED")
	
def on_message(client, userdata, msg): # Func for Sending msg
	message = msg.payload.decode()
	command = f'${message}' #adding $ infront of message as we have substring 1 in the aurdino code
	ser.write(command.encode())
	# print(command)
	#ser.write(str.encode(command))
	
		
	
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("ip-addr", 1883, 60)
client.loop_forever()