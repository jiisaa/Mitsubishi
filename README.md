# Mitsubishi Ecodan

Mitsubishi Ecodan modbus dataloggausta Talologgerin avulla sekä simppelit koodit mitä voidaan ajaa esim. Crontabilla ja lähettää hälyjä suoraan Mitsulta modbus väylän tai tietokannan kautta luetuista arvoista sähköpostiin.

cop.py laskee Mitsulta saatujen tietojen perusteella lämmitys ja käyttöveden päivittäisen COP:n ja tallentaa sen samaan kantaan TaloLoggerin muiden mittausten joukkoon Crontabilla ajastettuna päivittäin puolenyön jälkeen.

ftc.py ohjaa Mitsun lämpökäyrää halutun hystereesin avulla lennosta Modbusväylän kautta.
