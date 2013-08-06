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
import re
import sys
import zipfile


def unescape(text):
	'''
	http://effbot.org/zone/re-sub.htm#unescape-html
	'''
	def fixup(m):
		text = m.group(0)
		if text[:2] == "&#":
			# character reference
			try:
				if text[:3] == "&#x":
					return unichr(int(text[3:-1], 16))
				else:
					return unichr(int(text[2:-1]))
			except ValueError:
				pass
		else:
			# named entity
			try:
				text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
			except KeyError:
				pass
		return text # leave as is
	return re.sub("&#?\w+;", fixup, text)

def extractLocation(hdnestgrp):
	'''
	Extract the location from the header.
	'''
	return [header.text for header in list(hdnestgrp)]

def extractSectionName(head):
	'''
	Extract the section's name from the section header.
	'''
	sectionName = unicode('').join([text.encode('utf-8', 'xmlcharrefreplace') for text in head.itertext()])
	return unescape(sectionName)

def parseBuffer(buffer):
	elements = []
	
	'''
	Set up the parser so that it doesn't choke on entities.
	'''
	parser = lxml.etree.XMLParser(resolve_entities = False, recover = True)

	'''
	Parse a section file.
	'''
	tree = lxml.etree.fromstring(buffer, parser)

	'''
	Check for a ToC file and skip it.
	'''
	if tree.tag != 'uscfrag':
		return None
	
	'''
	Do another check and skip it.
	'''
	hdnestgrp = tree.find('hdnestgrp')
	section = tree.find('section')

	if hdnestgrp == None or section == None:
		return None
	
	location = extractLocation(hdnestgrp)
	extid = section.attrib['extid']
	
	'''
	Now extract the elements from the section.
	'''
	head = section.find('head')
	sectionName = extractSectionName(head)
	
	content = section.find('sectioncontent')
	
	fullLocation = unicode('_').join(location)
	fullLocation = u'{0}_{1}'.format(fullLocation, sectionName).strip()
	edges = [(extid, ref.attrib['target']) for ref in content.findall(".//subref") if ref.attrib['type'] == 'sec']
	
	return edges

if __name__ == "__main__":
	'''
	Set the snapshot and load the file list.
	'''

	snapshot = '20100308'
	codeZip = zipfile.ZipFile('data/usc-%s.zip' % (snapshot))
	codeFiles = [codeFile for codeFile in sorted(codeZip.namelist()) if codeFile.lower().endswith('xml')]
	
	elements = []
	results = []
	for codeFile in codeFiles:
		xmlBuffer = codeZip.read(codeFile)
		results.append(parseBuffer(xmlBuffer))
		
	sedges = [s for s in results if s]
	edges = []
	for s in sedges:
		edges.extend(s)
	print len(sedges)
	print len(edges)

	cPickle.dump(edges, open('data/citations.pickle','wb'))
