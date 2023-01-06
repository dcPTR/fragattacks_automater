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

6. Uruchom automater: 
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
