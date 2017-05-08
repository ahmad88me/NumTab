#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
create_json = __import__("create-json")

def make_dict(triples, class_wd, wd_p, db_p, wd_values_file, log_file):
	data_struc = {}
	for result in triples['results']['bindings']:
		if 'statement' not in result['object']['value'] and not str(result['prop']['value']) == 'http://www.wikidata.org/prop/direct/P31':
			item = result['item']['value']
			propob = str(result['prop']['value']) 
			propob += result['object']['value'].encode('utf8')
			if propob not in data_struc:
				data_struc[propob] = []
				data_struc[propob].append(item)
			else:
				data_struc[propob].append(item)
	mx = 0
	max_key = ''
	for k, v in data_struc.iteritems():
		if len(v) > mx:
			max_key = k
			mx = len(v)
	
	#print class_wd
	#print max_key
	#print len(data_struc[max_key])
	#print data_struc[max_key]
	values = get_values(triples, data_struc[max_key], wd_p)
	#print values
	#print str(len(values)) + ' ' + str(len(data_struc[max_key]))
	#print data_struc[max_key]
	# get random 50 values

	#random.shuffle(data_struc[max_key])
	#wikidata_entities = data_struc[max_key][0:50]

	create_json.create(class_wd, wd_p, db_p, values, max_key, wd_values_file, log_file)

def get_values(triples, wd_entities, wd_p):
	values = []
	print wd_p
	itemprop = []
	for result in triples['results']['bindings']:
		if result['item']['value'] in wd_entities:
			if result['prop']['value'] == ('http://www.wikidata.org/prop/direct/' + wd_p):
				ip = result['item']['value'] + result['prop']['value']
				if not ip in itemprop:
					values.append(result['object']['value'])
					itemprop.append(ip)
	return values
