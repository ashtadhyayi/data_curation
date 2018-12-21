# -*- coding: utf-8 -*-
import codecs
import re
import glob
import os
import sys

def createRepList(filein, frep, commonPoolSet):
	with codecs.open(filein, 'r', 'utf-8') as fin:
		print(filein)
		print(len(commonPoolSet))
		data = fin.read().rstrip()
		words = re.split('([ ,`])', data)
		for word in words:
			if '()' in word:
				if word not in commonPoolSet:
					commonPoolSet.add(word)
					frep.write(word + ':' + word + ':' + filein.lstrip('../../../../../ashtadhyayi/') + '\n')
		
def doCorrections(filein, repList):
	fin = codecs.open(filein, 'r', 'utf-8')
	data = fin.read()
	fin.close()
	fout = codecs.open(filein, 'w', 'utf-8')
	for (pre, post) in repList:
		data = data.replace(pre, post)
	#data = re.sub('\(\)([ -~])', '\g<1>', data)
	#data = re.sub('\(\)([^ -~])', ' \g<1>', data)
	fout.write(data)
	fout.close()

if __name__ == "__main__":
	commentaryFolder = '../../../../../ashtadhyayi/nyasa'
	if len(sys.argv) > 1:
		frep = codecs.open('bracketReplacementList.txt', 'w', 'utf-8')
		commonPoolSet = set()
		subfolders = [f.path for f in os.scandir(commentaryFolder) if f.is_dir() ]
		for subfolder in subfolders:
			files = glob.glob(os.path.join(subfolder, '*.md'))
			for file in files:
				createRepList(file, frep, commonPoolSet)
		print(len(commonPoolSet))
	else:
		frep = codecs.open('bracketReplacementListManuallyCorrected.txt', 'r', 'utf-8')
		repList = []
		for line in frep:
			line = line.rstrip()
			(pre, post, filename) = line.split(':')
			repList.append((pre, post))
		subfolders = [f.path for f in os.scandir(commentaryFolder) if f.is_dir() ]
		for subfolder in subfolders:
			files = glob.glob(os.path.join(subfolder, '*.md'))
			for file in files:
				doCorrections(file, repList)
		