import string
from unittest import result
from openpyxl import load_workbook
from bs4 import BeautifulSoup

import requests
import re
import mechanize
import csv

# TODO: Først løber vi alle id'er igennem fra 1 til 9999
nGBErrors = []
idErrors = []
unicodeErrors = []


def scrape(i):
    NGBnr = ""
    speciesName = ""
    accessionNamesAndIdentifiers = ""
    donorAssNr = ""
    breederAssDesig = ""
    species = ""  # TODO SE NOTE I EXCEL
    origin = ""
    nGBRecYear = ""
    nGBRecMonth = ""
    imporvementSts = ""
    pedigree = ""
    breederRemark = ""
    accessionRemark = ""
    actions = ""
    citations = ""
    # Contact curator if interested in SSD material TODO: ?????

    # for i in range(1, 10):
    result = requests.get(
        f"https://nordic-baltic-genebanks.org/gringlobal/accessiondetail.aspx?id={i}")
    src = result.content
    soup = BeautifulSoup(src, features="html5lib")

    sideBarWrapper = soup.find(id="main-wrapper").find("h1")

    try:
        sideBarText = sideBarWrapper.text
    except AttributeError:
        return idErrors.append(f"id is empty at: {i}")
    resultOfFind = soup.find_all("h1")

    # Find NGB Number for checking
    try:
        NGBnr = resultOfFind[0].text.replace(" ", "")
    except IndexError:
        pass
    except AttributeError:
        pass

    # Find Species Name
    try:
        result = soup.find(
            id="ctl00_cphBody_plAccessionNames").find_all("th")
        speciesName = result[0].value
    except IndexError:
        nGBErrors.append(f"speciesName IndexErrorError at:{NGBnr}")
    except AttributeError:
        nGBErrors.append(f"speciesName AttributeError at:{NGBnr}")

    try:
        donorAssNr = result[2].value
    except IndexError:
        nGBErrors.append(f"donorAssNr IndexError at:{NGBnr}")
    except TypeError:
        nGBErrors.append(f"donorAssNr TypeError at:{NGBnr}")

    try:
        result = soup.find(id="ctl00_cphBody_plAccessionNames").find_all(
            "th")

        accessionNames = []
        for th in result:
            if th.text in accessionNames:
                pass
            else:
                accessionNames.append(th.text)

        for accessionName in accessionNames:
            accessionNamesAndIdentifiers += ";"
            accessionNamesAndIdentifiers += accessionName
        accessionNamesAndIdentifiers = accessionNamesAndIdentifiers.replace(
            ";", "", 1)
    except AttributeError:
        nGBErrors.append(f"accessionNames AttributeError at:{NGBnr}")
    try:
        result = soup.find(
            id="ctl00_cphBody_plAccessionNames").find_all("td")
        for j in range(len(result)):
            if result[j].text == "Comment:":
                if result[j-2] == "Designation":
                    breederAssDesig = result[j+1]
    except AttributeError:
        nGBErrors.append(f"breederAssDesig AttributeError at:{NGBnr}")

    try:
        result = soup.find(
            id="ctl00_cphBody_plAnnotations").find_all("td")
        speciesName = result[4].text
    except AttributeError:
        nGBErrors.append(f"speciesName AttributeError at:{NGBnr}")

    try:
        result = soup.find(
            "table", {"style": "width:535px; border:1px solid black"}).find_all("td")
        origin = result[0].text
        nGBRecYear = result[2].text[-4:]
        nGBRecMonth = result[2].text[3:6]
        imporvementSts = result[6].text
        pedigree = result[5].text
    except AttributeError:
        nGBErrors.append(
            f"origin, nGBRecYear, nGBRecMonth, imporvementSts, pedigree AttributeError at:{NGBnr}")

    try:
        result = soup.find(id="ctl00_cphBody_plSource").find(
            "ul").find_all("li")

        for list in result:
            splittedTextArray = list.text.split(" ")
            for texts in splittedTextArray:
                if "genotype" in texts:
                    splittedLastResult = texts.split(":")
                    breederRemark = splittedLastResult[1].strip()
    except AttributeError:
        nGBErrors.append(f"breederRemark AttributeError at:{NGBnr}")

    try:
        result = soup.find(id="ctl00_cphBody_plNarrative").text.strip()
        resultArray = result.split(":")
        accessionRemark = resultArray[1].strip()
    except IndexError:
        nGBErrors.append(f"accessionRemark IndexError at:{NGBnr}")
    except AttributeError:
        nGBErrors.append(f"accessionRemark AttributeError at:{NGBnr}")

    try:
        result = soup.find(id="ctl00_cphBody_plActionNote").find(
            "ul").find("li").text
        actions = result

    except AttributeError:
        pass

    try:
        result = soup.find(id="ctl00_cphBody_pnlCitations").find(
            "ul").find("li").text
        citations = result

    except AttributeError:
        pass

    """
    print("NGBnr:", NGBnr)
    print("accessionNamesAndIdentifiers:", accessionNamesAndIdentifiers)
    print("speciesName:", speciesName)
    print("donorAssNr:", donorAssNr)
    print("breederAssDesig:", breederAssDesig)
    print("species:", species)
    print("origin:", origin)
    print("nGBRecYear:", nGBRecYear)
    print("nGBRecMonth:", nGBRecMonth)
    print("imporvementSts:", imporvementSts)
    print("pedigree:", pedigree)
    print("breederRemark:", breederRemark)
    print("accessionRemark:", accessionRemark)
    print("actions:", actions)
    print("citations:", citations) 
    """

    return f'"{NGBnr}","{accessionNamesAndIdentifiers}","{speciesName}","{donorAssNr}","{breederAssDesig}","{species}","{origin}","{nGBRecYear}","{nGBRecMonth}","{imporvementSts}","{pedigree}","{breederRemark}","{accessionRemark}","{actions}","{citations}"\n'


with open('data.txt', 'a') as f:
    csvHeader = 'NGBRnr,accessionNamesAndIdentifiers,speciesName,donorAssNr, breederAssDesig,species,origin,nGBRecYear,nGBRecMonth,imporvementSts,pedigree,breederRemark,accessionRemark,actions,citations\n'

    f.write(csvHeader)
    for i in range(2453, 50000):
        print(i)
        csvLine = scrape(i)
        if csvLine != "" and csvLine != None:
            try:
                f.write(csvLine)
            except UnicodeEncodeError:
                unicodeErrors.append(csvLine)

with open('unicodeErrors.txt', 'a') as unicodeErrorFile:
    for line in unicodeErrors:
        unicodeErrorFile.write(line)
        unicodeErrorFile.write('\n')

with open('NGBerrors.txt', 'a') as nGBErrorFile:
    for line in nGBErrors:
        nGBErrorFile.write(line)
        nGBErrorFile.write('\n')

with open('IDerrors.txt', 'a') as iDErrorFile:
    for line in idErrors:
        iDErrorFile.write(line)
        iDErrorFile.write('\n')
