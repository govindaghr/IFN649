import paho.mqtt.publish as publish

publish.single("ifn649/LED", "LED_OFF", hostname="ip-addr")
print("LED_OFF")