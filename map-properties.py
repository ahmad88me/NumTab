from SPARQLWrapper import SPARQLWrapper, JSON
import requests

import pandas as pd

dbsparql = SPARQLWrapper('http://dbpedia.org/sparql')
wd_url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
properties_file_path = '/Users/admin/code/csv2rdf/dataset/golden-wikidata/properties/properties.csv'

log_file = open('properties/log.txt', 'a+')
wd_properties_file = open('properties/wd-properties.py', 'a+')

# read the properties.csv file by bob
#returns a list of properties
def get_db_properties():
	df = pd.read_csv(properties_file_path, usecols=[0])
	return df

# get properties from Wikidata connecting given subject and object
#returns a dict with values for p
def get_wd_properties(s, o):
	query = 'SELECT ?p WHERE { <' + s + '> ?p ' + o + ' . FILTER (!regex(STR(?p), "wikiba.se")) }'
	try:
		wd_results = requests.get(wd_url, params={'query': query, 'format': 'json'}).json()
		if wd_results:
			return wd_results
	except Exception as e:
		print e
		return

# get subjects and objects for a given predicate
# returns a dict with values for wd and o
def get_db_data(property):
	query = """
		PREFIX owl: <http://www.w3.org/2002/07/owl#>
		SELECT ?wd ?o WHERE{
			?s <%s> ?o. 
			?s owl:sameAs ?wd.
			FILTER( regex(str(?wd), "wikidata.org" ))
		}
	""" % property
	print query
	dbsparql.setQuery(query)
	dbsparql.setReturnFormat(JSON)
	return dbsparql.query().convert()

# connect the above functions
# print matched subject, matched value, original DBpedia property and matched Wikidata properties
# @TODO: break/continue out of the loops if certain numbers of property is collected, make it better performance wise
def get_mappings():
	wd_properties_file.write('wd_props = {')
	db_properties = get_db_properties()
	for index, row in db_properties.iterrows():	
		prop =  row['c1']
		results = get_db_data(prop)

		if results:
			#print len(results['results']['bindings'])
			counter_mapped = 0
			for result in results['results']['bindings']:
				if counter_mapped < 10:
					wd_results = get_wd_properties(result['wd']['value'], result['o']['value'])
					if wd_results['results']['bindings']:
						counter_mapped += 1
						for wd_result in wd_results['results']['bindings']:
							print 'test'
							log_file.write('WD subject: ' + result['wd']['value'] + 'DB value: ' + result['o']['value'] + 'DB property: ' + prop + 'WD property: ' + wd_result['p']['value'] + '\n')
							wd_properties_file.write('"' + prop + '": "' + wd_result['p']['value'] + '", ')
	wd_properties_file.write('}')

if __name__ == "__main__":
	get_mappings()






