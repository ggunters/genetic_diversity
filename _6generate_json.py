# JSON object needs to be hard coded into visualization!
# Copy and paste text in data_obj.json into vis.htm

import pickle
import json
import re

def dump(obj, path):
	file = open(path, 'w')
	pickle.dump(obj, file)
	file.close()

def load(path):
	file = open(path, 'r')
	x = pickle.load(file)
	file.close()
	return x

f_sets = load('objects/f_sets.p')

geos = []
nodes = []
for k in f_sets.keys():
	tokens = re.sub('_', ' ', k).split(' - ')
	d = {}
	geo = tokens[0]
	geo = re.sub('Subsaharian', 'Subsaharan', geo)
	geo = re.sub('Middle Est', 'Middle East', geo)
	geo = re.sub('America', 'Americas', geo)
	if (geo not in geos):
		geos.append(geo)
	for i in range(len(geos)):
		if (geos[i] == geo):
			d['group'] = i
			break
	avg_F = 0
	for other_k in f_sets[k].keys():
		avg_F += f_sets[k][other_k]
	avg_F = round(avg_F / len(f_sets.keys()), 3)
	d['key'] = k
	d['geo'] = geo
	d['subgeo'] = tokens[1]
	d['name'] = tokens[2]
	d['avg_F']  = avg_F
	nodes.append(d)

links = []
for i in range(len(nodes)):
	for j in range(len(nodes)):
		d = {}
		d['source'] = i
		d['target'] = j
		k1 = nodes[i]['key']
		k2 = nodes[j]['key']
		F_st = f_sets[k1][k2]
		d['value'] = round(F_st, 3)
		links.append(d)

Min = Max = 0
for k1 in f_sets.keys():
	for k2 in f_sets[k1].keys():
		v = f_sets[k1][k2]
		if (v < Min): Min = v
		if (Max < v): Max = v
Min = round(Min, 3)
Max = round(Max, 3)

j = {'nodes': nodes, 'links': links, 'min': Min, 'max': Max}
json_file = open('vis/data_obj.json', 'w')
json.dump(j, json_file)
json_file.close()
