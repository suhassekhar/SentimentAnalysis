import xlwt
import xlsxwriter
import datetime
import sys
import xlrd
import os.path


workbook = xlsxwriter.Workbook('demo_trial.xlsx')

worksheet = workbook.add_worksheet('current')
worksheet.write('A1', 'time')

# Text with formatting.
worksheet.write('B1', 'positive')

# Text with formatting.
worksheet.write('C1', 'negative')
#workbook.close()
row = 1
#row = last_row
col = 0
for line in sys.stdin:
    if line.split(' ',1)[0] == 'time':
        time = line.rsplit(None, 1)[-1]
        worksheet.write(row, col, time)
        col += 1
    elif line.split(' ',1)[0] == 'positive':
        positive = line.rsplit(None, 1)[-1]
        posval = int(positive)
        worksheet.write(row, col, posval)
        col += 1
    elif line.split(' ',1)[0] == 'negative':
        negative = line.rsplit(None, 1)[-1]
        negval = int(negative)
        worksheet.write(row, col, negval ) ##change to worksheet to go to old
        row += 1
        col = 0
workbook.close() ##change to workbook to go to old
