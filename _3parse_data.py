import pickle
import sys

def dump(obj, path):
	file = open(path, 'wb')
	pickle.dump(obj, file)
	file.close()

def load(path):
	file = open(path, 'rb')
	x = pickle.load(file)
	file.close()
	return x

def print_progress(percentage):
	n_chars = int(percentage * 70)
	sys.stdout.write('|')
	for i in range(n_chars):
		sys.stdout.write('=')
	for i in range(70 - n_chars):
		sys.stdout.write(' ')
	sys.stdout.write('|\r')


# parse genotypes

infile = open('rand_sample.tsv', 'r')
text = infile.read()
infile.close()
	
lines = text.split('\n')[:-1]
fieldsets = []
for line in lines:
	fieldsets.append(line.split('\t'))

m = len(fieldsets[0])
n = len(fieldsets)
genotypes_map = {}
for j in range(1, m):
	subject = fieldsets[0][j]
	genotype = {}
	for i in range(1, n):
		locus = fieldsets[i][0]
		pair = fieldsets[i][j]
		genotype[locus] = pair
	genotypes_map[subject] = genotype
	print_progress(1.0 * (j - 1) / m)

subjects = fieldsets[0][1:]
subjects.sort()

loci = []
for fieldset in fieldsets[1:]:
	loci.append(fieldset[0])
loci.sort()

m = len(subjects)
n = len(loci)
genotypes_matrix = []
for i in range(n):
	locus = loci[i]
	genotype = []
	for j in range(m):
		subject = subjects[j]
		pair = genotypes_map[subject][locus]
		genotype.append(pair)
	genotypes_matrix.append(genotype)
	print_progress(1.0 * i / n)

dump(subjects, 'objects/subjects.p')
dump(loci, 'objects/loci.p')
dump(genotypes_matrix, 'objects/genotypes_matrix.p')


# parse populations

infile = open('populations.tsv', 'r')
text = infile.read()
infile.close()

lines = text.split('\n')[:-1]
fieldsets = []
for line in lines:
	fieldsets.append(line.split('\t'))
	
pops_map = {}
for fieldset in fieldsets[1:]:
	subject = fieldset[0]
	pop = fieldset[4] + ' - ' + fieldset[3] + ' - ' + fieldset[2]
	if (genotypes_map.has_key(subject)):
		if (pops_map.has_key(pop)):
			pops_map[pop] += [subject]
		else:
			pops_map[pop] = [subject]

dump(pops_map, 'objects/pops_map.p')
