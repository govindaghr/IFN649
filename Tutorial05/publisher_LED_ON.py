import paho.mqtt.publish as publish

publish.single("ifn649/LED", "LED_ON", hostname="ip-addr")
print("LED_ON")
