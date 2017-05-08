import requests

wd_url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'

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

# get all 'instance of' classes for the items connected to a given properties
# must be at least 100 items per class
# limit to max of 5000 items otherwise hell breaks loose
# limit to 20 classes
def get_classes_with_numbers(prop):
	query = """
		SELECT ?class (COUNT(?item) AS ?count)
		WHERE
		{
			?item wdt:%s ?value .
		  	?item wdt:P31 ?class .
		} GROUP BY (?class)
		HAVING (?count > 100 && ?count < 5000) LIMIT 20
	""" % prop
	try:
		wd_results = requests.get(wd_url, params={'query': query, 'format': 'json'}).json()
		if wd_results:
			return wd_results
	except Exception as e:
		print e
		return

# REMOVE LIMIT 10 !!!
def get_item_triples_for_class_and_property(cl, prop):
	#use wdt instead of 
	query = """
		SELECT DISTINCT ?item ?prop ?object
		WHERE
		{
		    ?item ?prop ?object .
		  	?item wdt:%s ?value .
			?item wdt:P31 <%s> .
		    FILTER( regex(str(?prop), "wikidata.org" ))
		} #LIMIT 10
	""" % (prop, cl)
	try:
		wd_results = requests.get(wd_url, params={'query': query, 'format': 'json'}).json()
		if wd_results:
			return wd_results
	except Exception as e:
		print e
		return