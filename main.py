import serial # Allows Python to communicate with the Arduino over USB
import time # Used to track time and create delays
import matplotlib.pyplot as plt # Library used to create real-time graphs and then renames it as plt for shorter commands. It is an alias.

ser = serial.Serial('/dev/cu.usbmodem1401', 9600, timeout = 1)
# Opens the serial port to communicate with the Arduino
# Arguments: (port name, baud rate, timeout)

time.sleep(2) # Waits 2 seconds so the Arduino has time to reset after opening the port

# Lists used to store the time, temperature, and humidity readings for graphing
times = [] # Stores the x-axis value (time since program started)
temps = [] # Stores temperature readings from the Arduino
hums = [] # Stores humidity readings from the Arduino

start_time = time.time() # Records the exact time the program started

# Creates a figure window containing 2 subplots: ax1 = top (temperature)
fig, (ax1, ax2) = plt.subplots (2, 1, figsize = (7,6))
# figsize sets the width and height of the graph in inches

while True:
    # Reads a single line sent by Arduino (e.g. "24.5, 48.0")
    # readline() returns bytes, .decode() converts converts bytes to string
    line = ser.readline().decode("utf-8", errors='ignore').strip()
    #strip() removes newline characters (\n, \r)
    if not line:
        continue # If the line is empty, skip this loop and wait for real data

    try:
        # Splits the incoming string at the comma, giving two separate numbers as text
        temp_str, hum_str = line.split(',')
        # Converts the temperature and humidity strings into floating-point numbers
        temp_val = float(temp_str)
        hum_val = float(hum_str)
    except ValueError:
        # If the line was not in the correct format, this avoids crashing the program
        print("Bad line", line)
        continue

    # Calculates how many seconds have passes since the script started
    current_time = time.time() - start_time

    #Stores the new readings in their lists for graphing
    times.append(current_time)
    temps.append(temp_val)
    hums.append(hum_val)

    # Clears previous frames so the graph can update in real time
    ax1.clear()
    ax2.clear()

    # Temperature Graph
    ax1.plot(times, temps, label= "Temperature (°C)")
    ax1.axhline(26, color='red', linestyle='--', label = "Buzzer Threshold (26°C)")
    # axhline draws a horizontal line at y = 26 to show the buzzer temperature limit
    ax1.set_ylabel("Temperature (°C)")
    ax1.legend()

    # Humidity Graph
    ax2.plot(times, hums, label = "Humidity (%)", color='orange')
    ax2.axhline(65, color = 'red',linestyle='--', label = "Buzzer Threshold")
    # Line at 65% humidity to indicate alarm level
    ax2.set_ylabel("Humidity (%)")
    ax2.set_xlabel("Time (s)")
    ax2.legend()

    # Determines whether the buzzer should be on
    #This uses exactly the same rule as the Arduino code
    buzzer_on = False
    if temp_val > 26 or hum_val > 65:
        buzzer_on = True

    if buzzer_on:
        # ax1.text places text at a location relative to the axis:
        # x = 0.5 is the middle, y = 0.9 is near the top
        # transform=ax1.transAxes means "use axis coordinates from 0 to 1"
        ax1.text(
            0.5 , 0.9, "BUZZER ON",
            transform=ax1.transAxes, # Tells the text to use axis-relative coordinates (not data coordinates)
            fontsize=16, color ='red',
            fontweight='bold',
            ha='center', # Centers the text horizontally
        )

    if buzzer_on:
        ax2.text(
            0.5 , 0.9, "BUZZER ON",
            transform=ax2.transAxes,
            fontsize=16, color= 'red',
            fontweight='bold',
            ha='center',
        )

    plt.tight_layout() # Prevents the two graphs from overlapping visually
    plt.pause(0.1)

    # pause(0.1) updates the graph every 0.1 seconds.
    # This is needed so the graph wouldn't freeze or never refresh