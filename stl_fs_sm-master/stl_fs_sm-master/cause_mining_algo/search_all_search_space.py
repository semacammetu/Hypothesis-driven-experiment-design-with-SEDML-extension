from optimization import formula_search
from .helper_funs import concat_with_or_infix
from constants import stl_constants
from trace_checker import formula_generator
from itertools import combinations
from itertools import product
from itertools import chain
from collections import namedtuple
from trace_checker import STL

def my_iterable():
    # function to initialize an empty iterable
    for i in []:
        yield i

def search_all_search_space(metric_list, control_metrics, set_valued_metrics, parameter_domains, folder_name,
                            trace_count, signal_file_base, process_count, return_type, oc_limit, cause_limit, upto=True,
                            withoutS=False, controllable_formulas=True, time_shift=0):
    """

    Designed as a function to understand how true and efficient our cause_mining heuristic works. This function searches
    through the whole search space (until operator_count == n) and is guaranteed to find the best formula.

    This function tries to search through all search space in a pretty naive way, going through all possible
    cause_mining formulas in all possible "concatenated with or's" forms, iterating through operator counts in an increasing
    manner. Without dictating the heurisic -which is putting an hierarchy to the business of searching through the same
    formed formulas, and some restrictions of course- in the algorithm in cause_mining_for_traffic_data, in a very
    loose way.

    Args:
        metric_list:
        control_metrics:
        set_valued_metrics:
        parameter_domains:
        folder_name:
        trace_count:
        signal_file_base:
        process_count:
        return_type:
        oc_limit: operator count. The computation stops when operator count reaches the value n+1.
        cause_limit: the max number of formula component in the end formula
        upto: (bool) if True, the formulas with up to cause_limit many components,
                     if False, the formulas with exactly cause_limit many components are searched for.
        controllable_formulas: (bool) if True, the function calls generate_formula_tree_for_cause_mining,
                                if False, it calls generate_formula_tree_iterative. So in the first case controllable
                                formulas are generated, in the second case all formulas are.

    Returns: best_result type: FormulaValuation

    """

    best_result = stl_constants.FormulaValuation(formula="", valuation=0)  # initialize

    # find all formulas till oc = n+1
    all_formulas_till_n = []
    if controllable_formulas:
        all_formulas_till_n = all_formulas_till_n + \
                              formula_generator.generate_formula_tree_for_cause_mining(metric_list=metric_list,
                                                                                       control_metrics=control_metrics,
                                                                                       operator_count=oc_limit,
                                                                                       set_valued_metrics=set_valued_metrics,
                                                                                       withoutS=withoutS)
    else:
        all_formulas_till_n = all_formulas_till_n + \
                              formula_generator.generate_formula_tree_iterative(metric_list=metric_list,
                                                                                operator_count=oc_limit,
                                                                                return_formula_string=True,
                                                                                set_valued_metrics=set_valued_metrics,
                                                                                withoutS=withoutS)
        if time_shift > 0:
            time_shift_str = str(time_shift) + " " + str(time_shift)
            all_formulas_till_n = ['P ' + time_shift_str + " ( " + f + " )" for f in all_formulas_till_n]
    # find all combinations of these formulas and concatenate all with or
    iter_all_combinations = my_iterable()
    if not upto:
        iter_all_combinations = chain(iter_all_combinations, product(all_formulas_till_n, repeat=cause_limit))
    else:
        for n in range(1, cause_limit+1):
            iter_all_combinations = chain(iter_all_combinations, product(all_formulas_till_n, repeat=n))
        # now we have an iterator of all formulas up to cause_limit many components,

    all_comb_set = set()
    for i in iter_all_combinations:
        all_comb_set.add(frozenset(i))

    print("there are " + str(len(all_formulas_till_n)) + " formulas in all_formulas_till_" + str(oc_limit) + \
          " and cause limit is " + str(cause_limit) + " so there will be " + str(len(all_comb_set)) + \
          " formulas to be iterated over.")
    # concatenate the formulas with or and put them into a list
    concatenated_list = []
    cnt = 0
    for formula_set in all_comb_set:
        cnt += 1
        formula_list = list(formula_set)
        concatenated_list.append(concat_with_or_infix(formula_list))
        print("the formula number " + str(cnt) + " that we are on is: " + formula_list[0])
        # find the best parameter values for this formula
        formula, parameter_domains_for_formula = formula_search.generate_formula_from_template(
            template_formula=formula_list[0], parameter_domains=parameter_domains)
        formula_valuation = formula_search.parameter_search_for_formula(formula=formula,
                                                                        parameter_domains_for_formula=parameter_domains_for_formula,
                                                                        folder_name=folder_name,
                                                                        trace_count=trace_count,
                                                                        signal_file_base=signal_file_base,
                                                                        process_count=process_count,
                                                                        return_type=return_type)
        # make this formula the new best_result if its valuation is better than the old best_result
        if formula_valuation.valuation > best_result.valuation:
            best_result = formula_valuation
            print("\n\nBest Formula of search_all_search_space for now is " + best_result.formula + \
                  " with valuation " + str(best_result.valuation) + "\n The tuple in iteration is " + str(formula_list) \
                  + "\n")

    return best_result
