#!/usr/bin/python3

from os.path import basename
from glob import glob

def main():
	results = ""

	countries = []

	filePaths = glob("../data/*")

	for filePath in filePaths:
		country = {}

		fileBasename = basename(filePath)
		country["name"] = fileBasename.replace("_", " ")[0:(len(fileBasename) - 4)]

		file = open(filePath, "r")

		for x in file:
			line = x.replace("\n", "")
			lineStart = line[0:7]

			if lineStart == "\"Linux\"":
				country["linux"] = float(line[8:])
				break

		file.close()

		if "linux" not in country:
			country["linux"] = 0

		countries.append(country)

	countryCount = len(countries)

	while True:
		isSorted = True

		for i in range(countryCount - 1):
			currentC = countries[i]
			nextC = countries[i + 1]

			if nextC["linux"] > currentC["linux"]:
				countries[i + 1] = currentC
				countries[i] = nextC

				isSorted = False

		if isSorted:
			break

	for i in range(countryCount):
		country = countries[i]

		hi = i + 1

		countryName = country["name"]
		countryLinux = country["linux"]

		results += f"{hi}. {countryName} - {countryLinux}%\n";

	resultsFile = open("../results.txt", "w")
	resultsFile.write(results)
	resultsFile.close()

	print(results)
	print("DONE")

main()
