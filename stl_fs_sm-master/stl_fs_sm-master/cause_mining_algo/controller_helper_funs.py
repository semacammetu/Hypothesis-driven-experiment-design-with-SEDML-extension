import re
from trace_checker import STL
import copy

"""
helper functions for controller construction
"""

def break_formula(cause_formula):
    """
    Breaks a cause formula Phi = Phi_1 | Phi_2 | ... | Phi_n into an array formula_list = [Phi_1, Phi_2, ..., Phi_n]
    where Phi_i = A[1,a](u_i = c_i) & P[1,1] (phi_i)
    Args:
        cause_formula:
    Returns: stn_list of all formula components of the given concatenated formula

    """
    stn = STL.SyntaxTreeNode()
    stn.initialize_node(cause_formula.split(), 0)
    return break_formula_helper(stn)


def break_formula_helper(stn):
    """
    Args:
        stn: (of cause formula)
    Returns: stn_list of all formula components of the given concatenated formula

    """
    broken_formula_list = []
    if not (stn.op == '|'):
        return [stn]
    broken_formula_list += break_formula_helper(stn.left_node)
    broken_formula_list += break_formula_helper(stn.right_node)
    return broken_formula_list


def give_formula_components(formulalist):
    """
    Takes a formula list of the form formula_list = [Phi_1, Phi_2, ..., Phi_n] for a cause formula Phi = Phi_1 | Phi_2 | ... | Phi_n
    where Phi_i = A[1,a](u_i = c_i) & P[m,m] (phi_i).
    (which is the output of break_formula(cause_formula)
    returns a 2 dimensional array formula_components:
    A[0,a_0-2] (u_0 = c_0)   P[m-1,m-1] phi_0
    A[0,a_1-2] (u_1 = c_1)   P[m-1,m-1] phi_1
    ...
    A[0,a_n-2] (u_n = c_n)   P[m-1,m-1] phi_n # if m = 1 phi_n instead of P[0,0] phi_n

    Args:
        formulalist: stn list of cause formulas

    Returns: formula_components (2 dimensional array of stns)


    """
    formula_list = copy.deepcopy(formulalist)
    formula_components = [[None for x in range(0, 2)] for y in range(len(formula_list))]
    for i in range(0, len(formula_list)):
        if formula_list[i].op == '&':
            formula_components[i][0] = formula_list[i].left_node
        else:
            formula_components[i][0] = formula_list[i]
        if formula_components[i][0].interval.lb == 1:  # just double checking, it is always 1
            formula_components[i][0].interval.lb = 0
        else:
            raise Exception('least bound of A on lefthand side should have been 1, but it is not. WHY?!?!? it is:', formula_components[i][0].interval.lb )
        formula_components[i][0].interval.ub -= 2
        if formula_list[i].op == '&':
            if not formula_list[i].right_node.interval.lb == formula_list[i].right_node.interval.ub:
                raise Exception('P n n condition is not satisfied, least bound of P is different from its upper bound')
            if formula_list[i].right_node.interval.lb == 1:
                formula_components[i][1] = formula_list[i].right_node.left_node
            else:
                formula_components[i][1] = formula_list[i].right_node
                formula_components[i][1].interval.lb -= 1
                formula_components[i][1].interval.ub -= 1

    return formula_components


def label_count(folder_name, label_file_base, label_file_rest, trace_count):
    """
    count 1 labeled data points in the files in a folder
    Returns: violation_count (integer)

    """
    i = 0
    viol_cnt = 0
    for i in range(0, trace_count):
        label_file_name = folder_name + label_file_base + str(i) + label_file_rest
        with open(label_file_name, 'r') as lf:
            contents = lf.read()
            contents = re.split('\n| ', contents)
            viol_cnt += -1 + (contents.count('1'))
    return viol_cnt

def file_label_count(label_file_name):
    """
    finds label count of the given file_name
    """
    viol_cnt = 0
    with open(label_file_name, 'r') as lf:
        contents = lf.read()
        contents = re.split('\n| ', contents)
        viol_cnt += -1 + (contents.count('1'))
    return viol_cnt

def safe_remove(initial_list, value):

    list_removed = copy.deepcopy(initial_list)
    try:
        list_removed.remove(value)
    except ValueError:
        pass
    return list_removed