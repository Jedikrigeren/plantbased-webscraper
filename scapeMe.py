import string
from unittest import result
from openpyxl import load_workbook
from bs4 import BeautifulSoup

import requests
import re
import mechanize


# TODO: Først løber vi alle id'er igennem fra 1 til 9999

def scrape():
    i = 46548
    NGBnr = ""
    speciesName = ""
    donorAssNr = ""
    breederAssDesig = ""
    species = ""  # TODO SE NOTE I EXCEL
    origin = ""
    NGBRecYear = ""
    NGBRecMonth = ""
    ImporvementSts = ""
    Pedigree = ""
    # Breeder remark, Allele designations (genotype): TODO: Se under source history
    # Accession remark #TODO: Se under Narrative
    # Comments in NGB TODO:
    # Contact curator if interested in SSD material TODO:

    # for i in range(1, 10):
    result = requests.get(
        f"https://nordic-baltic-genebanks.org/gringlobal/accessiondetail.aspx?id={i}")
    src = result.content
    soup = BeautifulSoup(src, features="html5lib")
    resultOfFind = soup.find_all("h1")
    # Find NGB Number for checking
    try:
        NGBnr = resultOfFind[0].text
    except IndexError:
        pass

    # Find Species Name
    result = soup.find(
        id="ctl00_cphBody_plAccessionNames").find_all("th")
    speciesName = result[0].value
    donorAssNr = result[2].value

    result = soup.find(
        id="ctl00_cphBody_plAccessionNames").find_all("td")
    for j in range(len(result)):
        if result[j].text == "Comment:":
            print("succes")
            if result[j-2] == "Designation":
                breederAssDesig = result[j+1]

    result = soup.find(
        id="ctl00_cphBody_plAnnotations").find_all("td")
    speciesName = result[4].text

    result = soup.find(
        "table", {"style": "width:535px; border:1px solid black"}).find_all("td")
    origin = result[0].text

    NGBRecYear = result[2].text[-4:]
    NGBRecMonth = result[2].text[3:6]
    ImporvementSts = result[6]
    Pedigree = result[5]

    # Hvorfor noteres det ikke når Donor assession number = Sortsnavn?


scrape()
exit()


wb = load_workbook(filename='Peas & Love NGB-list.xlsx')
sheet_ranges = wb['Ark1']
cellNr = 1

for sheet in sheet_ranges:
    cellNr += 1
    try:
        NGBnr = re.split("[NGB]", sheet_ranges[f'B{cellNr}'].value)
        newNGB = f"NGB {NGBnr[-1]}"

    except:
        if type(sheet_ranges[f'B{cellNr}'].value) == int:
            newNGB = f"NGB {sheet_ranges[f'B{cellNr}'].value}"
        else:
            continue
