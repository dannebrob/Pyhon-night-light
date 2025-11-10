from machine import Pin
import network
import ntptime
import neopixel
import time
import math

PIN = 21         # GPIO21
NUM = 24         # antal LEDs

np = neopixel.NeoPixel(Pin(PIN, Pin.OUT), NUM)

# sätt första LED till rött och skriv ut till stripen
np[0] = (255, 0, 0)
np.write()

#wifi conncect
def ensure_wifi():
    if not wlan.isconnected():
        print("Wi-Fi disconnected. Reconnecting...")
        wlan.connect('Stangorsgatan', 'Kakor&Bullar')
        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
        if wlan.isconnected():
            np[0] = (255, 0, 0)
            print("Reconnected. IP:", wlan.ifconfig()[0])
        else:
            print("Failed to reconnect.")


def get_time():
    try:
        ntptime.settime()
    except:
        print("Failed to sync time from NTP")
        return None

    timezone_offset = 3600  # 1 hour for CET
    adjusted_time = time.localtime(time.time() + timezone_offset)
    print("Current time:", adjusted_time)
    return adjusted_time

while True:
    ensure_wifi()
    current_time = get_time()
    if current_time:
        hour = current_time[3]
        print(hour)

        if hour >= 19:
            for i in range(NUM):
                np[i] = (255, 0, 0)  # Red
            np.write()

        elif 6 <= hour <= 9:
            for i in range(NUM):
                np[i] = (0, 255, 0)  # Green
            np.write()

        else:
            for i in range(NUM):
                np[i] = (0, 0, 0)  # Off
            np.write()

    time.sleep(60)  # Wait 1 minute before checking again




