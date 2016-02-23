import csv
from collections import namedtuple
import constants
import numpy

Entry = namedtuple('Entry', 'idx name')

def get_type_from_idx(idx):

    # TODO
    if idx:
        typ = constants.A:
    elif idx:
        typ = constants.T:
    elif idx:
        typ = constants.V:
    pass

def read_relations():
    relations = dict()

    with open('dblp_4area/relation.txt', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')

        for row in reader:
            paper_idx, other_idx, _ = row
            print('paper_idx: ', paper_idx, 'other_idx: ', other_idx)

            if get_type_from_idx(other_idx) == constants.A:
                relations[paper_idx]
            elif get_type_from_idx(other_idx) == constants.T:
                pass
            elif get_type_from_idx(other_idx) == constants.V:
                pass
            else:
                print("Line: " + row + " in relation.txt matchs nothing. ")

    return relations


def read_file(filename):
    entries = []

    with open('dblp_4area/' + filename + '.txt', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='\t')

        for row in reader:
            idx, name = row
            print('idx: ', idx, 'name: ', name)
            entry = Entry(idx, name)
            entries.append(entry)

            # TODO build entries_dict
    return (entries, entries_dict)


def idx2line_num(idx_lst, entries_dict):
    return [entries_dict[idx] for idx in idx_lst]


def get_xs_from_paper(type_x, paper_idx, xs_dict, relations):
    relation = relations[paper_idx]

    if type_x == constants.A:
        xs_idx_lst = relation.authors
    elif type_x == constants.T:
        xs_idx_lst = relation.terms
    elif type_x == constants.V:
        xs_idx_lst = relation.venue
    else:
        print("Wrong Constant Type")

    xs_line_num = idx2line_num(xs_idx_lst, xs_dict)

    return xs_line_num


def construct_matrixPX(type_x, relations):
    papers, papers_dict = read_file(constants.P)
    xs, xs_dict = read_file(type_x)

    matrix = numpy.zeros((len(papers), len(xs)))
    for p_line_num, paper in enumerate(papers):
        xs_line_num = get_xs_from_paper(type_x, paper.idx, xs_dict, relations)

        for x_line_num in xs_line_num:
            matrix[p_line_num][x_line_num] = 1

    # print('row_content: ', row_content)
    return matrix


authors, authors_dict = read_file(constants.P)
terms, terms_dict = read_file(constants.P)
venues, venues_dict = read_file(constants.P)

relations = read_relations()

matrixPA = construct_matrixPX(constants.A, relations)
matrixAP = matrixPA.transpose()
matrixPV = construct_matrixPX(constants.V, relations)

matrixAPV = matrixAP * matrixPV
matrixVPA = matrixAPV.transpose()
matrixAPVPA = matrixAPV * matrixVPA
