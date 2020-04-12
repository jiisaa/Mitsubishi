#!/usr/bin/env python3

## Luetaan tiedot MySQL kannasta ja tuloksen perusteella
## joko lähetetään sähköpostiin viesti tai ei tehdä mitään

import smtplib
import mysql.connector

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

## Alustetaan mysql yhteys
mydb = mysql.connector.connect(
  host="192.168.x.x",
  user="talologger",
  passwd="Salasana",
  database="talologgerdb"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT value FROM `talo_data` WHERE position_id = 41 ORDER BY `id` DESC LIMIT 0,1")

myresult = mycursor.fetchone()

res = myresult[0]/100

## Jos arvo on yli 38 lähetetään sähköpostiin ilmoitus
if res > 38:

## Määritetään lähettäjä ja vastaanottoja
    me = "Lähettäjä"
    you = "Vastaanottaja"

## Alustetaan postin lähetys
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Mitsun valvontahäly"
    msg['From'] = me
    msg['To'] = you

## Sähköpstin sisältö, tekstinä ja HTML versiona.
    text = "Hei!\n\nMIME viestit eivät ole tuottuja."
    html = """\
    <html>
      <head></head>
      <body>
        <h2>Toimintahäiriö!</h2><br>
          <p>Menoveden lämpötila on nyt {res} °C
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
    print("Menoveden lämpötila on ok:", (res) ,"°C")
