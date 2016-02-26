import pandas
import numpy
import csv

import constants


def read_author():
    return pandas.read_csv(
        constants.datapath + constants.AUTHOR + '.txt',
        sep='\t', index_col=0, header=None)


def parse_link(matrix, metapath):
    with open(constants.datapath + metapath + '.txt', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')

        for row in reader:
            aid1, aid2, _ = row
            aid1 = int(aid1)
            aid2 = int(aid2)

            matrix.loc[aid1, aid2] += 1
            matrix.loc[aid2, aid1] += 1

            if matrix.loc[aid1, aid2] > 1:
                print('m[', aid1, ', ', aid2, '] = ', matrix.loc[aid1, aid2])


def create_adjacency_matrix(metapath, author):
    # initialize
    matrix = pandas.DataFrame(numpy.zeros(shape=(len(author), len(author))))
    matrix = matrix.set_index(author.index.values)
    matrix.columns = author.index.values

    parse_link(matrix, metapath)
    return matrix


def p_pagerank(t, metapath, author):
    matrix = create_adjacency_matrix(metapath, author)
    print('matrix created')

author = read_author()
# result = p_pagerank(10, 'APTPA', author)
result = p_pagerank(10, 'APVPA', author)
