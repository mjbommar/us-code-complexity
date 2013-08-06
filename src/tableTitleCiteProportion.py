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
	
	edges = cPickle.load(open('data/citations.pickle'))
	sectionID = cPickle.load(open('data/sectionID.pickle'))
	edges = [(sectionID[e[0]], sectionID[e[1]]) for e in edges if sectionID.has_key(e[0]) and sectionID.has_key(e[1])]
	edges = [(e[0],e[1]) for e in edges if 'APPENDIX' not in e[0] and 'APPENDIX' not in e[1]]
	edges = [map(int,(e[0].split()[1], e[1].split()[1])) for e in edges]
	
	titleI = {}
	for e in edges:
		if not titleI.has_key(e[0]):
			titleI[e[0]] = [0,0]
			
		if e[0] == e[1]:
			titleI[e[0]][0] += 1
		else:
			titleI[e[0]][1] += 1
	
	output_file = csv.writer(open('results/table_title_cite_prop.csv', 'w'))	

	for k in titleI.keys():
		print k, titleI[k][0] / float(sum(titleI[k]))
		output_file.writerow((k, titleI[k][0] / float(sum(titleI[k]))))
		
	
	
	
	
