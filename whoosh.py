import sys
import whoosh
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser

def search(indexer, searchTerm):
	with indexer.searcher() as searcher:
		query = MultifieldParser(["title", "content"], schema=indexer.schema).parse(searchTerm)
		results = searcher.search(query)
		print("Length of results: " + str(len(results)))
		for line in results:
			print(line['title'] + ": " + line['content'])

def index():
	schema = Schema(title=TEXT(stored=True), path=ID(stored=True), content=TEXT(stored=True))
	indexer = create_in("indexDir", schema)

	writer = indexer.writer()
	test = ['First document', 'Second document']
	test = map(unicode,test)
	writer.add_document(title=test[0], path=u"/a", content=u"This is the document we've added!")
	writer.add_document(title=test[1], path=u"/b", content=u"The second one is even more interesting!")
	writer.commit()
	return indexer

def main():
	searchTerm = 'First OR Second'
	indexer = index()
	results = search(indexer, searchTerm)



if __name__ == '__main__':
	main()
