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
import pylab
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
	initOutput()
	root = False	
	
	elements = cPickle.load(open('data/elements.pickle'))
	nodes = set()
	edges = set()
	
	for e in elements:
		p = e.split('_')
		
		for i in range(1, len(p)):
			eA = '_'.join(p[0:i])
			eB = '_'.join(p[0:i+1])
			nodes.update([eA,eB])
			edges.add((eA,eB))
	
	nodes = sorted(list(nodes))
	nodeMap = dict(zip(nodes, range(len(nodes))))
	edges = sorted(list(edges))
	edges = [(nodeMap[e[0]], nodeMap[e[1]]) for e in edges]

	'''
	Add the USC root node.
	'''
	if root:
		rootNode = len(nodes)
		nodes.append('ROOT')
		for i,node in enumerate(nodes):
			if node.count('_') == 0:
				edges.append((i, rootNode))
	
	g = igraph.Graph(edges)
	for i,v in enumerate(g.vs):
		v['label'] = nodes[i]
		
	print g
	c = g.components()
	for i in range(len(c)):
		gg = c.subgraph(i)
		print gg.vs[0]
