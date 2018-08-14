import sys
import whoosh
import csv
import os
from datetime import datetime
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from whoosh.query import *
from whoosh.searching import *
def search(indexer, searchTerm):
	with indexer.searcher() as searcher:
		queryTest = MultifieldParser(["City", "avgTemp", "avgLow", "avgHigh", "State", "Date"], schema=indexer.schema).parse(searchTerm)
		#nr = NumericRange("Index", 1, 200);
		#np = query.Term("Index", 151);
		results = searcher.search(queryTest, limit=None)
		print("Length of results: " + str(len(results)))
		Cities = {};
		for line in results:
			print(line);
			'''
			if line['City'] in Cities:
				pass;
			else:
				print(line['City']);
				Cities[line['City']] = 1;
			'''
			
def index():
	schema = Schema(City=TEXT(stored=True), Index=NUMERIC(stored=True), State=TEXT(stored=True), Date=DATETIME(stored=True), avgHigh=NUMERIC(float, stored=True), avgLow=NUMERIC(float, stored=True), avgUV=NUMERIC(float, stored=True), totalSun=NUMERIC(float, stored=True), avgSun=NUMERIC(float, stored=True), totalSnow=NUMERIC(float, stored=True), avgSnow=NUMERIC(float, stored=True), totalRainfall=NUMERIC(float, stored=True), avgRainfall=NUMERIC(float, stored=True), avgHumidity=NUMERIC(float, stored=True), pressure=NUMERIC(float, stored=True), windSpeed=NUMERIC(float, stored=True), avgTemp=NUMERIC(float, stored=True));
	indexer = create_in("indexedData", schema)
	
	writer = indexer.writer()
	
	fp = open("./weather_data/weather-data-complete.csv", "r");
	data = [];
	header=next(fp);
	i = 1;
	for line in fp:
		row = line.split(',');
		print("Adding Index: " + str(i));
		i+=1;
		row[3] = datetime.datetime.strptime(row[3], "%Y-%m")
		print(row[3]);
		writer.add_document(City=row[1], Index=row[0], State=row[2], Date=row[3], avgHigh=float(row[4]), avgLow=float(row[5]), avgUV=row[6], totalSun=row[7], avgSun=row[8], totalSnow=row[9], avgSnow=row[10], totalRainfall=row[11], avgRainfall=row[12], avgHumidity=row[13], pressure=row[14], windSpeed=row[15], avgTemp=row[16])
		
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
	'''
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
	'''
	for c in argv:
		searchTerm += c;
		searchTerm += " "
	print(searchTerm);
	results = search(indexer, searchTerm)

if __name__ == '__main__':
	main(sys.argv[1:])