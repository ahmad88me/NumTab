import bz2
import re
from collections import defaultdict
import json

dump_path = '/Users/admin/code/csv2rdf/dataset/dump.nt.bz2'
numerical_dump = open('numerical-dump.txt', 'a+')
numerical_dict = defaultdict()

with bz2.BZ2File(dump_path, "r") as file:
	for line in file:
		#if prop direct
		triple = line.split()
		#print triple[2]
		for x in range(3, len(triple)):
			triple[2] += ' ' + triple[x]
		#print triple[2]
		if 'P' in triple[1] and '"' in triple [2] and not triple[2].startswith('<http') and bool(re.search(r'\d', triple[2])) and not re.match( '"(.*?)"\@(.*?) .', triple[2]):
			#print triple[2].split('"')[1].replace('+','')
			#print triple[2]
			#print triple[1].replace('<','').replace('>','')
			#numerical_dump.write(triple[0].replace('<','').replace('>','') + ' ' + triple[1].replace('<','').replace('>','') + ' ' + triple[2].split('"')[1].replace('+','') + '\n')
			triple[2] = triple[2].split('"')[1].replace('+','')
			# for dates like 2017-03-03T06:36:48Z
			if 'Z' in triple[2]:
				triple[2] = triple[2][:4]
			key = triple[0].replace('<','').replace('>','') + '+' + triple[2]
			if not key in numerical_dict:
				numerical_dict[key] = [triple[1].replace('<','').replace('>','')]
			else:
				numerical_dict[key].append(triple[1].replace('<','').replace('>',''))
			print numerical_dict
	json.dump(numerical_dict, numerical_dump)