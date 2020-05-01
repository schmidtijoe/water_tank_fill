#!/usr//bin/python3.7

# ----- imports -----
from __future__ import print_function
import time
import datetime
import json
import numpy as np


# ----- functions -----
def measure(temperature=20.0):
    """
    measures distance to ultrasonic sensor, returns cm value
    """
    GPIO.output(trig, 1)
    time.sleep(0.00001)
    GPIO.output(trig, 0)
    while GPIO.input(echo) == 0:
        pass
    start = time.time()
    while GPIO.input(echo) == 1:
        pass
    stop = time.time()
    sonic_speed = 331.5 + 0.6 * temperature
    elapsed = stop - start
    distance = (elapsed * sonic_speed) * 100 / 2  # s * m/s = m * 100 = cm
    return distance


def measure_avg(calibration=0.0, n_avg=3, temperature=20.0):
    """
    calls the measure function n times, calculates and returns average.
    """
    distance = calibration
    for ind in range(n_avg):
        distance += measure(temperature=temperature)
        time.sleep(2)  # wait for 200ms
    distance /= n_avg
    return distance


def measure_temperature():
    """
    1-wire slave file read and converting to number
    """
    file = open('/sys/bus/w1/devices/28-011939d72138/w1_slave')
    filecontent = file.read()
    file.close()

    stringvalue = filecontent.split("\n")[1].split(" ")[9]
    temperature_value = float(stringvalue[2:]) / 1000
    return temperature_value


def write_to_json(temperature, volume):
    with open('data.json', 'r+') as json_file:
        data = json.load(json_file)
        if len(data) >= 60:
            average = 0
            for k in range(30):
                average += data[k]
            average /= 30
            with open('long.json', 'r+') as archive_file:
                archive = json.load(archive_file)
                archive.append({'date': datetime.datetime.now().strftime("%d/%m/%Y"),
                                'last 30': average})
                archive_file.seek(0)
                json.dump(archive, archive_file)
            data = data[30:]
        data.append({
            'date': datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            'temperature': "{:.3f} °C".format(temperature),
            'fill_percentage': '{} %'.format(volume/max_volume*100)
        })
        json_file.seek(0)
        json.dump(data, json_file, indent=2)
    return


def calculate_fill(radius, length, f_dist):
    """
    returns fill volume in litres
    """
    height = np.clip(h_b - f_dist, 0.0, 120.0)
    a = np.arccos((radius - height) / radius)
    v_fill = length * (radius ** 2 * a - (radius - height) * np.sqrt(2 * radius * height - height ** 2)) / 1000.0
    return np.clip(v_fill, 0.0, 3000.0)


# ----- main script -----

# ----- variables -----
L = 223.0           # dimensions of tank [cm]
r = 72.0            # radius of inner cylinder [cm]

litres = 0
percis = 0
max_volume = 3000.0     # [l]

h_b = 177             # height where module is placed [cm]

# pin numbers
trig = 12
echo = 11
temp = 20  # degrees, can get this through temp sensor

calib = 2.3  # cm. calibration. Add this to refine measurement offset

# allow settling time
time.sleep(0.1)

# wrap in block to catch interrupts with cleanup
for k_index in range(20):
    print("Starting Measurement")
    temper = 15 + 5 * np.random.random(1)[0]
    print("measured temperature= {:.3f}".format(temper))
    distance = 50 + 50 * np.random.random(1)[0]
    print("measured dist: {:.3f} cm".format(distance))
    fill = calculate_fill(r, L, distance)
    print("fill volume= {:.3f} l".format(fill))
    fill_percentage = fill/max_volume * 100
    print("fill percentage= {:.1f} %".format(fill_percentage))
    write_to_json(temper, fill)
    time.sleep(1)


