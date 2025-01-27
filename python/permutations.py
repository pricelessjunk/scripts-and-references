#!/bin/python

import itertools as it


l = 'abcdefghijklmnopqrstuvwxyz'
l = list(l)
d=8
resultlist=[]

f = open('permutations.txt','w')

def recurse(curval, depth):
	global resultlist
	depth-=1
	for v in l:
		s = curval + v
		if depth > 0:
			recurse(s, depth)
		else:
			# print(s)
			resultlist.append(s)
			
			if len(resultlist)==100000:
				print('Writing out 100000 records')
				for word in resultlist:
					f.write(word + '\n')
				resultlist=[]
	
	
if __name__ == '__main__':
	
	recurse('',d)
	
	for word in resultlist:
		f.write(word + '\n')
	
	f.close()


