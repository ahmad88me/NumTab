import bz2
import re
from collections import defaultdict
import requests
import json

#dump_path = '/Users/admin/code/csv2rdf/dataset/dump.nt.bz2'
golden_wikidata = open('gold/golden_wikidata.txt', 'a+')
properties_mapped = open('gold/wikidata-values-1.txt')

wd_url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'

#numerical_dict = defaultdict(list)
#wd_entities = defaultdict(list)
last_prop = ''

#wd_entities = {}
for line in properties_mapped:
	l = line.split(': ')
	db_prop = l[0]

	if not db_prop == last_prop:
		golden_wikidata.write('\n' + db_prop + '\n' + '50' + '\n')

	p = l[2].replace('https://www.wikidata.org/wiki/Property:', '')

	values = l[3].split(',')
	for v in values:
		#wd_entities[key].append(v.replace('\n', '') + ' ' + l[2])
		s = v.replace('http://www.wikidata.org/entity/', '')
		query = 'SELECT ?o WHERE { wd:' + s + ' wdt:' + p + ' ?o . }'
		print query
		try:
			wd_results = requests.get(wd_url, params={'query': query, 'format': 'json'}).json()
			if wd_results:
				print 'dbpedia: ' + l[0] + ' result: '+ wd_results['results']['bindings'][0]['o']['value']
				golden_wikidata.write(wd_results['results']['bindings'][0]['o']['value'] + '\n')
		except Exception as e:
			print e
	last_prop = db_prop
golden_wikidata.close()
#for k, v in wd_entities.iteritems():
#	print k



'''
with bz2.BZ2File(dump_path, "r") as file:
	for line in file:
		triple = line.split()
		if 'P' in triple[1] and "'" in triple [2] and not triple[2].startswith('<http') and bool(re.search(r'\d', triple[2])) and not re.match( '"(.*?)"\@(.*?) .', triple[2]):		
			# make them pretty!
			triple[0] = triple[0].replace('<','').replace('>','')
			triple[1] = triple[1].replace('<','').replace('>','')
			triple[1] = re.sub('https://www.wikidata.org/wiki/Property:', '', triple[1])

			for db_prop, v in wd_entities.iteritems():
				for ent in v:
					if ent == (triple[0] + ' ' + triple[1]):

						for x in range(3, len(triple)):
							triple[2] += ' ' + triple[x]
						triple[2] = triple[2].split('"')[1]
						triple[2] = triple[2].replace('+','')
						if 'Z' in triple[2]:
							triple[2] = triple[2][:4]
						print db_prop + ': ' +triple[0] + ' ' + triple[1] + ' ' + triple[2]


		if triple[1] in properties_mapped:

			value_dump.write(triple[0].replace('<','').replace('>','') + ' ' + triple[1] + ' ' + triple[2])
'''