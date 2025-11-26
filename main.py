import serial
import time
import matplotlib.pyplot as plt

serial = serial.Serial('/dev/cu.usbmodem1401', 9600, timeout = 1)

time.sleep(2)

times = []
temps = []
hums = []

start_time = time.time()

fig, (ax1, ax2) = plt.subplots (2, 1, fisize = (7,6))

while True:
    line = serial.readline().decode("utf-8", errors='ignore').strip()

    if not line:
        continue


    try:
        temp_str, hum_str = line.split(',')
        temp_val = float(temp_str)
        hum_val = float(hum_str)

    except ValueError:
        print("Bad line", line)
        continue

    current_time = time.time() - start_time
    time.append(current_time)
    temps.append(temp_val)
    hums.append(hum_val)

    ax1.clear()
    ax2.clear()

    ax1.plot(times, temps, label= "Temperature (°C)")
    ax1.set_ylabel("Temperature (°C)")
    ax1.legend()

    ax2.plot(times, hums, label = "Humidity (%)", color='orange')
    ax2.set_ylabel("Humidity (%)")
    ax2.set_xlabel("Time (s)")
    ax2.legend()

    plt.tight_layout()
    plt.pause(0.1)