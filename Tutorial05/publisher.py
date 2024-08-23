import paho.mqtt.publish as publish

publish.single("ifn649", "Hello World", hostname="ip-addr")
print("Done")
