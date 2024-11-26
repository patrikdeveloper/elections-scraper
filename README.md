# Engeto-projekt
Třetí projekt na Python akademii od engeta.
## Popis projektu
Tento projekt slouží k extrahování volebních výsledků v roce 2017.
## Instalace knihoven
Použité knihovny jsou uloženy v souboru requirements.txt

Postup
1. Naklonujte projekt z GitHubu.
2. Aktivujte virtuální prostředí.
3. Nainstalujte závislosti:
pip install -r requirements.txt
## Spuštění projektu
Spuštění souboru elections_scraper.py v rámci příkazového řádku vyžaduje dva povinné argumenty.

python elections_scraper <odkaz-uzemního-celku> <vysledny-soubor>

Následně se vám stáhnou výsledky jako soubor s příponou .csv

## Ukázka projektu

Výsledky hlasování pro okres Prostějov:

1.argument: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103
2.argument: vysledky_prostejov.csv

### Spuštění programu

python elections_scraper.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" "vysledky_prostejov.csv"

Průběh stahování:

STAHUJI DATA Z VYBRANEHO URL: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103
UKLADAM DO SOUBORU: vysledky_prostejov.csv
UKONCUJI elections_scraper

Částečný výstup:

code,location,registered,envelopes,valid,...
506761,Alojzov,205,145,144,29,0,0,9,0,5,17,4,1,1,0,0,18,0,5,32,0,0,6,0,0,1,1,15,0
589268,Bedihošť,834,527,524,51,0,0,28,1,13,123,2,2,14,1,0,34,0,6,140,0,0,26,0,0,0,0,82,1
589276,Bílovice-Lutotín,431,279,275,13,0,0,32,0,8,40,1,0,4,0,0,30,0,3,83,0,0,22,0,0,0,1,38,0
...