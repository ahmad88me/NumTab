import bz2
import re
from collections import defaultdict
import json

dump_path = '/Users/admin/code/csv2rdf/dataset/dump.nt.bz2'
value_dump = open('value-dump.txt', 'a+')
numerical_dict = defaultdict()
properties_mapped = json.loads(open('properties/properties-automatic')).keys()

with bz2.BZ2File(dump_path, "r") as file:
	for line in file:
		triple = line.split()

		triple[1] = triple[1].replace('<','').replace('>','')
		triple[1] = re.sub('https://www.wikidata.org/wiki/Property:', '', triple[1])

		if triple[1] in properties_mapped:
			for x in range(3, len(triple)):
				triple[2] += ' ' + triple[x]
			triple[2] = triple[2].split('"')[1].replace('+','')
			if 'Z' in triple[2]:
				triple[2] = triple[2][:4]
			value_dump.write(triple[0].replace('<','').replace('>','') + ' ' + triple[1] + ' ' + triple[2])