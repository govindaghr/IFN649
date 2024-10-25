import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import serial
import string
import re

# Define the MQTT broker settings (use your public DNS)
broker_address = "ec2-3-25-206-82.ap-southeast-2.compute.amazonaws.com"
broker_port = 8883  # Port for TLS communication
# Path to the CA certificate file
ca_cert_path = "/home/govindaghr/IFN649/SBIDS/ca.crt"

try:
    ser = serial.Serial("/dev/rfcomm0", 9600)
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit(1)

# Callback function for connection success
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
        client.subscribe("safeBox/access")  # Subscribe to a topic
    else:
        print(f"Failed to connect, return code {rc}")

# Callback function for received messages
def on_message(client, userdata, message):
    msg = (message.payload.decode()).upper()
    print(f"Message received: {msg} on topic {message.topic}")
    try:
        ser.write(msg.encode())  # Send the message to the serial port
    except serial.SerialException as e:
        print(f"Error writing to serial port: {e}")

# Create a new MQTT client instance
client = mqtt.Client()
# Set the TLS configuration to use the CA certificate
client.tls_set(ca_certs=ca_cert_path)
# Set up the connection callback
client.on_connect = on_connect
# Set up the message callback
client.on_message = on_message

try:
    # Connect to the MQTT broker
    client.connect(broker_address, broker_port)
except Exception as e:
    print(f"Error connecting to MQTT broker: {e}")
    exit(1)

# Variables to store previous temperature and humidity readings
prev_temp = None
prev_humidity = None

def read_serial():
    global prev_temp, prev_humidity
    while True:
        try:
            rawserial = ser.readline().decode('utf-8').strip()
            print(f"Serial message: {rawserial}")
            
            # Check for "UnauthorizedAccess" in the message
            if "UNAUTHORIZEDACCESS" in rawserial.upper():
                publish.single("safeBox/alert", "Unauthorised access detected!", hostname=broker_address, port=broker_port, tls={'ca_certs': ca_cert_path} )
                print("Alert: Unauthorised access detected!")

            if "Temperature:" in rawserial and "Humidity:" in rawserial:
                temp_match = re.search(r'Temperature:\s*([\d.]+)\s*C', rawserial)
                humidity_match = re.search(r'Humidity:\s*([\d.]+)\s*%', rawserial)
                if temp_match and humidity_match:
                    temp = float(temp_match.group(1))
                    humidity = float(humidity_match.group(1))

                    #print(f"Temperature: {temp}")
                    #print(f"Humidity: {humidity}")

                    if prev_temp is not None and abs(temp - prev_temp) >= 0.01:
                        #print("Alert: Temperature change detected")
                        publish.single("safeBox/alert", f"Temperature change detected: {temp}C", hostname=broker_address, port=broker_port, tls={'ca_certs': ca_cert_path})
                        print(f"Alert: Temperature change detected: {temp}C")

                    if prev_humidity is not None and abs(humidity - prev_humidity) >= 0.01:
                        publish.single("safeBox/alert", f"Humidity change detected: {humidity}%", hostname=broker_address, port=broker_port, tls={'ca_certs': ca_cert_path})
                        print(f"Alert: Humidity change detected: {humidity}%")

                    prev_temp = temp
                    prev_humidity = humidity
			

        except serial.SerialException as e:
            print(f"Error reading from serial port: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

# Start the serial reading in a separate thread
import threading
serial_thread = threading.Thread(target=read_serial)
serial_thread.start()

# Start the network loop to process callbacks and messages
client.loop_forever()
