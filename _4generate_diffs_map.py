import numpy as np
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

subjects = load('objects/subjects.p')
loci = load('objects/loci.p')
genotypes_matrix = load('objects/genotypes_matrix.p')

m = len(subjects)
n = len(loci)
diffs_matrix = np.zeros((m, m), np.double)
for i in range(m):
	for j in range(i, m):
		n_diffs = 0
		n_sites = 0
		for k in range(n):
			pairA = genotypes_matrix[k][i]
			pairB = genotypes_matrix[k][j]
			if (pairA != '--' and pairB != '--'):
				if (pairA[0] != pairB[0] and pairA[0] != pairB[1]):
					n_diffs += 1
				if (pairA[1] != pairB[0] and pairA[1] != pairB[1]):
					n_diffs += 1
				n_sites += 2
		diffs_matrix[i][j] = diffs_matrix[j][i] = 1.0 * n_diffs / n_sites
	print_progress(1.0 * i / m)

diffs_map = {}
m = len(subjects)
for i in range(m):
	subI = subjects[i]
	sub_map = {}
	for j in range(m):
		subJ = subjects[j]
		sub_map[subJ] = diffs_matrix[i][j]
	diffs_map[subI] = sub_map

dump(diffs_map, 'objects/diffs_map.p')
