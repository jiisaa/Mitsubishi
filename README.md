# Mitsubishi
Mitsubishi Ecodan data logging

Mitsubishin dataloggausta Talologgerin avulla sekä simppelit koodit mitä voidaan ajaa esim. Crontabilla ja lähettää hälyjä suoraan Mitsulta modbus väylän tai tietokannan kautta luetuista arvoista.

cop.py laskee Mtsulta saatujen tietojen perusteella lämmitys ja käyttöveden päivittäisen COP:n ja tallentaa sen samaan kantaan Talologgerin muiden mittauksen joukkoon.
