#!/home/don/mypy/bin/python3

import os
import sys
import time

thermometer_dir = '/sys/bus/w1/devices/'
thermometer = '28-17ef0087bca5'

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

def read_temp_raw(thermometer):
    device_file = thermometer_dir + thermometer + '/w1_slave'
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp(thermometer):
    lines = read_temp_raw(thermometer)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = round(float(temp_string) / 1000.0, 2)
        temp_f = round((temp_c * 9.0 / 5.0) + 32.0, 2)
        return temp_c, temp_f

try:
    while True:
        try:
            c, f = read_temp(thermometer)
            print(thermometer + ': ' + str(f), flush=True)
        except Exception as error:
            c = None
            f = None
            print('Error reading thermometer ' + thermometer + ': ' + str(error), flush=True)

        time.sleep(1)

except KeyboardInterrupt:
    print('completed successfully.')
