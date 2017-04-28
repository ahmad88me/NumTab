from properties.wdproperties import wd_props
wdquery = __import__("wd-query")
datastruct = __import__("data-structure")

db_props_file = open('gold/dbpedia-properties.txt', 'a+')
wd_values_file = open('gold/wikidata-values.txt', 'a+')

for db_p, wd_p in wd_props.iteritems():
	db_props_file.write(db_p)

	# query magic
	# classes limited to 10 in wd-query!!!
	classes = wdquery.get_classes_with_numbers(wd_p)
	for class_result in classes['results']['bindings']:
		triples = wdquery.get_item_triples_for_class_and_property(class_result['class']['value'], wd_p)
		datastruct.make_dict(triples)