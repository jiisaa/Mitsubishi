#!/usr/bin/env python3
import minimalmodbus

instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 4)  # port name, slave address (in decimal)

## Setup serial port ##
instrument.serial.port
instrument.serial.baudrate = 9600
instrument.serial.timeout  = 5

## Read value ##

## Operating Mode, 2=Heating, 1=Hot Water, 0=Stop
r26 = instrument.read_register(26)

## H/C Thermostat Target Temperature – Zone 1 (signed)
r32 = instrument.read_register(32)

## Defrost 0=Normal, 2=Defrost
r67 = instrument.read_register(67)

## Flow Temperature – Zone 1 (signed)
r107 = instrument.read_register(107)

## Target temp change 0,5c below Flow Temp
tt = r107 - 50

## If Heating is on, target temp not same already set, we are not going over decided Flow Temp (in this case 29C) limit, Defrosting is off (Normal) and Heating is On, set Flow Temp to new Target temp, tt
if r26 == 2 and tt != r32 and tt < 2950 and r67 == 0 and r26 !=0:
  instrument.write_register(32, tt, functioncode=6)
  print("New Flow Temperature set", (tt), "set")

## If Heating is off, Defrosting is off (Normal) and Flow Temp is not 26C already we think system has reached maximum set temp and system has turn off heating and is waiting for hysteresis to go down, set Flow temp to min if not already set
elif r26 == 0 and r67 != 2 and r32 != 2600:
  instrument.write_register(32, 2600, functioncode=6)
  print("Heating off, set Flow Temperature to 26")

## Else end program...
else:
  print("Nothing changed")
