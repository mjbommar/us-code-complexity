# -*- coding: utf-8 -*-
'''
@author mjbommar
@date Jan 30, 2009
'''

import csv
import codecs
import cPickle
import glob
import htmlentitydefs
import lxml.etree
import multiprocessing
import nltk
import os.path
from pylab import log2
import re
import sys
import zipfile

stopwords = nltk.corpus.stopwords.words('english')
porter = nltk.PorterStemmer()

def initOutput():
	'''
	Setup the UTF-8 output.
	'''
	streamWriter = codecs.lookup('utf-8')[-1]
	sys.stdout = streamWriter(sys.stdout)

def entropy(words):
	N = float(len(words))
	P = [words.count(w)/N for w in set(words)]	
	return -sum([p*log2(p) for p in P])

if __name__ == "__main__":
	initOutput()
	elements = cPickle.load(open('data/text.pickle','rb'))
	
	titleSize = {}
	
	for e in elements:
		if not e:
			continue

		if 'APPENDIX' in e[0]:
			continue
		
		title = int(e[0].split()[1])
		if not titleSize.has_key(title):
			titleSize[title] = []

		words = [w.lower().strip() for w in nltk.word_tokenize(e[1])]
		words = [w for w in words if len(w) > 3 and w not in stopwords]
		titleSize[title].extend(words)
	

	output_file = csv.writer(open('results/table_title_entropy.csv', 'w'))	

	for (k,v) in titleSize.iteritems():
		print k, entropy(v)
		output_file.writerow((k, entropy(v)))

