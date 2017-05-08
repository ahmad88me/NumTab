#!/usr/bin/env python
# -*- coding: utf-8 -*-
#from properties.wdproperties import wd_props
import json
import re
wd_props = json.loads(open('properties/properties-unambiguous.txt').read())
wdquery = __import__("wd-query")
datastruct = __import__("data-structure")

wd_values_file = open('gold/numtab.txt', 'a+')
log_file = open('gold/logs-1.txt', 'a+')


for db_p, wd_p in wd_props.iteritems():
	# only needed for manual mapping
	#wd_p = re.sub('https://www.wikidata.org/wiki/Property:', '', wd_p)

	classes = wdquery.get_classes_with_numbers(wd_p)

	for class_result in classes['results']['bindings']:
		class_wd = class_result['class']['value']
		triples = wdquery.get_item_triples_for_class_and_property(class_wd, wd_p)
		#print triples
		#print 'class: ' + class_result['class']['value']
		print 'proeprty: ' + wd_p
		datastruct.make_dict(triples, class_wd, wd_p, db_p, wd_values_file, log_file)

wd_values_file.close()
log_file.close()