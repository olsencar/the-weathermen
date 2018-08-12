import sys
import whoosh
import csv
import os
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser

def search(indexer, searchTerm):
	with indexer.searcher() as searcher:
		query = MultifieldParser(["City" ,"State", "Date"], schema=indexer.schema).parse(searchTerm)
		results = searcher.search(query)
		print("Length of results: " + str(len(results)))
		for line in results:
			print(line);

def index():
	schema = Schema(City=TEXT(stored=True), Index=ID(stored=False), State=TEXT(stored=True), Date=TEXT(stored=True), avgHigh=NUMERIC(float, stored=False), avgLow=NUMERIC(float, stored=False), avgUV=NUMERIC(float, stored=False), totalSun=NUMERIC(float, stored=False), avgSun=NUMERIC(float, stored=False), totalSnow=NUMERIC(float, stored=False), avgSnow=NUMERIC(float, stored=False), totalRainfall=NUMERIC(float, stored=False), avgRainfall=NUMERIC(float, stored=False), avgHumidity=NUMERIC(float, stored=False), pressure=NUMERIC(float, stored=False), windSpeed=NUMERIC(float, stored=False));
	indexer = create_in("indexedData", schema)
	
	writer = indexer.writer()
	
	fp = open("weather-data-complete.csv", "r");
	data = [];
	header=next(fp);
	i = 1;
	for line in fp:
		row = line.split(',');
		print("Adding Index: " + str(i));
		i+=1;
		writer.add_document(City=row[1], Index=row[0], State=row[2], Date=row[3], avgHigh=float(row[4]), avgLow=float(row[5]), avgUV=row[6], totalSun=row[7], avgSun=row[8], totalSnow=row[9], avgSnow=row[10], totalRainfall=row[11], avgRainfall=row[12], avgHumidity=row[13], pressure=row[14], windSpeed=row[15])
		
	writer.commit();
	
	return indexer


def main(argv):
	if (os.path.isdir("indexedData") == True):
		import whoosh.index as indexUSE
		indexer = indexUSE.open_dir("indexedData");
	else:
		os.makedirs("indexedData")
		indexer = index()
	count=0;
	searchTerm = ""
	for c in argv:
		if (count == 0):
			if (c):
				searchTerm += c;
				searchTerm += " AND ";
		if (count == 1):
			if (c):
				searchTerm += c;
				searchTerm += " AND ";
		if (count == 2):
			if (c):
				searchTerm += c;
		count+=1;
	print(searchTerm);
	results = search(indexer, searchTerm)
	



if __name__ == '__main__':
	main(sys.argv[1:])