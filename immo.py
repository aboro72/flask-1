from bs4 import BeautifulSoup
import requests
from pandasgui import show
from pandasgui.datasets import titanic
import pandas as pd
import urllib.parse


def crawler():
    titel = []
    quadratmeter = []
    zimmer = []
    miete = []
    beschreibung = []
    lage = []
    Vermieter = []

    for i in range(1, 79):
        seite = 'https://www.immonet.de/nordrhein-westfalen/rhein-erft-kreis-bergheim-bergheim-wohnung-mieten-seite' + \
                str(i) + '.html'

        # HTTP requets
        response = requests.get(seite)

        # Soup Object
        soup = BeautifulSoup(response.content, 'html.parser')

        # Container mit 23 Ergebnissen
        results_container = soup.find_all('div', {'class': 'cursor-hand'})

        # url_part1
        url_part1 = 'https://www.immonet.de'

        # url_part2 (leere Liste)
        url_part2 = []

        for item in results_container:
            for link in item.find_all('a', {'class': 'text-225'}):
                url_part2.append(link.get('href'))

        url_joined = []

        for i1 in url_part2:
            url_joined.append(urllib.parse.urljoin(url_part1, i1))

        for link in url_joined:

            # HTTP requets zu jeden Link aus der "url_joined" Liste
            response = requests.get(link)

            # Soup Object
            soup = BeautifulSoup(response.content, 'html.parser')

            # Titel
            try:
                titel.append(soup.find('h1').get_text().strip())

            except:
                titel.append('')

            # quadratmeter
            try:
                quadratmeter.append(soup.find('span', {'id': 'kffirstareaValue'}).get_text().strip().replace('\xa0', ' '))

            except:
                quadratmeter.append('')

            # Zimmer
            try:
                zimmer.append(soup.find('span', {'id': 'kfroomsValue'}).get_text().strip())

            except:
                zimmer.append('')

            # Miete
            try:
                miete.append(soup.find('span', {'id': 'kfpriceValue'}).get_text().strip().replace('\xa0', ' '))

            except:
                miete.append('')

            # Vermieter
            try:
                firma = soup.find('span', {'id': 'bdBrokerFirmname'}).get_text().strip()
                makler = soup.find('p', {'id': 'bdBrokerName'}).get_text().strip()
                f_strasse = soup.find('p', {'id': 'bdBrokerStreet'}).get_text().strip()
                f_ort = soup.find('p', {'id': 'bdBrokerZipCity'}).get_text().strip()
                f_all = firma + ' ' + makler + ' ' + f_strasse + ' ' + f_ort
                Vermieter.append(f_all)

            except:
                Vermieter.append('')

            # beschreibung
            try:
                beschreibung.append(soup.find('p', {'id': 'objectDescription'}).get_text())

            except:
                beschreibung.append('')

                # Lage
            try:
                lage.append(soup.find('p', {'id': 'locationDescription'}).get_text())

            except:
                lage.append('')

    immo = pd.DataFrame({'Objekt': titel, 'Quadratmeter': quadratmeter, 'Zimmer': zimmer, 'Miete': miete,
                         'Beschreibung': beschreibung, 'Lage': lage, 'Ansprechpartner': Vermieter})

    return immo


crawler()

