from trace_checker import STL
from trace_checker import formula_utilities as U


def return_next_form(stn):
    """

    Args:
        stn: stn of the formula to be written in next form.

    Returns: next form of formula

    """
    if stn.op in U.MetricOperators:
        return ' ( ' + stn.to_formula() + ' ) '
    elif stn.op in U.BooleanOperators:
        if U.is_binary(stn.op):
            return ' ( ' + return_next_form(stn.left_node) + ' ' + stn.op + ' ' + return_next_form(stn.right_node) + ' ) '
        else:  # if op == '!'
            return ' ( ! ' + return_next_form(stn.left_node) + ' ) '
    elif stn.op in U.STLPastOperators:
        if stn.op == 'P':
            sign = ' | '
        elif stn.op == 'A':
            sign = ' & '
        else:
            print(" didn't make the arrangements yet for since")

        strn = ' ( '
        strn_left_node = return_next_form(stn.left_node)
        for i in range(stn.interval.lb, stn.interval.ub+1):
            if i == stn.interval.lb:
                strn += 'X '*i + ' ( ' + strn_left_node + ' ) '
            else:
                strn += sign + 'X '*i + ' ( ' + strn_left_node + ' ) '
        strn += ' ) '

    return strn

def  return_sc_form(formula, prefix=True):
    """

    Args:
        formula: formula to be written with "next" statements
        prefix:  bool value that indicates whether the given formula is prefix or infix

    Returns: formula written with only X and !. For example, return_sc_form('P 1 1 ( x0 = 0 ))', False) = 'X (x0=0.0)'

    """

    if not prefix:
        formula = STL.infix_to_prefix(formula)
    stn = STL.SyntaxTreeNode()
    stn.initialize_node(formula.split(), 0)

    next_form_str = return_next_form(stn)
    #print(next_form_str)
    return next_form_str


def turn_inequalities_to_atomic_propositions(formula):
    """

    Args:
        formula: string formula with X (next) and linear inequalities (such as x0 < 5, x1 = 8) only

    Returns: the formula replacing the linear equailities with p(0-9) namely atomic propositions and a dictionary
     giving the mapping of atomic propositions and the corresponding inequalities
     For example,  inp:  ( X ( x5 = 0.0 ) )  &  ( X  ( X ( ( x3 > 10.0 ) | ( x0 = 1 ) )  & X X  ( X ( x3 > 10.0 ) )  )
                   outp: Xp0 & XXp1 | XXp2 & XXXp1, {'x5 = 0.0':'p0', 'x3 > 10.0':'p1', '( x0 = 1 )':'p2'}

    """
    formula0 = formula.replace(" ", "")
    proposition_no = 0
    proposition_dictionary = {}
    new_formula = ""

    while formula0.count('(') > 0 :
        new_formula = ""

        X_cnt = 0
        index = 0
        while index < len(formula0):
            if not formula0[index] == '(':
                new_formula += formula0[index]
                if formula0[index] == 'X':
                    X_cnt += 1
                else:
                    X_cnt = 0
            if formula0[index] == '(':
                atomic_flag = True
                op_flag = False
                par_cnt = 1  # count of open parantheses
                i = index
                while par_cnt != 0:
                    i += 1
                    st = formula0[i]
                    new_formula += st
                    if (st == '&' or st == '|') and par_cnt == 1:  # add X in front of binary op iff open paranthesis count is 1, i.e. X effects directly this operator
                        op_flag = True
                    if st == '(' or st == '[':
                        par_cnt += 1
                    elif st == ')' or st == ']':
                        par_cnt -= 1
                        if par_cnt == 0:
                            new_formula = new_formula[:-1]
                    if par_cnt == 2 and atomic_flag:
                        atomic_flag = False
                if atomic_flag:  # formula[index+1:i-1] does not contain any parantheses, thus is an atomic proposition
                    dict_key = formula0[index+1:i]
                    if dict_key in proposition_dictionary:
                        dict_value = proposition_dictionary[dict_key]
                    else:
                        dict_value = 'p' + str(proposition_no)
                        proposition_dictionary[dict_key] = dict_value
                        proposition_no += 1
                    new_formula = new_formula.replace(dict_key, dict_value, 1)

                if op_flag:
                    new_formula = new_formula.replace(formula0[index+1:i], '[' + formula0[index+1:i] + ']', 1)
                new_formula += formula0[i+1:]
                formula0 = new_formula
                break
            index += 1

    new_formula = new_formula.replace('[', ' ( ', new_formula.count('['))
    new_formula = new_formula.replace(']', ' ) ', new_formula.count(']'))
    new_formula = new_formula.replace('p', ' p', new_formula.count('p'))
    new_formula = new_formula.replace('&', ' & ', new_formula.count('&'))
    new_formula = new_formula.replace('|', ' | ', new_formula.count('|'))
    new_formula = new_formula.replace('!', ' ! ', new_formula.count('!'))
    new_formula = new_formula.replace('  ', ' ', new_formula.count('  '))
    new_formula = new_formula.replace('  ', ' ', new_formula.count('  '))
    if new_formula[0] == ' ':
        new_formula = new_formula[1:]
    if new_formula[-1] == ' ':
        new_formula = new_formula[:-1]

    return new_formula, proposition_dictionary
