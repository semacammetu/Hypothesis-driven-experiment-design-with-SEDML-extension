from trace_checker import STL
from constants import stl_constants
import optimization
import re

def traverse_formula_check_intervals(stn):
    """

    Traverses the formula tree and returns True if all intervals are within the necessary limits, i.e.
    for A,P,S: the least bound < the upper bound,
    Returns False otherwise.

    """
    if not stn:
        return True
   # if stn.op == 'S' and stn.interval.lb != 0:  # Irmak Dikkat. S'nin lb'sini 0 olarak fixliyor.
        #  Bunu yapmak istemeyebiliriz. Istesek bile bu cok verimsiz bir yol, A'daki gibi fixleyecegiz.
    #    return False
    if (stn.op == 'A' or stn.op == 'P' or stn.op == 'S') and stn.interval.lb > stn.interval.ub:
        return False
    # if stn.op == 'A' and stn.interval.ub == 0:
    #     return False
    if not (stn.left_node or stn.right_node):
        return True
    return traverse_formula_check_intervals(stn.left_node) and traverse_formula_check_intervals(stn.right_node)


def formula_val_list_into_concat_formula_list(prefix_formula_val_list, folder_name, signal_file_base, trace_count,
                                              signal_file_rest, return_type):
    """
    Designed for debug purposes of cause mining algorithm
    Takes only the formula parts of a Formula_Valuation list, turns them into their infix forms,
    concatenates them with or and calculates the valuation of the resulting formula. Returns the resulting formula and
    the valuation as a FormulaValuation.
    Args:
        prefix_formula_val_list: A list of Formula Valuations where formulas are in prefix forms.
         Ex: [FormulaValuation(formula='A 0 4 x5 = 0', valuation=0.7824),
         FormulaValuation(formula='& A 0 2 x5 = 0 P 1 1 x3 > 10', valuation=0.921521)]
        return_type:

    Returns: a FormulaValuation

    """
    infix_formula_list = [fv.formula for fv in prefix_formula_val_list]
    prefix_to_infix_list(infix_formula_list)
    concat_with_or_infix(infix_formula_list)
    formula = STL.infix_to_prefix(infix_formula_list[0])
    valuation = optimization.evaluator.evaluate_signals(formula, folder_name, signal_file_base, trace_count,
                                                        signal_file_rest, return_type)
    return stl_constants.FormulaValuation(formula=infix_formula_list[0], valuation=valuation)


def print_past_formulas_prefix_infix_valuation(past_results, folder_name, signal_file_base, trace_count,
                                               signal_file_rest, return_type):
    """
        Debugging tool for past formulas.
        Calls formula_val_list_into_concat_formula_list and calculates the resulting formula from past_results list
         (or any FormulaValuation list with formulas in prefix forms), returns the prefix and infix form and the
         valuation of the resulting formula
    """

    forVal = formula_val_list_into_concat_formula_list(past_results, folder_name, signal_file_base, trace_count,
                                                       signal_file_rest, return_type)
    print("Infix Formula: " + forVal.formula)
    print("Prefix Formula: " + STL.infix_to_prefix(forVal.formula))
    print("Valuation: " + str(forVal.valuation))


def concat_with_or_prefix(formula_list):
    """

    Args:
        formula_list: prefix formula list

    Returns: a prefix version of the concatenated (with | ) form of the formulas in formula_list

    """
    if len(formula_list) == 1:
        return formula_list[0]
    length = len(formula_list)
    resulting_formula = "| "*(length-2) + "|"
    for i in range(0, length):
        resulting_formula += " " + formula_list[i]
    return resulting_formula


def concat_with_or_infix(formula_list):
    """
    Probably is buggy
    Written as a helper function for search_all_search_space function.
    Args:
        formula_list: list of infix formulas to be concatenated with or. For example, for
        formula_list=['( A 0 pA ( x6 = p6 ) ) & ( ( x0 > p0 ) | ( x2 > p2 ) )','( A 0 pA ( x6 = p6 ) ) & ( x0 > p0 )'],
        result is '( ( A 0 pA ( x6 = p6 ) ) & ( ( x0 > p0 ) | ( x2 > p2 ) ) | ( A 0 pA ( x6 = p6 ) ) & ( x0 > p0 ) )'
    Returns: result (infix formula) type: String

    Note: as a side effect, it turns the input list formula_list into a list with one element, which is the result

    """
    length = len(formula_list)
    if length == 1:
        return formula_list[0]
    else:
        formula1 = formula_list[0]
        formula2 = formula_list[1]
        concat_formula = '( ( ' + formula1 + ' ) | ( ' + formula2 + ' ) )'
        formula_list.pop(0)
        formula_list.pop(0)
        formula_list.append(concat_formula)
        return concat_with_or_infix(formula_list)


def prefix_to_infix_list(prefix_list):
    """
    Changes prefix formulas in a list to their infix forms

    Args:
        prefix_list: list of prefix formulas

    Returns: nothing

    """
    length = len(prefix_list)
    for i in range(0, length):
        prefix_list.append(STL.prefix_to_infix(prefix_list[0]))
        prefix_list.pop(0)

def count_formula_components(prefix_concatenated_formula):
    """
    This function is used in one, not very important place. I suspect that it count only the number of | operations that
    occur in the formula's string form rather than counting how many cause formulas concatanated with | form up this
    formula. It is not important since its usage is non-essential in the cause mining code, but if it will be used in
    an important piece of code, it should be rewritten.
    Args:
        prefix_concatenated_formula: (string)

    Returns:

    """
    formula_count = 0
    for i in range(len(prefix_concatenated_formula)):
        if prefix_concatenated_formula[i] == '|':
            formula_count += 1
        elif prefix_concatenated_formula[i] == ' ':
            continue
        else:
            break
    return formula_count