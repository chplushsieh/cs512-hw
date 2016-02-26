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
            aid1, aid2 = row
            aid1 = int(aid1)
            aid2 = int(aid2)

            matrix.loc[aid1, aid2] += 1
            matrix.loc[aid2, aid1] += 1

            if matrix.loc[aid1, aid2] > 1:
                print('m[', aid1, ', ', aid2, '] = ', matrix.loc[aid1, aid2])


def create_adjacency_matrix(metapath, author):
    filepath = constants.datapath + 'adjacency_matrix_for_' + metapath + '.csv'

    try:
        matrix = pandas.DataFrame.from_csv(filepath)
        # print('matrix is loaded')
    except IOError:
        # initialize
        matrix = pandas.DataFrame(
            numpy.zeros(shape=(len(author), len(author))))
        matrix = matrix.set_index(author.index.values)
        matrix.columns = author.index.values

        parse_link(matrix, metapath)

        # normalize the matrix
        row_sum = matrix.sum(axis=1)
        matrix = matrix.div(row_sum.ix[0], axis='columns')

        matrix.to_csv(filepath)
        # print('matrix is saved')

    return matrix


def p_pagerank(qid, adjacency, author):
    # create preference vector u
    preference = pandas.DataFrame(
        numpy.zeros(shape=(len(author), 1)))
    preference.loc[qid] = 1

    # initialize scores vector v
    score = pandas.DataFrame(
        numpy.ones(shape=(len(author), 1)))
    score = score / len(author)

    # iterate
    t = constants.ITERATION_TIME
    while(t > 0):
        t -= 1
        score = adjacency.dot(score) * (1 - constants.TELEPORT) + (
            constants.TELEPORT * preference)

    return score


def top_k_similar(qid, k, adjacency, author):
    similar = p_pagerank(qid, adjacency, author)

    similar.sort_values(inplace=True, ascending=False)
    return similar[0:k]


def print_result(result, author):
    for similar_aid, score in result.iteritems():
        print(author.loc[similar_aid][1])
        # print(similar_aid, score)

author = read_author()

adjacencyAPVPA = create_adjacency_matrix('APVPA', author)
print('adjacency matrix for APVPA is created')

print('\nThe top similar authors to A. Apple using APVPA are:\n')
result = top_k_similar(42166, 5, adjacencyAPVPA, author)
print_result(result, author)

# print('\nThe top similar authors to Christos Faloutsos using APVPA are:\n')
# result = top_k_similar(68855, 10, adjacencyAPVPA, author)
# print_result(result, author)

# print('\nThe top similar authors to AnHai Doan using APVPA are:\n')
# 51360
# 'APVPA'

adjacencyAPTPA = create_adjacency_matrix('APTPA', author)
print('adjacency matrix for APTPA is created')

print('\nThe top similar authors to A. Apple using APVPA are:\n')
result = top_k_similar(42166, 5, adjacencyAPTPA, author)
print_result(result, author)

# print('\nThe top similar authors to Xifeng Yan using APTPA are:\n')
# 66631
# 'APTPA'

# print('\nThe top similar authors to Jamie Callan using APTPA are:\n')
# 59090
# 'APTPA'
