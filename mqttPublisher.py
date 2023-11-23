import time
from umqttsimple import MQTTClient
import ubinascii
import micropython
import network
import esp
import gc
import machine
from machine import Pin


def sendertest():
    print("jens")
    if dør.value(1):
        msg = "open"
        klient.publish(topic_Pub, msg)
    elif dør.value(0):
        msg = "clos"
        klient.publish(topic_Pub, msg)
        
def pubåben():
        msg = "open"
        klient.publish(topic_Pub, msg)

def publuk():
    msg = "clos"
    klient.publish(topic_Pub, msg)
            # Add your code here to handle the door being closed
def dør_send():
    if dør.value() == 1:
        msg = "åben"
        klient.publish(topic_Pub, msg)
        # Add your code here to handle the door being open
    elif dør.value() == 0:
        msg = "lukket"
        klient.publish(topic_Pub, msg)
        # Add your code here to handle the door being closed

def restart():
    time.sleep(1)
    machine.reset()

def klientcb():
    pass

#Led der skal lyse, hvis internet ikke er forbundet
led = machine.Pin(13, machine.Pin.OUT)

dør = Pin(14, mode=Pin.OUT)

esp.osdebug(None)
gc.collect()

#Internet navn/password
ssid = "FTTH_DU1219"
password = "Derek401"
#Raspberry pi IP (brokeren til mqtt)
brokerIP = "192.168.0.192"

#Forbind til net
net = network.WLAN(network.STA_IF)
net.active(True)
if not net.isconnected():
    net.connect(ssid,password)
    #Tænd for led, hvis intet net (LED lyser rød, til venstre for port)
    while not net.isconnected():
        led.value(1)
        time.sleep(2)
print("Du er nu forbundet IP = " + net.ifconfig()[0])

#Klient + ID
klientID = ubinascii.hexlify(machine.unique_id())
klient = MQTTClient(klientID, brokerIP, user="gruppe3",password="gruppe3")
klient.set_callback(klientcb)
klient.connect()


#Topic der skal publishes til
topic_Pub = b'dør'


while True:
    try:
        dør.value(1)
        dør.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING, handler=sendertest)

    except OSError:
        restart()

        



