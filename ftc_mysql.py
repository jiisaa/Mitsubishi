#!/usr/bin/env python3
import time
import minimalmodbus
import datetime
import mysql.connector
from datetime import datetime

## Settings for mysql connection
mydb = mysql.connector.connect(
  host="a.b.c.d",
  user="DatabaseUsername",
  passwd="DatabasePWD",
  database="DatabaseName"
)

## Read Settings

## Maximum Flow Temperature
mycursor = mydb.cursor()
mycursor.execute("SELECT value FROM mitsubishi WHERE id = 2")
myresultset1 = mycursor.fetchone()
set1 = int(myresultset1[0])

## Minimum Flow Temperature
mycursor = mydb.cursor()
mycursor.execute("SELECT value FROM mitsubishi WHERE id = 3")
myresultset2 = mycursor.fetchone()
set2 = int(myresultset2[0])

## Lowest temperature after change to fixed flow temperature -> Allows heat pump to rise power by it's own software
mycursor = mydb.cursor()
mycursor.execute("SELECT value FROM mitsubishi WHERE id = 4")
myresultset3 = mycursor.fetchone()
set3 = int(myresultset3[0])

## Heat temperature curve 0
mycursor = mydb.cursor()
mycursor.execute("SELECT value FROM mitsubishi WHERE id = 7")
myresultset5 = mycursor.fetchone()
res20 = int(myresultset5[0])

## Heat temperature curve 10
mycursor = mydb.cursor()
mycursor.execute("SELECT value FROM mitsubishi WHERE id = 8")
myresultset6 = mycursor.fetchone()
res21 = int(myresultset6[0])

## Heat temperature curve 20
mycursor = mydb.cursor()
mycursor.execute("SELECT value FROM mitsubishi WHERE id = 9")
myresultset7 = mycursor.fetchone()
res22 = int(myresultset7[0])

## Heat temperature curve 30
mycursor = mydb.cursor()
mycursor.execute("SELECT value FROM mitsubishi WHERE id = 10")
myresultset8 = mycursor.fetchone()
res23 = int(myresultset8[0])

## Read sensors status

## Operating mode, 2=Heating, 1=Hot Water, 0=Stop
mycursor = mydb.cursor()
mycursor.execute("SELECT value FROM talo_data WHERE position_id = 49 AND value IS NOT NULL ORDER BY id DESC LIMIT 0,1")
myresult5 = mycursor.fetchone()
res1 = int(myresult5[0])

## Flow Temperature Setpoint – Zone 1
mycursor = mydb.cursor()
mycursor.execute("SELECT value FROM talo_data WHERE position_id = 51 AND value IS NOT NULL ORDER BY id DESC LIMIT 0,1")
myresult6 = mycursor.fetchone()
res2 = int(myresult6[0])

## Defrost 0=Normal, 2=Defrost
mycursor = mydb.cursor()
mycursor.execute("SELECT value FROM talo_data WHERE position_id = 50 AND value IS NOT NULL ORDER BY id DESC LIMIT 0,1")
myresult7 = mycursor.fetchone()
res3 = int(myresult7[0])

## Flow Temperature – Zone 1 (signed) (THW6)
mycursor = mydb.cursor()
mycursor.execute("SELECT value FROM talo_data WHERE position_id = 46 AND value IS NOT NULL ORDER BY id DESC LIMIT 0,1")
myresult8 = mycursor.fetchone()
res4 = int(myresult8[0])

## Outdoor Ambient Temperature (Read 60 min average without values in time of defrosting)
mycursor = mydb.cursor()
mycursor.execute("SELECT AVG(a.value) FROM talo_data a WHERE a.position_id = 44 AND time >= NOW() - INTERVAL 60 MINUTE AND EXISTS (SELECT 1 FROM talo_data b WHERE b.id > a.id AND a.time = b.time AND b.position_id = 50 AND time >= NOW() - INTERVAL 60 MINUTE AND (b.value = 0 OR b.value <> 2))")
myresult9 = mycursor.fetchone()
res5 = int(myresult9[0])

## Before last Operating mode, 2=Heating, 1=Hot Water, 0=Stop
mycursor = mydb.cursor()
mycursor.execute("SELECT value FROM talo_data WHERE position_id = 49 AND value IS NOT NULL ORDER BY id DESC LIMIT 2,1")
myresult10 = mycursor.fetchone()
res6 = int(myresult10[0])

mycursor.close()
mydb.close()

instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 4)  # port name, slave address (in decimal)

## Setup serial port ##
instrument.serial.port
instrument.serial.baudrate = 9600
instrument.serial.timeout  = 5

## Target temp change 0,5c below Flow Temp, or 25c if already at minimum level
#tt = res4 - 50 if res4 >= 2550 else 2500
tt = res4 if res4 >= 2500 else 2500
temp = res5 / 10

## If logging needed, if not, # also all print functions
now = datetime.now()
with open('log.txt', 'a') as f:

## If Operating mode is Hot Water
  if res1 == 1:

## If Operating mode was Heating
    if res6 == 2:
      if res2 < set1 + 300:
        instrument.write_register(32, (res2 + 300), functioncode=6)
        print(now.strftime("%d/%m/%Y %H:%M:%S"),"Operating mode was Hot Water before Heating, change Flow temp 5c higher to ",(res2 + 300), file=f)
    else:
      print(now.strftime("%d/%m/%Y %H:%M:%S"),"Operating mode Hot Water, Flow temp rised already, wait for Heat mode", file=f)
      time.sleep(120)

## If Heating is on, target temp over max temp because change after Hot water, first set flow temp 0.5c below Flow Temp wait and set Flow Temp to max set
  elif res1 == 2 and tt != res2 and res2 > set1 and res3 == 0:
    time.sleep(60)
    res2 = res2 - 100
    instrument.write_register(32, (tt), functioncode=6)
    print(now.strftime("%d/%m/%Y %H:%M:%S"),"New Flow Temperature after DHW 1 = ", (tt), file=f)
    time.sleep(300)

    if res2 > set1:
      instrument.write_register(32, (tt - 100), functioncode=6)
      print(now.strftime("%d/%m/%Y %H:%M:%S"),"New Flow Temperature after DHW 2 = ", (tt-100), file=f)
      time.sleep(300)
      res2 = res2 - 100

      if res2 > set1:
        instrument.write_register(32, (tt - 200), functioncode=6)
        print(now.strftime("%d/%m/%Y %H:%M:%S"),"New Flow Temperature after DHW 3 = ", (tt-200), file=f)
        time.sleep(300)
        res2 = res2 - 100

        if res2 > set1:
          instrument.write_register(32, (tt - 300), functioncode=6)
          print(now.strftime("%d/%m/%Y %H:%M:%S"),"New Flow Temperature after DHW 4 = ", (tt-300), file=f)
          time.sleep(300)
          res2 = res2 - 100

          if res2 > set1:
            instrument.write_register(32, (tt - 400), functioncode=6)
            print(now.strftime("%d/%m/%Y %H:%M:%S"),"New Flow Temperature after DHW 5 = ", (tt-400), file=f)
            time.sleep(300)
            res2 = res2 - 100

            if res2 > set1:
              instrument.write_register(32, (tt - 500), functioncode=6)
              print(now.strftime("%d/%m/%Y %H:%M:%S"),"New Flow Temperature after DHW 6 = ", (tt-500), file=f)

            else:
              instrument.write_register(32, (set1 - 100), functioncode=6)
              print(now.strftime("%d/%m/%Y %H:%M:%S"),"New Flow Temperature after DHW 7 = ", (tt), file=f)

          else:
            instrument.write_register(32, (set1 - 100), functioncode=6)
            print(now.strftime("%d/%m/%Y %H:%M:%S"),"New Flow Temperature after DHW 8 = ", (tt), file=f)

        else:
          instrument.write_register(32, (set1 - 100), functioncode=6)
          print(now.strftime("%d/%m/%Y %H:%M:%S"),"New Flow Temperature after DHW 9 = ", (tt), file=f)

      else:
        instrument.write_register(32, (set1 - 100), functioncode=6)
        print(now.strftime("%d/%m/%Y %H:%M:%S"),"New Flow Temperature after DHW 10 = ", (tt), file=f)

    else:
      instrument.write_register(32, (set1 - 100), functioncode=6)
      print(now.strftime("%d/%m/%Y %H:%M:%S"),"New Flow Temperature after DHW 11 = ", (tt), file=f)

## If Defrosting, wait for heating to start and wait little longer to prevent system to step down Flow Temp setpoint and stop heating due to too high Flow Temp.
  elif res3 == 2:
    print(now.strftime("%d/%m/%Y %H:%M:%S"),"Defrosting, waiting for heating to start ", file=f)
    time.sleep(420)

## If outdoor temp below minimum outdoor temp set to enter Flow Temp Curve
  elif temp < set3:

## We go to Flow Temp Curve and depending of outdoor temp and settings we change flow temp to suite requirements
    if temp <= 0 and temp > -1:
      tt = res20
      if tt != res2:
        instrument.write_register(32, (tt), functioncode=6)
        print(now.strftime("%d/%m/%Y %H:%M:%S"),"Outdoor 0C, Target temp = ", (tt), file=f)

    if temp <= -1 and temp > -2:
      tt2 = round(((res21 - res20) / 10 + res20)/100*2)/2
      tt = tt2 * 100
      if tt != res2:
        instrument.write_register(32, (tt), functioncode=6)
        print(now.strftime("%d/%m/%Y %H:%M:%S"),"Outdoor 1C, Target temp = ", (tt), file=f)

    if temp <= -2 and temp > -3:
      tt2 = round(((res21 - res20) / 10 * 2 + res20)/100*2)/2
      tt = tt2 * 100
      if tt != res2:
        instrument.write_register(32, (tt), functioncode=6)
        print(now.strftime("%d/%m/%Y %H:%M:%S"),"Outdoor 2C, Target temp = ", (tt), file=f)

    if temp <= -3 and temp > -4:
      tt2 = round(((res21 - res20) / 10 * 3 + res20)/100*2)/2
      tt = tt2 * 100
      if tt != res2:
        instrument.write_register(32, (tt), functioncode=6)
        print(now.strftime("%d/%m/%Y %H:%M:%S"),"Outdoor 3C, Target temp = ", (tt), file=f)

    if temp <= -4 and temp > -5:
      tt2 = round(((res21 - res20) / 10 * 4 + res20)/100*2)/2
      tt = tt2 * 100
      if tt != res2:
        instrument.write_register(32, (tt), functioncode=6)
        print(now.strftime("%d/%m/%Y %H:%M:%S"),"Outdoor 4C, Target temp = ", (tt), file=f)

    if temp <= -5 and temp > -6:
      tt2 = round(((res21 - res20) / 10 * 5 + res20)/100*2)/2
      tt = tt2 * 100
      if tt != res2:
        instrument.write_register(32, (tt), functioncode=6)
        print(now.strftime("%d/%m/%Y %H:%M:%S"),"Outdoor 5C, Target temp = ", (tt), file=f)

    if temp <= -6 and temp > -7:
      tt2 = round(((res21 - res20) / 10 * 6 + res20)/100*2)/2
      tt = tt2 * 100
      if tt != res2:
        instrument.write_register(32, (tt), functioncode=6)
        print(now.strftime("%d/%m/%Y %H:%M:%S"),"Outdoor 6C, Target temp = ", (tt), file=f)

    if temp <= -7 and temp > -8:
      tt2 = round(((res21 - res20) / 10 * 7 + res20)/100*2)/2
      tt = tt2 * 100
      if tt != res2:
        instrument.write_register(32, (tt), functioncode=6)
        print(now.strftime("%d/%m/%Y %H:%M:%S"),"Outdoor 7C, Target temp = ", (tt), file=f)

    if temp <= -8 and temp > -9:
      tt2 = round(((res21 - res20) / 10 * 8 + res20)/100*2)/2
      tt = tt2 * 100
      if tt != res2:
        instrument.write_register(32, (tt), functioncode=6)
        print(now.strftime("%d/%m/%Y %H:%M:%S"),"Outdoor 8C, Target temp = ", (tt), file=f)

    if temp <= -9 and temp > -10:
      tt2 = round(((res21  - res20) / 10 * 9 + res20)/100*2)/2
      tt = tt2 * 100
      if tt != res2:
        instrument.write_register(32, (tt), functioncode=6)
        print(now.strftime("%d/%m/%Y %H:%M:%S"),"Outdoor 9C, Target temp = ", (tt), file=f)

    if temp <= -10 and temp > -11:
      tt = res21
      if tt != res2:
        instrument.write_register(32, (tt), functioncode=6)
        print(now.strftime("%d/%m/%Y %H:%M:%S"),"Outdoor 10C, Target temp = ", (tt), file=f)

    if temp <= -11 and temp > -12:
      tt2 = round(((res22 - res21) / 10 + res21)/100*2)/2
      tt = tt2 * 100
      if tt != res2:
        instrument.write_register(32, (tt), functioncode=6)
        print(now.strftime("%d/%m/%Y %H:%M:%S"),"Outdoor 11C, Target temp = ", (tt), file=f)

    if temp <= -12 and temp > -13:
      tt2 = round(((res22 - res21) / 10 * 2 + res21)/100*2)/2
      tt = tt2 * 100
      if tt != res2:
        instrument.write_register(32, (tt), functioncode=6)
        print(now.strftime("%d/%m/%Y %H:%M:%S"),"Outdoor 12C, Target temp = ", (tt), file=f)

    if temp <= -13 and temp > -14:
      tt2 = round(((res22 - res21) / 10 * 3 + res21)/100*2)/2
      tt = tt2 * 100
      if tt != res2:
        instrument.write_register(32, (tt), functioncode=6)
        print(now.strftime("%d/%m/%Y %H:%M:%S"),"Outdoor 13C, Target temp = ", (tt), file=f)

    if temp <= -14 and temp > -15:
      tt2 = round(((res22 - res21) / 10 * 4 + res21)/100*2)/2
      tt = tt2 * 100
      if tt != res2:
        instrument.write_register(32, (tt), functioncode=6)
        print(now.strftime("%d/%m/%Y %H:%M:%S"),"Outdoor 14C, Target temp = ", (tt), file=f)

    if temp <= -15 and temp > -16:
      tt2 = round(((res22 - res21) / 10 * 5 + res21)/100*2)/2
      tt = tt2 * 100
      if tt != res2:
        instrument.write_register(32, (tt), functioncode=6)
        print(now.strftime("%d/%m/%Y %H:%M:%S"),"Outdoor 15C, Target temp = ", (tt), file=f)

    if temp <= -16 and temp > -17:
      tt2 = round(((res22 - res21) / 10 * 6 + res21)/100*2)/2
      tt = tt2 * 100
      if tt != res2:
        instrument.write_register(32, (tt), functioncode=6)
        print(now.strftime("%d/%m/%Y %H:%M:%S"),"Outdoor 16C, Target temp = ", (tt), file=f)

    if temp <= -17 and temp > -18:
      tt2 = round(((res22 - res21) / 10 * 7 + res21)/100*2)/2
      tt = tt2 * 100
      if tt != res2:
        instrument.write_register(32, (tt), functioncode=6)
        print(now.strftime("%d/%m/%Y %H:%M:%S"),"Outdoor 17C, Target temp = ", (tt), file=f)

    if temp <= -18 and temp > -19:
      tt2 = round(((res22 - res21) / 10 * 8 + res21)/100*2)/2
      tt = tt2 * 100
      if tt != res2:
        instrument.write_register(32, (tt), functioncode=6)
        print(now.strftime("%d/%m/%Y %H:%M:%S"),"Outdoor 18C, Target temp = ", (tt), file=f)

    if temp <= -19 and temp > -20:
      tt2 = round(((res22 - res21) / 10 * 9 + res21)/100*2)/2
      tt = tt2 * 100
      if tt != res2:
        instrument.write_register(32, (tt), functioncode=6)
        print(now.strftime("%d/%m/%Y %H:%M:%S"),"Outdoor 19C, Target temp = ", (tt), file=f)

    if temp <= -20 and temp > -21:
      tt = res22
      if tt != res2:
        instrument.write_register(32, (tt), functioncode=6)
        print(now.strftime("%d/%m/%Y %H:%M:%S"),"Outdoor 20C, Target temp = ", (tt), file=f)

    if temp <= -21 and temp > -22:
      tt2 = round(((res23 - res22) / 10 + res22)/100*2)/2
      tt = tt2 * 100
      if tt != res2:
        instrument.write_register(32, (tt), functioncode=6)
        print(now.strftime("%d/%m/%Y %H:%M:%S"),"Outdoor 21C, Target temp = ", (tt), file=f)

    if temp <= -22 and temp > -23:
      tt2 = round(((res23 - res22) / 10 * 2 + res22)/100*2)/2
      tt = tt2 * 100
      if tt != res2:
        instrument.write_register(32, (tt), functioncode=6)
        print(now.strftime("%d/%m/%Y %H:%M:%S"),"Outdoor 22C, Target temp = ", (tt), file=f)

    if temp <= -23 and temp > -24:
      tt2 = round(((res23 - res22) / 10 * 3 + res22)/100*2)/2
      tt = tt2 * 100
      if tt != res2:
        instrument.write_register(32, (tt), functioncode=6)
        print(now.strftime("%d/%m/%Y %H:%M:%S"),"Outdoor 23C, Target temp = ", (tt), file=f)

    if temp <= -24 and temp > -25:
      tt2 = round(((res23 - res22) / 10 * 4 + res22)/100*2)/2
      tt = tt2 * 100
      if tt != res2:
        instrument.write_register(32, (tt), functioncode=6)
        print(now.strftime("%d/%m/%Y %H:%M:%S"),"Outdoor 24C, Target temp = ", (tt), file=f)

    if temp <= -25 and temp > -26:
      tt2 = round(((res23 - res22) / 10 * 5 + res22)/100*2)/2
      tt = tt2 * 100
      if tt != res2:
        instrument.write_register(32, (tt), functioncode=6)
        print(now.strftime("%d/%m/%Y %H:%M:%S"),"Outdoor 25C, Target temp = ", (tt), file=f)

    if temp <= -26 and temp > -27:
      tt2 = round(((res23 - res22) / 10 * 6 + res22)/100*2)/2
      tt = tt2 * 100
      if tt != res2:
        instrument.write_register(32, (tt), functioncode=6)
        print(now.strftime("%d/%m/%Y %H:%M:%S"),"Outdoor 26C, Target temp = ", (tt), file=f)

    if temp <= -27 and temp > -28:
      tt2 = round(((res23 - res22) / 10 * 7 + res22)/100*2)/2
      tt = tt2 * 100
      if tt != res2:
        instrument.write_register(32, (tt), functioncode=6)
        print(now.strftime("%d/%m/%Y %H:%M:%S"),"Outdoor 27C, Target temp = ", (tt), file=f)

    if temp <= -28 and temp > -29:
      tt2 = round(((res23 - res22) / 10 * 8 + res22)/100*2)/2
      tt = tt2 * 100
      if tt != res2:
        instrument.write_register(32, (tt), functioncode=6)
        print(now.strftime("%d/%m/%Y %H:%M:%S"),"Outdoor 28C, Target temp = ", (tt), file=f)

    if temp <= -29 and temp > -30:
      tt2 = round(((res23 - res22) / 10 * 9 + res22)/100*2)/2
      tt = tt2 * 100
      if tt != res2:
        instrument.write_register(32, (tt), functioncode=6)
        print(now.strftime("%d/%m/%Y %H:%M:%S"),"Outdoor 29C, Target temp = ", (tt), file=f)

    if temp <= -30:
      tt = res23
      if tt != res2:
        instrument.write_register(32, (tt), functioncode=6)
        print(now.strftime("%d/%m/%Y %H:%M:%S"),"Outdoor 30C, Target temp = ", (tt), file=f)

## If Heating is on, target temp not same already set, we are not going over decided Flow Temp limit, Defrosting is off (Normal) and Heating is On, set Flow Temp to new Target temp, tt
  elif res1 == 2 and tt != res2 and tt < (set1-100) and res3 == 0:
    instrument.write_register(32, tt, functioncode=6)
    print(now.strftime("%d/%m/%Y %H:%M:%S"),"New Flow Temperature 1 = ", (tt), file=f)

## If Heating is off and Defrosting is off (Normal) we think system has reached maximum set temp and system has turn off heating and is waiting for hysteresis to go down, set Flow temp to min
  elif res1 == 0 and res3 != 2 and res2 != set2:
    instrument.write_register(32, set2, functioncode=6)
    print(now.strftime("%d/%m/%Y %H:%M:%S"),"Heating off, New Flow Temperature = ", (set2), file=f)

## Else end program...
  else:
    print("No need to change settings...")
