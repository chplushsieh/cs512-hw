import csv
import numpy
import pandas
import constants
import time


def get_type_from_xid(xid):
    typ = ''
    if constants.tmin <= xid <= constants.tmax:
        typ = constants.TERM
    elif constants.pmin <= xid <= constants.pmax:
        typ = constants.PAPER
    elif constants.vmin <= xid <= constants.vmax:
        typ = constants.VENUE
    elif constants.amin <= xid <= constants.amax:
        typ = constants.AUTHOR
    else:
        print('xid:', xid, 'has no matched type. ')

    return typ


def read_data(filename):
    return pandas.read_csv(
        constants.datapath + filename + '.txt',
        sep='\t', index_col=0, header=None)


def create_matrixPX(paper, x):
    matrixPX = pandas.DataFrame(numpy.zeros(shape=(len(paper), len(x))))
    matrixPX = matrixPX.set_index(paper.index.values)
    matrixPX.columns = x.index.values
    return matrixPX


def set_relation(matrixPT, matrixPV, matrixPA):
    with open(constants.datapath + 'relation.txt', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')

        for row in reader:
            pid, xid, _ = row
            pid = int(pid)
            xid = int(xid)

            xtype = get_type_from_xid(xid)
            if xtype == constants.TERM:
                matrixPT.loc[pid, xid] += 1
            elif xtype == constants.VENUE:
                matrixPV.loc[pid, xid] += 1
            elif xtype == constants.AUTHOR:
                matrixPA.loc[pid, xid] += 1
            else:
                print('xid:', xtype, 'has no matched type. ')


def create_data():
    author = read_data(constants.AUTHOR)
    term = read_data(constants.TERM)
    venue = read_data(constants.VENUE)

    paper = read_data(constants.PAPER)
    return author, term, venue, paper


def create_matrices(author, term, venue, paper):
    matrixPT = create_matrixPX(paper, term)
    matrixPV = create_matrixPX(paper, venue)
    matrixPA = create_matrixPX(paper, author)

    set_relation(matrixPT, matrixPV, matrixPA)
    return matrixPT, matrixPV, matrixPA


def create_matrixAPVPA(matrixPV, matrixPA):
    matrixAP = matrixPA.transpose()

    try:
        matrixAPV = pandas.DataFrame.from_csv(
            constants.datapath + 'matrixAPV.csv')
        # print('matrixAPV is loaded')
    except IOError:
        matrixAPV = matrixAP.dot(matrixPV)
        matrixAPV.to_csv(constants.datapath + 'matrixAPV.csv')
        # print('matrixAPV is saved')

    matrixVPA = matrixAPV.transpose()

    try:
        matrixAPVPA = pandas.DataFrame.from_csv(
            constants.datapath + 'matrixAPVPA.csv')
        matrixAPVPA.columns = matrixAPVPA.index.values
        # print('matrixAPVPA is loaded')
    except IOError:
        matrixAPVPA = matrixAPV.dot(matrixVPA)
        matrixAPVPA.to_csv(constants.datapath + 'matrixAPVPA.csv')
        # print('matrixAPVPA is saved')

    return matrixAPVPA


def create_matrixAPTPA(matrixPT, matrixPA):
    matrixAP = matrixPA.transpose()

    try:
        matrixAPT = pandas.DataFrame.from_csv(
            constants.datapath + 'matrixAPT.csv')
        # print('matrixAPT is loaded')
    except IOError:
        matrixAPT = matrixAP.dot(matrixPT)
        matrixAPT.to_csv(constants.datapath + 'matrixAPT.csv')
        # print('matrixAPT is saved')

    matrixTPA = matrixAPT.transpose()

    try:
        matrixAPTPA = pandas.DataFrame.from_csv(
            constants.datapath + 'matrixAPTPA.csv')
        matrixAPTPA.columns = matrixAPTPA.index.values
        # print('\nmatrixAPTPA is loaded')
    except IOError:
        matrixAPTPA = matrixAPT.dot(matrixTPA)
        matrixAPTPA.to_csv(constants.datapath + 'matrixAPTPA.csv')
        # print('\nmatrixAPTPA is saved')

    return matrixAPTPA


def top_k_similar(aid, k, matrix):
    similar = matrix.loc[aid].copy()
    for other_aid in similar.index:
        similar[other_aid] = 2 * matrix.loc[aid][other_aid] / (
            matrix.loc[aid][aid] + matrix.loc[other_aid][other_aid])

    similar.sort_values(inplace=True, ascending=False)

    return similar[0:k]


def print_result(result, author):
    for similar_aid, score in result.iteritems():
        print(author.loc[similar_aid][1])
        # print(similar_aid, score)

preprocessing_start = time.process_time()

author, term, venue, paper = create_data()
matrixPT, matrixPV, matrixPA = create_matrices(author, term, venue, paper)
# print('\n matrixPT, matrixPV, matrixPA done \n')

preprocessing_done = time.process_time()
print('Preprocessing takes %.2f sec. ' % (
    preprocessing_done - preprocessing_start))

matrixAPVPA = create_matrixAPVPA(matrixPV, matrixPA)

APVPA_done = time.process_time()
print('\nCreating matrixAPVPA takes %.2f sec. ' % (
    APVPA_done - preprocessing_done))

matrixAPTPA = create_matrixAPTPA(matrixPT, matrixPA)

APTPA_done = time.process_time()
print('\nCreating matrixAPTPA takes %.2f sec. ' % (
    APTPA_done - APVPA_done))

print('\nThe top similar authors to Christos Faloutsos using APVPA are:\n')
result = top_k_similar(68855, 10, matrixAPVPA)
print_result(result, author)

print('\nThe top similar authors to AnHai Doan using APVPA are:\n')
result = top_k_similar(51360, 10, matrixAPVPA)
print_result(result, author)

print('\nThe top similar authors to Xifeng Yan using APTPA are:\n')
result = top_k_similar(66631, 10, matrixAPTPA)
print_result(result, author)

print('\nThe top similar authors to Jamie Callan using APTPA are:\n')
result = top_k_similar(59090, 10, matrixAPTPA)
print_result(result, author)

query_done = time.process_time()
print('\nThe above queries take %.2f sec. ' % (
    query_done - APTPA_done))
