from machine import Pin
import network
import ntptime
import neopixel
import time

PIN = 21         # GPIO21
NUM = 24         # antal LEDs

np = neopixel.NeoPixel(Pin(PIN, Pin.OUT), NUM)

# sätt första LED till rött och skriv ut till stripen
np[0] = (255, 0, 0)
np.write()

#wifi setup

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Connect to Wi-Fi and wait for connection
def ensure_wifi():
    if not wlan.isconnected():
        print("Wi-Fi disconnected. Reconnecting...")
        wlan.connect('ssid', 'secret')
        timeout = 10
        while not wlan.isconnected() and timeout > 0:
            time.sleep(1)
            timeout -= 1
        if wlan.isconnected():
            np[0] = (255, 0, 0)
            print("Reconnected. IP:", wlan.ifconfig()[0])
        else:
            print("Failed to reconnect.")

# Get current time from NTP and adjust for timezone
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

# Main loop, checking time and updating LEDs accordingly
while True:
    ensure_wifi()
    current_time = get_time()
    if current_time:
        hour = current_time[3]
        minute = current_time[4]
        weekday = current_time[6]
        # print(hour)

       # Evening red light between 19:00 and 06:15
        if hour >= 19 or (hour == 6 and minute < 15) or hour < 6:
            for i in range(NUM):
                np[i] = (125, 10, 0)  # Dim red/orange
            np.write()

        # Morning green light between 06:15 and 09:00
        elif (hour == 6 and minute >= 15) or (7 <= hour <= 9):
            if weekday in (5, 6):  # Saturday or Sunday
                if hour >= 7:
                    for i in range(NUM):
                         np[i] = (0, 30, 0)  # Dim green
                    np.write()
                else:
                    for i in range(NUM):
                        np[i] = (0, 0, 0)  # Off
                    np.write()
            else:  # Monday to Friday
                for i in range(NUM):
                    np[i] = (0, 30, 0)  # Dim green
                np.write()

        # Daytime off
        else:
            for i in range(NUM):
                np[i] = (0, 0, 0)  # Off
            np.write()



    time.sleep(60)  # Wait 1 minute before checking again
