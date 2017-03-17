import xlrd
import re

book = xlrd.open_workbook('raw/HGDPid_populations.xls')
sheet = book.sheet_by_index(0)

outfile = open('populations.tsv', 'w')
for i in range(sheet.nrows):
    for v in sheet.row_values(i):
        outfile.write(v + '\t')
    outfile.write('\n')
outfile.close()
