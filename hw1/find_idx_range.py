import constants

import csv
import math


def find_file_idx_range(filename):
    min_idx = math.inf
    max_idx = -math.inf

    with open(constants.datapath + filename + '.txt', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')

        for row in reader:
            idx, name = row
            idx = int(idx)

            print('Line', reader.line_num, ', idx =', idx, 'name =', name)

            if idx < min_idx:
                min_idx = idx
            elif idx > max_idx:
                max_idx = idx

    print('For', filename, '.txt: min_idx =', min_idx, ', max_idx =', max_idx)

find_file_idx_range(constants.A)
find_file_idx_range(constants.V)
find_file_idx_range(constants.T)
find_file_idx_range(constants.P)

'''
For author .txt: min_idx = 42166 , max_idx = 70865
For venue .txt: min_idx = 42145 , max_idx = 42164
For term .txt: min_idx = 1 , max_idx = 13575
For paper .txt: min_idx = 13576 , max_idx = 42144
'''
