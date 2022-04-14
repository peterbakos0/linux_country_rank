#!/usr/bin/python3

import datetime
import requests
from bs4 import BeautifulSoup

def main():
	countries = []

	print("downloading main page")

	rawHtml = requests.get("https://gs.statcounter.com/os-market-share/desktop/worldwide/").content
	dom = BeautifulSoup(rawHtml, "lxml")

	regionsElem = dom.body.find(id="regions")
	allRegionsElem = dom.body.find(id="all-regions")

	countryElems = list(regionsElem.children) + list(allRegionsElem.children)

	for countryElem in countryElems:
		country = {}

		try:
			countryLinkEnd = countryElem.find("a")["href"]
			country["link"] = "https://gs.statcounter.com" + countryLinkEnd
		except:
			continue

		country["name"] = countryElem.string[1:]

		countries.append(country)

	countryCount = len(countries)

	for i in range(countryCount):
		country = countries[i]

		hi = i + 1

		print(str(hi) + "/" + str(countryCount) + ": " + country["name"])

		print("downloading country page")

		countryRawHtml = requests.get(country["link"]).content

		print("generating link")

		countryDom = BeautifulSoup(countryRawHtml, "lxml")

		metaElem = countryDom.head.find(property="og:image")
		metaContent = metaElem["content"]

		countryCode = metaContent[(metaContent.rfind("-") + 1):(metaContent.rfind("."))]

		if countryCode == "00":
			countryCode = "ww"
		elif countryCode == "01":
			countryCode = "af"
		elif countryCode == "02":
			countryCode = "as"
		elif countryCode == "03":
			countryCode = "eu"
		elif countryCode == "04":
			countryCode = "na"
		elif countryCode == "05":
			countryCode = "oc"
		elif countryCode == "07":
			countryCode = "sa"

		countryName = country["name"]

		date = datetime.date.today()

		year = date.year
		month = str(date.month - 1)

		if len(month) < 2:
			month = "0" + month

		dataLink = f"https://gs.statcounter.com/os-market-share/desktop/worldwide/chart.php?device=Desktop&device_hidden=desktop&statType_hidden=os_combined&region_hidden={countryCode}&granularity=monthly&statType=Operating%20System&region={countryName}&fromInt={year}{month}&toInt={year}{month}&fromMonthYear={year}-{month}&toMonthYear={year}-{month}&csv=1"

		print(dataLink)

		print("downloading data")

		data = requests.get(dataLink).content

		filename = country["name"].replace(" ", "_").replace("(", "").replace(")", "") + ".csv"
		filepath = "../data/" + filename

		print("saving data")

		file = open(filepath, "wb")
		file.write(data)
		file.close()

	print("DONE")

main()
