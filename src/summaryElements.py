# -*- coding: utf-8 -*-
'''
@author mjbommar
@date Jan 30, 2009
'''


import codecs
import cPickle
import glob
import htmlentitydefs
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
	
	elements = cPickle.load(open('data/elements.pickle'))
	print 'Number of Elements:', len(elements)
	
	depthDistribution = [e.count('_') for e in elements]
	print 'Mean/Std Element Depth:', pylab.mean(depthDistribution), pylab.std(depthDistribution) 
	print 'Min/Max Element Depth:', min(depthDistribution), max(depthDistribution)
	
	'''
	Plot the element depth distribution.
	'''
	fig = pylab.figure(figsize=(8,6))
	ax = fig.add_subplot(111)
	n, b, p = pylab.hist(depthDistribution, bins = max(depthDistribution) - min(depthDistribution), normed = True, alpha = 0.5, color = 'blue')
	x = pylab.linspace(min(depthDistribution), max(depthDistribution), 20)
	y = pylab.normpdf(x,  pylab.mean(depthDistribution), pylab.std(depthDistribution))
	pylab.plot(x, y, 'r--', linewidth=1)
	pylab.xlabel('Element Depth')
	pylab.ylabel('Probability')
	pylab.savefig('figures/element_depth_distribution.png', dpi=600)
	
'''
11: TITLE 21_CHAPTER 9_SUBCHAPTER VII_Part A_§ 374_g_6_A_ii_IV_aa
11: TITLE 26_Subtitle A_CHAPTER 1_Subchapter F_PART VI_§ 527_e_5_A_ii_I
11: TITLE 42_CHAPTER 6A_SUBCHAPTER V_Part A_subpart i_§ 292d_a_1_A_i_I
'''
