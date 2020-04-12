#!/usr/bin/env python3
import minimalmodbus
import datetime
import mysql.connector

# -*- coding: utf8mb4_general_ci -*-

## Portin osoite
instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 4)

instrument.serial.port
instrument.serial.baudrate = 9600
#instrument.serial.bytesize = 8
#instrument.serial.parity   = PARITY_NONE
#instrument.serial.stopbits = 1
instrument.serial.timeout  = 5

## Alustetaan mysql yhteys
mydb = mysql.connector.connect(
  host="192.168.x.x",
  user="käyttäjätunnus",
  passwd="salasana",
  database="talologgerdb"
)

## Luetaan halutut arvot
#h279 = instrument.read_register(279) # Year
#h280 = instrument.read_register(280) # Month
#h281 = instrument.read_register(281) # Day
h282 = instrument.read_register(282)
h283 = instrument.read_register(283)
h286 = instrument.read_register(286)
h287 = instrument.read_register(287)
h292 = instrument.read_register(292)
h293 = instrument.read_register(293)
h296 = instrument.read_register(296)
h297 = instrument.read_register(297)

## Lasketaan arvot
copheat = (round((h292 + h293/100)/(h282 + h283/100) ,2))
copdhw = (round((h296 + h297/100)/(h286 + h287/100) ,2))
heatcons = (round((h282 + h283/100) ,2))
heatprod = (round((h292 + h293/100) ,2))
dhwcons = (round((h286 + h287/100) ,2))
dhwprod = (round((h296 + h297/100) ,2))

## Kerrotan että now on edellispäivä
now = datetime.datetime.now() - datetime.timedelta(days=1)

## Jos halutaan vain tulostaa arvot:
#print("Last Measured DHW Energy Consumption – kWh part:", (h286))

## Jos halutaan tallentaa arvot tiedostoon:
## Valmistellaan tiedosto
#with open('cop.txt', 'a') as f:
## Tulostusjärjestys: pvm copheat copdhw heatconsumption heatproduced dhwconsumption dhwproduced year month day
#    print ((now.strftime("%Y-%m-%d")), (round((h292 + h293/100)/(h282 + h283/100) ,2)), (round((h296 + h297/100)/(h286 + h287/100) ,2)), (h282 + h283/100), (h292 + h293/100), (h286 + h287/100), (h296 + h297/100), (h279), (h280), (h281), file=f)  # Tallennetaan tiedostoon

## Tallennetaan tiedot TaloLoggerin kantaan
mycursor = mydb.cursor()
sql = "INSERT INTO talo_data (time, position_id, value) VALUES (%s, %s, %s)"
val = [
  ((now.strftime("%Y-%m-%d")), '52', (copheat)),
  ((now.strftime("%Y-%m-%d")), '53', (copdhw)),
  ((now.strftime("%Y-%m-%d")), '54', (heatcons)),
  ((now.strftime("%Y-%m-%d")), '55', (heatprod)),
  ((now.strftime("%Y-%m-%d")), '56', (dhwcons)),
  ((now.strftime("%Y-%m-%d")), '57', (dhwprod)),
]

mycursor.executemany(sql, val)

mydb.commit()
