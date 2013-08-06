# -*- coding: utf-8 -*-
'''
@author mjbommar
@date Jan 30, 2009
'''

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
	
	nodes = set()
	for e in edges:
		nodes.update(e)
	nodes = sorted(list(nodes))
	nodeMap = dict(zip(nodes, range(len(nodes))))
	
	edges = [(nodeMap[e[0]], nodeMap[e[1]]) for e in edges]
	g = igraph.Graph(edges, directed = True)
	print 'Citation Network', g
	print 'Giant Component', g.components().giant()
	
	indegree = g.indegree()
	outdegree = g.outdegree()
	
	print 'Highest In-Degree:'
	print sorted(zip(indegree, nodes), reverse = True)[0:5]
	print
	print 'Highest Out-Degree:'
	print sorted(zip(outdegree, nodes), reverse = True)[0:6]
	
