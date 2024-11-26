"""
elections_scraper.py: třetí projekt do Engeto Online Python Akademie

author: Patrik Hlaváč
email: pathlavac@seznam.cz
discord: patrik_py
"""
import requests
from bs4 import BeautifulSoup
import re
import csv
import sys
import argparse

"""
Election Data Scraper

Tento skript stahuje a analyzuje volební data z daného URL a ukládá je do CSV souboru. 
Používá knihovny `requests`, `BeautifulSoup`, `csv` a `argparse` pro zpracování HTML, správu HTTP požadavků 
a manipulaci se soubory CSV. 

Skript očekává dva argumenty: 
1. URL stránky s daty (např. https://www.volby.cz)
2. Název výstupního CSV souboru.

Funkce:
- `get_urls(main_url)`: Získá seznam URL pro jednotlivé volební obce.
- `get_name_of_village(url)`: Získá názvy obcí z daného URL.
- `get_code_of_village(url)`: Získá kódy obcí z daného URL.
- `get_valid_party_votes(url)`: Získá hlasy jednotlivých stran z daného URL.
- `get_party_name(url)`: Získá názvy stran z daného URL.
- `main()`: Hlavní funkce pro řízení celého procesu (scraping a zápis do CSV).

Použití:
    python elections_scraper.py <URL> <soubor.csv>
"""
def get_urls(main_url):
    """
    Získá seznam URL jednotlivých volebních obcí z hlavní stránky.

    Args:
        main_url (str): URL hlavní stránky obsahující odkazy na volební obce.

    Returns:
        list: Seznam URL (str) jednotlivých volebních obcí.
    """
    response = requests.get(main_url)
    links = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        tables = soup.find_all("table")

        for table in tables:
            rows = table.find_all("a")
            for link in rows:
                text = link.get_text()
                if re.match(r'^\d{6}$', text):
                    href = link.get('href')
                    if href:
                        full_url = f"https://www.volby.cz/pls/ps2017nss/{href}"
                        links.append(full_url)
    else:
        print(f"Chyba při stahování hlavní stránky: {main_url}")
    return links

def get_name_of_village(url):
    """
    Získá seznam názvů obcí z daného URL.

    Args:
        url (str): URL stránky s informacemi o obcích.

    Returns:
        list: Seznam názvů obcí (str).
    """
    response = requests.get(url)
    village = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        rows = soup.find_all("tr")

        for row in rows:
            cells = row.find_all("td")
            if len(cells) > 1:
                village_name = cells[1].get_text(strip=True)
                if village_name and village_name != "-":
                    village.append(village_name)
    return village

def get_code_of_village(url):
    """
    Získá seznam kódů obcí z daného URL.

    Args:
        url (str): URL stránky s informacemi o obcích.

    Returns:
        list: Seznam kódů obcí (str).
    """
    response = requests.get(url)
    code_of_village = []
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        rows = soup.find_all("tr")

        for row in rows:
            cells = row.find_all("td")
            if len(cells) > 0:
                code = cells[0].get_text(strip=True)
                if code and code != "-":
                    code_of_village.append(code)
    return code_of_village

def get_valid_party_votes(url):
    """
    Získá hlasy jednotlivých stran z daného URL.

    Args:
        url (str): URL stránky s volebními výsledky.

    Returns:
        list of tuples: Seznam dvojic (strana, hlasy), kde:
            - strana (str): Název politické strany.
            - hlasy (str): Počet platných hlasů.
    """
    valid_votes_party = []
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        tables = soup.find_all("table")
        
        for table in tables[1:3]:
            rows = table.find_all("tr")
            for row in rows:
                cells = row.find_all("td")
                if len(cells) > 1:
                    party_name = cells[1].get_text(strip=True)
                    if party_name != "-" and party_name != "":
                        votes = cells[2].get_text(strip=True)
                        valid_votes_party.append((party_name, votes))
    
    return valid_votes_party

def get_party_name(url):
    """
    Získá názvy stran z daného URL.

    Args:
        url (str): URL stránky s informacemi o stranách.

    Returns:
        list: Seznam názvů politických stran (str).
    """
    response = requests.get(url)
    party_name = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        rows = soup.find_all("tr")

        for row in rows:
            cells = row.find_all("td")
            if len(cells) > 1:
                code = cells[1].get_text(strip=True)
                if code and code != "-" and code != "1":
                    party_name.append(code)
    return party_name
    
def main():
    """
    Hlavní funkce programu. Spravuje scraping a zápis dat do CSV.

    Provádí následující kroky:
    1. Získá seznam URL jednotlivých volebních obcí.
    2. Stáhne data o obcích, kódech obcí, voličích, obálkách a hlasech stran.
    3. Zapíše získaná data do CSV souboru.

    Args:
        None

    Returns:
        None
    """
     # Nastavení argumentů pomocí argparse
    parser = argparse.ArgumentParser(description="Scrape election data and save to CSV.")
    parser.add_argument('url', type=str, help='URL adresa stránky pro stahování dat')
    parser.add_argument('csv_output', type=str, help='Název výstupního CSV souboru')

    args = parser.parse_args()

    # Oznámení o začátku stahování dat
    print(f"STAHUJI DATA Z VYBRANEHO URL: {args.url}")

    # Načítání dat zadaného URL
    urls = get_urls(args.url)
    
    if not urls:
        print("Nebyla nalezena žádná data k dané URL. Zkontrolujte vstupní adresu.")
        sys.exit(1)
    
    party_name = get_party_name(urls[0])
    village = get_name_of_village(args.url)
    code_of_village = get_code_of_village(args.url)
    envelop = []
    electors = []
    valid_votes_total = []

    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            table = soup.find("table")
            rows = table.find_all("tr")

            for row in rows:
                cells = row.find_all("td")
                if len(cells) > 4:
                    envelop.append(cells[4].get_text(strip=True).replace("\xa0", " "))
                    
                if len(cells) > 3:
                    electors.append(cells[3].get_text(strip=True).replace("\xa0", " "))
                    
                if len(cells) > 7:
                    valid_votes_total.append(cells[7].get_text(strip=True).replace("\xa0", " "))

    # Zápis do CSV souboru
    print("UKLADAM DO SOUBORU:", args.csv_output)
    with open(args.csv_output, 'w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        
        # Zapsání hlavičky CSV 
        csvwriter.writerow(["code", "location", "registered", "envelopes", "valid", *party_name])
        
        for i, url in enumerate(urls):
            valid_votes = get_valid_party_votes(url)
            votes_dict = {party: "0" for party in party_name}
            for party, votes in valid_votes:
                votes_dict[party] = votes
            row = [code_of_village[i], village[i], electors[i], envelop[i], valid_votes_total[i]] + [votes_dict[party] for party in party_name]
            csvwriter.writerow(row)
    print("UKONCUJI elections_scraper")

# Spuštění hlavní funkce, pokud je skript spuštěn jako hlavní program
if __name__ == "__main__":
    allowed_url_pattern = r"^https://www\.volby\.cz/pls/ps2017nss/.+$"
    if len(sys.argv) != 3:
        print("Nesprávný počet argumentů. Použijte: python elections_scraper.py <URL> <soubor.csv>")
    else:
        url = sys.argv[1]
        output_file = sys.argv[2]
        if not re.match(allowed_url_pattern, url):
            print(f"Chybný první argument. URL musí odpovídat vzoru: {allowed_url_pattern}")
        elif not output_file.endswith('.csv'):
            print("Chybný druhý argument. Druhý argument musí být název souboru s příponou .csv")
        else:
            main()

