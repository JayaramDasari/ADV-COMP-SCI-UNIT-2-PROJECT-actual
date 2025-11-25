import serial
import time
import matplotlib.pyplot as plt

serial = serial.Serial('/dev/cu.usbmodem1401', 9600, timeout = 1)

time.sleep(2)

times = []
temps = []
humidity = []

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