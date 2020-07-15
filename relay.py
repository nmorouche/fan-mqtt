import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt

channel = 21
onOffStateTopic = "sensors/fan/activity/#"
rotationSpeedTopic = "sensors/fan/rotation-speed/#"

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.OUT)
pwm=GPIO.PWM(channel,30)

def motor_on(pin, speed, state):
	print("Motor is on")
	print("Speed: " + speed)
	
	if int(speed) <= 1:
		GPIO.output(channel,GPIO.HIGH)
	else:
		pwm.start(int(speed))
		sleep(5)

def motor_off(pin):
	print("Motor is off")
	pwm.stop()
	GPIO.output(channel, GPIO.LOW)
	time.sleep(1)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    print("User data: "+ str(userdata))

    client.subscribe(rotationSpeedTopic)
    client.subscribe(onOffStateTopic)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
       
    if msg.topic == "sensors/fan/rotation-speed":
	print("Run motor with speed")
        motor_on(channel, msg.payload, 1)
    elif msg.payload == "1":
	print("Turning motor on")
        motor_on(channel, msg.payload, 1)
    else:
        print("Stopping motor")
        motor_off(channel)

    print("Data received on topic: "+msg.topic+" "+str(msg.payload))


client = mqtt.Client()
client.username_pw_set(username="fan-mqtt-broker", password="raspberry")
client.on_connect = on_connect
client.on_message = on_message

client.connect("84.97.28.206:5003", 1883, 60)

client.loop_forever()
