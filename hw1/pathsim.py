import csv
from collections import namedtuple
import constants
import numpy
import pandas

Entry = namedtuple('Entry', 'idx name')


def get_type_from_idx(idx):
    typ = ''
    if constants.tmin <= idx <= constants.tmax:
        typ = constants.T
    elif constants.pmin <= idx <= constants.pmax:
        typ = constants.P
    elif constants.vmin <= idx <= constants.vmax:
        typ = constants.V
    elif constants.amin <= idx <= constants.amax:
        typ = constants.A
    else:
        print('idx:', idx, 'has no matched type. ')

    return typ


def read_relations():
    relations = dict()

    with open(constants.datapath + 'relation.txt', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')

        for row in reader:
            paper_idx, other_idx, _ = row
            paper_idx = int(paper_idx)
            other_idx = int(other_idx)
            # print('paper_idx: ', paper_idx, 'other_idx: ', other_idx)

            if paper_idx not in relations:
                relations[paper_idx] = {
                    constants.A: [], constants.T: [], constants.V: []}

            other_type = get_type_from_idx(other_idx)
            if other_type == constants.A:
                relations[paper_idx][constants.A].append(other_idx)
            elif other_type == constants.T:
                relations[paper_idx][constants.T].append(other_idx)
            elif other_type == constants.V:
                relations[paper_idx][constants.V].append(other_idx)
            else:
                print("Line: " + str(reader.line_num) + "matchs nothing. ")

    # print('relations:', relations)
    return relations


def read_file(filename):
    entries = []
    entries_dict = dict()

    with open(constants.datapath + filename + '.txt', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')

        for row in reader:
            idx, name = row
            idx = int(idx)
            # print('idx: ', idx, 'name: ', name)

            # build entries
            entry = Entry(idx, name)
            entries.append(entry)

            # build entries_dict
            entries_dict[idx] = reader.line_num - 1  # make it zero-based
    return (entries, entries_dict)


def idx2line_num(idx_lst, entries_dict):
    return [entries_dict[idx] for idx in idx_lst]


def get_xs_from_paper(type_x, paper_idx, xs_dict, relations):
    relation = relations[paper_idx]

    xs_idx_lst = relation[type_x]
    # return xs_idx_lst  # TODO if label is set properly
    xs_line_num = idx2line_num(xs_idx_lst, xs_dict)

    return xs_line_num


def construct_matrixPX(type_x, xs, xs_dict, papers, relations):
    matrix = pandas.DataFrame(numpy.zeros(shape=(len(papers), len(xs))))
    # print('matrix shape:', matrix.shape)

    # TODO read idx as matrix label
    for p_line_num, paper in enumerate(papers):
        # print('p_line_num=', p_line_num)
        xs_line_num = get_xs_from_paper(type_x, paper.idx, xs_dict, relations)

        for x_line_num in xs_line_num:
            # print('x_line_num=', x_line_num)
            # print('matrix[p_line_num]:', matrix[p_line_num])
            matrix[p_line_num][x_line_num] = 1

            # TODO if label is set properly
            # matrix[p_line_num].loc[x_idx] = 1

    # print('row_content: ', row_content)
    return matrix


def compute_other_similar_authors(author_idx, matrix):
    author_line_num_lst = idx2line_num([author_idx], authors_dict)
    author_line_num = author_line_num_lst[0]

    other_authors = matrix.loc[author_line_num, :]
    for other_line_num, other in enumerate(other_authors):
        other_authors[other_line_num] = 2*other_authors[other_line_num] / (
            matrix[author_line_num][author_line_num] +
            matrix[other_line_num][other_line_num])
    print('other_authors: ', other_authors)
    return other_authors


def top_k_similar_to(author_idx, k, matrix):
    other_authors = compute_other_similar_authors(author_idx, matrix)
    other_authors.sort(ascending=False)
    print('sorted other_authors: ', other_authors)


papers, papers_dict = read_file(constants.P)
# print('papers:', papers)
# print('papers_dict:', papers_dict)

authors, authors_dict = read_file(constants.A)
terms, terms_dict = read_file(constants.T)
venues, venues_dict = read_file(constants.V)

relations = read_relations()

matrixPA = construct_matrixPX(
    constants.A, authors, authors_dict, papers, relations)
matrixAP = matrixPA.transpose()
print('matrixAP:', matrixAP)

matrixPV = construct_matrixPX(
    constants.V, venues, venues_dict, papers, relations)
print('matrixPV:', matrixPV)

matrixAPV = matrixAP.dot(matrixPV)
print('matrixAPV:', matrixAPV)

matrixVPA = matrixAPV.transpose()
matrixAPVPA = matrixAPV.dot(matrixVPA)
print('matrixAPVPA:', matrixAPVPA)

top_k_similar_to(42166, 4, matrixAPVPA)
