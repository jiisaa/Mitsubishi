# Mitsubishi Ecodan - Suomeksi

Mitsubishi Ecodan dataloggausta Modbus väylän kautta Talologgerin avulla sekä simppelit koodit mitä voidaan ajaa esim. Crontabilla ja lähettää hälyjä suoraan Mitsulta Modbus väylän tai tietokannan kautta luetuista arvoista sähköpostiin.

cop.py laskee Mitsulta saatujen tietojen perusteella lämmitys ja käyttöveden päivittäisen COP:n ja tallentaa sen samaan kantaan TaloLoggerin muiden mittausten joukkoon Crontabilla ajastettuna päivittäin puolenyön jälkeen.

ftc.py ohjaa Mitsun lämpökäyrää halutun hystereesin avulla lennosta Modbus väylän kautta.

ftc_mysql.py ohjaa Mitsun lämmityspuolta kokonaisuudessaan hyödyntäen MySQL tietokantaa talletettuja arvoja leutoina aikoina välttäen pätkäkäyntiä ja tietyn pisteen jälkeen siirtyen lämpökäyrälle. Vaatii lisäksi myös halutunlaisen web näkymän mistä asetuksia voidaan muokata.

# Mitsubishi Ecodan - English

Mitsubishi Ecodan datalogging through Modbus and Talologger software. Also included simple codes which you can run in Crontab to send alarms using data from either straight from Modbus or from database.

cop.py calculates daily COP for DHW and heating and save that to database.

ftc.py is used to add hysteresis through Modbus.

ftc_mysql.py controls heating in many ways in combination with MySQL database to avoid short cycling when heat power is too much. This requires also web page to control settings for ease of use.
