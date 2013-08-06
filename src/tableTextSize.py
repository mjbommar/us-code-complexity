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

if __name__ == "__main__":
	initOutput()
	elements = cPickle.load(open('data/text.pickle','rb'))

	titleSize = {}
	titleSWSize = {}
	
	for e in elements:
		if not e:
			continue

		if 'APPENDIX' in e[0]:
			continue
		
		title = int(e[0].split()[1])
		if not titleSize.has_key(title):
			titleSize[title] = 0                                 
			titleSWSize[title] = 0
		
		words = [w.lower().strip() for w in nltk.word_tokenize(e[1])]
		words_sw = [w for w in words if len(w) > 3 and w not in stopwords]
		titleSize[title] += len(words)
		titleSWSize[title] += len(words_sw)
	
	output_file = csv.writer(open('results/table_title_text_size.csv', 'w'))
	
	for (k,v) in titleSize.iteritems():
		print k, v
		output_file.writerow((k, titleSize[k], titleSWSize[k]))
		
