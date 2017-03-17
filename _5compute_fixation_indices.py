import pickle

def dump(obj, path):
	file = open(path, 'w')
	pickle.dump(obj, file)
	file.close()

def load(path):
	file = open(path, 'r')
	x = pickle.load(file)
	file.close()
	return x

MINIMUM_SUBJECTS = 9

subjects = load('objects/subjects.p')
loci = load('objects/loci.p')
pops_map = load('objects/pops_map.p')
diffs_map = load('objects/diffs_map.p')

# estimate fixation index for each pair of populations
# from https://en.wikipedia.org/wiki/Fixation_index
# F_st = (PI_between - PI_within) / PI_between
f_sets = {}
for ingroup in pops_map.keys():
	ingroup_subs = pops_map[ingroup]
	n = len(ingroup_subs)
	if (n < MINIMUM_SUBJECTS): continue

	f_set = {}

	# PI is average number if diffs per site
	n_pairs = 0
	diffs_per_site = 0.0
	for i in range(n):
		subI = ingroup_subs[i]
		for j in range(n):
			subJ = ingroup_subs[j]
			#if (subI == subJ): continue
			n_pairs += 1
			diffs_per_site += diffs_map[subI][subJ]
	PI_within = diffs_per_site / n_pairs

	for outgroup in pops_map.keys():
		#if (ingroup == outgroup): continue
		outgroup_subs = pops_map[outgroup]
		m = len(outgroup_subs)
		if (m < MINIMUM_SUBJECTS): continue

		# PI is average number if diffs per site
		n_pairs = 0
		diffs_per_site = 0.0
		for i in range(n):
			subI = ingroup_subs[i]
			for j in range(m):
				subJ = outgroup_subs[j]
				n_pairs += 1
				diffs_per_site += diffs_map[subI][subJ]
		PI_between = diffs_per_site / n_pairs

		f_set[outgroup] = (PI_between - PI_within) / PI_between

	f_sets[ingroup] = f_set

pops = f_sets.keys()
pops.sort()
outfile = open('fixation_indices.tsv', 'w')
for p2 in pops:
	outfile.write('\t' + p2)
for p1 in pops:
	outfile.write('\n')
	outfile.write(p1)
	for p2 in pops:
		outfile.write('\t' + str(f_sets[p1][p2]))
outfile.close()

dump(f_sets, 'objects/f_sets.p')
