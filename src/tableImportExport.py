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
import igraph
import lxml.etree
import multiprocessing
import os.path
import re
import sys
import zipfile


def initOutput():
	'''
	Setup the UTF-8 output.
	'''
	streamWriter = codecs.lookup('utf-8')[-1]
	sys.stdout = streamWriter(sys.stdout)
	
if __name__ == "__main__":
	'''
	Set the snapshot and load the file list.
	'''
	initOutput()
	
	titles = range(1,51)
	titles.remove(34)
	titleNet = dict(zip(titles, [0]*len(titles)))
	
	edges = cPickle.load(open('data/citations.pickle'))
	sectionID = cPickle.load(open('data/sectionID.pickle'))
	edges = [(sectionID[e[0]], sectionID[e[1]]) for e in edges if sectionID.has_key(e[0]) and sectionID.has_key(e[1])]
	edges = [(e[0],e[1]) for e in edges if 'APPENDIX' not in e[0] and 'APPENDIX' not in e[1]]
	edges = [map(int,(e[0].split()[1], e[1].split()[1])) for e in edges]
	
	for e in edges:
		titleNet[e[0]] -= 1
		titleNet[e[1]] += 1
	
	output_file = csv.writer(open('results/table_title_import.csv', 'w'))
	
	for (k,v) in titleNet.iteritems():
		print "{0},{1}".format(k,v)
		output_file.writerow((k, v))
		
	
	
	
	
