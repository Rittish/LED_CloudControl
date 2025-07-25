import network
from machine import Pin
import time
import urequests
import ujson

# WiFi Configuration
WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"

# Firebase Configuration
FIREBASE_URL = "https://your-project-id.firebaseio.com"
FIREBASE_SECRET = "YOUR_FIREBASE_SECRET"
LED_PATH = "/led/status"  # Firebase path to monitor

# LED Setup
led = Pin(2, Pin.OUT)  # GPIO2 (D4 on NodeMCU)

def connect_wifi():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print("Connecting to WiFi...")
        sta_if.active(True)
        sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
        while not sta_if.isconnected():
            pass
    print("WiFi Connected:", sta_if.ifconfig())

def get_led_status():
    url = f"{FIREBASE_URL}{LED_PATH}.json?auth={FIREBASE_SECRET}"
    response = urequests.get(url)
    data = ujson.loads(response.text)
    response.close()
    return data

def control_led():
    status = get_led_status()
    if status == 1:
        led.on()
        print("LED ON")
    else:
        led.off()
        print("LED OFF")

def main():
    connect_wifi()
    while True:
        control_led()
        time.sleep(1)  # Check Firebase every second

if __name__ == "__main__":
    main()