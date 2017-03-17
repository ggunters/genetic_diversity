import random as r

r.seed()

src = open('raw/HGDP_FinalReport_Forward.txt', 'r')
dest = open('rand_sample.tsv', 'w')

dest.write(src.readline())

while (True):
	line = src.readline()
	if (line == ''):
		break
	if (r.random()*100 < 1 and line[0:4] != 'Mito'):
		dest.write(line)

src.close()
dest.close()
