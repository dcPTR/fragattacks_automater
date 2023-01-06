# fragattacks_automater

1. Pobierz skrypt i skopiuj go do podkatalogu research w katalogu fragattacks.
2. W skrypcie zmien sciezke do katalogu research (komenda `pwd` wyświetla ścieżkę) oraz nazwę interfejsu (komenda `iwconfig`)
3. Przejdz w tryb uprziwilejowany (root) komenda `sudo su`
4. Teraz uruchom środowisko wirtualne: `source venv/bin/activate`
5. (KROK JEDNORAZOWY) Pobierz pyshark komendą: 
```sh
pip3 install pyshark && pip3 install colorama
```
Rowniez moze zajsc potrzeba instalacji TShark:
```sh
apt-get install tshark
```

6. Dodaj siec od routera testowanego do pliku client.conf poprzez dodanie na koniec pliku fragmentu
```py
network={
	ssid="NetworkSSID"
	psk="password"

	pairwise=CCMP
	#group=CCMP

	# Some network cards don't properly support injection on non-20MHz
	# channels. In that case uncomment this line to disable 40 MHz.
	#disable_ht40=1

	# Might be useful in very noisy environments to disable high bitrates.
	#disable_ht=1
}
```
zamieniajac 'NetworkSSID' na SSID sieci z testowanego routera, a 'password' na haslo od niej.

7. Uruchom automater: 
```py
python3 automater.py
```
Opcjonalnie podaj interfejs sieciowy:
```py
python3 automater.py --iface wlan0
```
Opcjonalnie wylacz przechwytywanie pakietow:
```py
python3 automater.py --no-capture
```

Jak edytowac diagram:
1. Pobieramy diagram.vpd z repozytorium.
2. Wchodzimy na strone: https://online.visual-paradigm.com/drive/#infoart:proj=0&dashboard
3. Klikamy IMPORT / OPEN
4. Szukamy "Or open a Visual Paradigm file (.art, .vpd) from:" i wybieramy przycisk "Device"
5. Wybieramy plik do zaimportowania (diagram.vpd).
