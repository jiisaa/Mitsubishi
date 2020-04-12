#!/usr/bin/env python3

## Luetaan tiedot suoraan Modbus väylästä ja tuloksen
## perusteella joko lähetetään sähköpostiin viesti tai ei tehdä mitään

import smtplib
import minimalmodbus

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

## Portin osoite
instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 4)

instrument.serial.port
instrument.serial.baudrate = 9600
#instrument.serial.bytesize = 8
#instrument.serial.parity   = PARITY_NONE
#instrument.serial.stopbits = 1
instrument.serial.timeout  = 5

## Luetaan halutut arvot
h107 = instrument.read_register(107) ## Flow temperature - Zone 1

## Lasketaan arvo oikeaksi
r107 = h107 / 100

## Jos arvo on yli 38 lähetetään sähköpostiin ilmoitus
if r107 > 38:

## Määritetään lähettäjä ja vastaanottoja
    me = "Lähettäjän osoite"
    you = "Vastaanottajan osoite"

## Alustetaan postin lähetys
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Mitsun valvontahäly"
    msg['From'] = me
    msg['To'] = you

## Sähköpstin sisältö, tekstinä ja HTML versiona.
    text = "Hei!\n\nMIME viestit eivät ole tuettuja."
    html = """\
    <html>
      <head></head>
      <body>
        <h2>Toimintahäiriö!</h2><br>
          <p>Menoveden lämpötila on nyt {r107} °C
          </p>
      </body>
    </html>
    """.format(**locals())

## Tallennetaan viesti lähetettäväksi
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

## Liitetään viesti lähetettäväksi
    msg.attach(part1)
    msg.attach(part2)

## Lähetetään sähköposti
    s = smtplib.SMTP('Operaattorisi lätevän postin palvelin')
    s.sendmail(me, you, msg.as_string())
    s.quit()

## Jos kaikki on ok, tulostetaan vain tiedoksi
else:
    print("Menoveden lämpötila on ok:", (r107) ,"°C")
