# -*- coding: utf-8 -*-
from datamodules import Corpus, TwitterList, Domains

def getKeywords():
	corpus = Corpus('..', Domains)
	corpus.countDocsOnWords()
	corpus.calculateTFIDF()
	#corpus.display()
	return corpus.getKeywords(10000)

def computeImportance():
	twitters = TwitterList()
	twitters.loadKeywords('keywords.json')
	twitters.calculateImportance()
	twitters.addImportanceToDB()

if __name__ == '__main__':
	keywords = getKeywords()
	computeImportance()