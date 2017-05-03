#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
create_json = __import__("create-json")

data_struc = {}


def make_dict(data, class_wd, wd_p, db_p):
	for result in data['results']['bindings']:
		if 'statement' not in result['object']['value'] and not str(result['prop']['value']) == 'http://www.wikidata.org/prop/direct/P31':
			item = result['item']['value']
			propob = str(result['prop']['value']) 
			propob += result['object']['value'].encode('utf8')
			if propob not in data_struc:
				data_struc[propob] = []
				data_struc[propob].append(item)
			else:
				data_struc[propob].append(item)
	max_key = max(data_struc, key= lambda x: len(set(data_struc[x])))
	#print max_key
	#print len(data_struc[max_key])
	#print data_struc[max_key]
	# get random 50 values
	random.shuffle(data_struc[max_key])
	wikidata_entities = data_struc[max_key][0:50]

	create_json.create(class_wd, wd_p, db_p, wikidata_entities, max_key)

