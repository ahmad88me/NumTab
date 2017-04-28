data_struc = {}


def make_dict(data):
	for result in data['results']['bindings']:
		item = result['item']['value']