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
                matrixPT.loc[pid][xid] += 1
            elif xtype == constants.VENUE:
                matrixPV.loc[pid][xid] += 1
            elif xtype == constants.AUTHOR:
                matrixPA.loc[pid][xid] += 1
            else:
                print('xid:', xtype, 'has no matched type. ')


def create_matrices():
    author = read_data(constants.AUTHOR)
    term = read_data(constants.TERM)
    venue = read_data(constants.VENUE)

    paper = read_data(constants.PAPER)

    matrixPT = create_matrixPX(paper, term)
    matrixPV = create_matrixPX(paper, venue)
    matrixPA = create_matrixPX(paper, author)

    set_relation(matrixPT, matrixPV, matrixPA)
    return matrixPT, matrixPV, matrixPA


def top_k_similar(aid, k, matrix):
    similar = matrix.loc[aid].copy()
    for other_aid in similar.index:
        similar[other_aid] = 2 * matrix.loc[aid][other_aid] / (
            matrix.loc[aid][aid] + matrix.loc[other_aid][other_aid])

    similar.sort_values(inplace=True, ascending=False)
    return similar[0:k]

create_matrices_start = time.time()
matrixPT, matrixPV, matrixPA = create_matrices()
# print('matrixPT:', matrixPT)
# print('matrixPV:', matrixPV)
# print('matrixPA:', matrixPA)
print('\n matrixPT, matrixPV, matrixPA done \n')
create_matrices_end = time.time()
print('Time spent:', create_matrices_end - create_matrices_start)

matrixAP = matrixPA.transpose()

matrixAPV_start = time.time()
try:
    matrixAPV = pandas.DataFrame.from_csv(constants.datapath + 'matrixAPV.csv')
    print('\nmatrixAPV is loaded')
except IOError:
    matrixAPV = matrixAP.dot(matrixPV)
    matrixAPV.to_csv(constants.datapath + 'matrixAPV.csv')
    print('\nmatrixAPV is saved')
matrixAPV_end = time.time()
print('Time spent:', matrixAPV_end - matrixAPV_start)

matrixVPA = matrixAPV.transpose()

matrixAPVPA_start = time.time()
try:
    matrixAPVPA = pandas.DataFrame.from_csv(
        constants.datapath + 'matrixAPVPA.csv')
    matrixAPVPA.columns = matrixAPVPA.index.values
    print('\nmatrixAPVPA is loaded')
except IOError:
    matrixAPVPA = matrixAPV.dot(matrixVPA)
    matrixAPVPA.to_csv(constants.datapath + 'matrixAPVPA.csv')
    print('\nmatrixAPVPA is saved')
matrixAPVPA_end = time.time()
print('Time spent:', matrixAPVPA_end - matrixAPVPA_start)

# print('\matrixAPVPA:\n', matrixAPVPA)
print('\nThe top similar ones using APVPA are:\n')
print(top_k_similar(42166, 2, matrixAPVPA))

matrixAPT_start = time.time()
try:
    matrixAPT = pandas.DataFrame.from_csv(constants.datapath + 'matrixAPT.csv')
    print('\nmatrixAPT is loaded')
except IOError:
    matrixAPT = matrixAP.dot(matrixPT)
    matrixAPT.to_csv(constants.datapath + 'matrixAPT.csv')
    print('\nmatrixAPT is saved')
matrixAPT_end = time.time()
print('Time spent:', matrixAPT_end - matrixAPT_start)

matrixTPA = matrixAPT.transpose()

matrixAPTPA_start = time.time()
try:
    matrixAPTPA = pandas.DataFrame.from_csv(
        constants.datapath + 'matrixAPTPA.csv')
    matrixAPTPA.columns = matrixAPTPA.index.values
    print('\nmatrixAPTPA is loaded')
except IOError:
    matrixAPTPA = matrixAPT.dot(matrixTPA)
    matrixAPTPA.to_csv(constants.datapath + 'matrixAPTPA.csv')
    print('\nmatrixAPTPA is saved')
matrixAPTPA_end = time.time()
print('Time spent:', matrixAPTPA_end - matrixAPTPA_start)

# print('\nmatrixAPTPA:\n', matrixAPTPA)
print('\nThe top similar ones using matrixAPTPA are:\n')
print(top_k_similar(42166, 2, matrixAPTPA))
