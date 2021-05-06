
import time
import random

from trace_checker import STL
from constants import stl_constants
import cause_mining_algo as cma
from cause_mining_algo import cause_mining_heuristic
from cause_mining_algo import search_all_search_space
from cause_mining_algo import helper_funs
from cause_mining_algo import controller_helper_funs as hf
from signal_generation import sg
from . import syntactically_cosafe_form as scf


def cause_mining_for_basic_example(pc, valuation_limit, folder_name, trace_count, signal_file_base, return_type,
                                   operator_count_limit, withoutS=False, controllable_formulas=True):
    """
    Calls cause_mining_algorithm -with heuristic- from cause_mining_algo package with basic_example data.

    Returns: best formula in prefix form

    """
    print("---------------------------------------------------------------------------------------")
    print("                         cause_mining_for_basic_example ")
    print("---------------------------------------------------------------------------------------")
    start_time = time.time()
    save = False

    metric_list = ['0', '1']
    control_metrics = ['1']
    set_valued_metrics = ['1']
    parameter_domains = {'p0': range(3, 6, 1), 'p1': [-2, 1, 2],
                         'pA': range(0, 3, 1), 'pP': range(0, 3, 1), 'pS': range(0, 3, 1), 'pT': [1, 2]}
    result_file = 'min_max'
    strictly_increasing_oc = False
    best_result = cause_mining_heuristic.cause_mining_algorithm(metric_list=metric_list, control_metrics=control_metrics,
                                                                set_valued_metrics=set_valued_metrics,
                                                                parameter_domains=parameter_domains,
                                                                folder_name=folder_name, trace_count=trace_count,
                                                                signal_file_base=signal_file_base, process_count=pc,
                                                                save=save, result_file=result_file,
                                                                return_type=return_type,
                                                                strictly_increasing_oc=strictly_increasing_oc,
                                                                valuation_limit=valuation_limit,
                                                                operator_count_limit=operator_count_limit,
                                                                withoutS=withoutS,
                                                                controllable_formulas=controllable_formulas)  # type: FormulaValuation
                                                                                    # formula is in prefix form

    print('### --------end of cause mining for basic example -------- ### ')
    print("Best Result in prefix form : " + best_result.formula +\
          "\nBest Result in infix form: " + STL.prefix_to_infix(best_result.formula) + \
          "\nWith the Valuation : " + str(best_result.valuation))
    end_time = time.time()
    print("")
    print("---------------------------------------------------------------------------------------")
    print("cause_mining_for_basic_example ended in %s seconds" % str(end_time - start_time))
    print("---------------------------------------------------------------------------------------")
    print("folder name: " + folder_name)
    print("trace count: " + str(trace_count))
    print("processor count: " + str(pc))
    print("parameter domains: " + str(parameter_domains))
    print("return type: " + return_type.name)
    print("strictly increasing: " + str(strictly_increasing_oc))
    print("searched until operator count: " + str(operator_count_limit))

    return best_result.formula  # prefix formula


def search_all_search_space_for_basic_example(cause_limit, pc, return_type, operator_count_limit=-1, upto=True,
                                              withoutS=False, controllable_formulas=True):
    print("---------------------------------------------------------------------------------------")
    print("                           search_all_search_space_for_basic_example ")
    print("---------------------------------------------------------------------------------------")
    start_time = time.time()
    folder_name = 'test_data/basic_example_data/'
    trace_count = 20
    signal_file_base = 'test'
    metric_list = ['0', '1']
    control_metrics = ['1']
    set_valued_metrics = ['1']
    parameter_domains = {'p0': range(3, 6, 1), 'p1': [-2, 1, 2],
                         'pA': range(0, 3, 1), 'pP': range(0, 3, 1), 'pS': range(0, 3, 1), 'pT': [1, 2]}
    best_result = search_all_search_space.search_all_search_space(metric_list=metric_list,
                                                                  control_metrics=control_metrics,
                                                                  set_valued_metrics=set_valued_metrics,
                                                                  parameter_domains=parameter_domains,
                                                                  folder_name=folder_name, trace_count=trace_count,
                                                                  signal_file_base=signal_file_base,
                                                                  process_count=pc, return_type=return_type,
                                                                  oc_limit=operator_count_limit,
                                                                  cause_limit=cause_limit, upto=upto,
                                                                  withoutS=withoutS,
                                                                  controllable_formulas=controllable_formulas)  # type: FormulaValuation

    print('### --------end of silly search all search space for traffic data-------- ### ')
    print("Best Result is : " + best_result.formula + "\nWith the Valuation : " + str(best_result.valuation))

    print('### --------end of silly search all search space for traffic data-------- ### ')
    print("Best Result is : " + best_result.formula + "\nWith the Valuation : " + str(best_result.valuation))
    end_time = time.time()
    print("")
    print("---------------------------------------------------------------------------------------")
    print("search_all_search_space_for_basic_example ended in %s seconds" % str(end_time - start_time))
    print("---------------------------------------------------------------------------------------")
    print("folder name: " + folder_name)
    print("trace count: " + str(trace_count))
    print("processor count: " + str(pc))
    print("parameter domains: " + str(parameter_domains))
    print("return type: " + return_type.name)
    print("searched until operator count: " + str(operator_count_limit))
    return best_result.formula


def generate_basic_traces(folder_name, trace_count, duration):

    viol_formula = 'x0 < 5'

    stn_viol = STL.SyntaxTreeNode()
    stn_viol.initialize_node(viol_formula.split(), 0)

    tc = 0
    while tc < trace_count:
        f_signal_name = folder_name + "test_" + str(tc)
        f_label_name = f_signal_name + "_label"
        f_s = open(f_signal_name, 'w')
        f_l = open(f_label_name, 'w')

        time = 0
        x = [random.randint(5, 7)] # this line is to be uncommented if initial x is wanted to be randomized.
        #x = [0]
        while time <= duration:
            u = [random.choice([-2, 1, 2])]
            f_s.write(
                "%s %s %s\n" % (str(time), " ".join([str(x[0])]), " ".join([str(u[0])])))
            stn_viol.compute_qv(STL.DataPoint(value=x+u, time=time))
            qual = 1 if stn_viol.qv < 0 else 0
            f_l.write("%s %s\n" % (str(time), str(qual)))
            x, _ = basic_example_step_function(x, u)

            time += 1

        f_s.close()
        f_l.close()
        print("Done with generate basic traces, trace no" + str(tc))
        tc += 1

def basic_example_step_function(xk, uk):
    """

    Args:
        xk: (list) of length 1 -> the system input
        uk: (list) of length 1 -> the control input

    Returns: [next xk], uk (uk is unimportant, not going to be used)

    """

    x = xk[0] + uk[0]
    x = 0 if x < 0 else x
    x = 10 if x > 10 else x

    return [x], uk

def basic_example(heuristic):
    """
    finds the best formula with heuristic or search_all_search_space and applies controller refinement loop_count times.
    Args:
        heuristic: (bool) True -> search the best formula by heuristic algorithm,
                          False -> search the best formula bu search_all_search_space

    Returns: nothing

    """

    loop_count = 6

    folder_name = 'test_data/basic_example_data/'
    trace_count = 20
    duration = 100
    pc = 24
    return_type = stl_constants.__F_03_SCORE
    oc_limit = 0
    cause_limit = 1
    upto = False
    withoutS = True

    #for heuristic==True and print_detailed_results
    valuation_limit = 0.01
    signal_file_base = 'test'
    signal_file_rest = ''
    operator_count_limit = 1

    viol_formula = 'x0 < 5'
    viol_formula_prefix = STL.infix_to_prefix(viol_formula)
    uk_domain = [-2, 1, 2]
    uk_count = 1

    #generate random traces and check the label count
    generate_basic_traces(folder_name, trace_count, duration)
    label_cnt = hf.label_count(folder_name=folder_name, label_file_base='test_', label_file_rest='_label',
                               trace_count=trace_count)
    print("label count before the controller: " + str(label_cnt))
    formula_list = []
    for i in range(loop_count):

        if not heuristic:
            best_formula = search_all_search_space_for_basic_example(cause_limit=cause_limit, pc=pc,
                                                                    return_type=return_type,
                                                                    operator_count_limit=oc_limit, upto=upto,
                                                                    withoutS=withoutS)
            cause_formula_prefix = STL.infix_to_prefix(best_formula)

        else:
            cause_formula_prefix = cause_mining_for_basic_example(pc=pc, valuation_limit=valuation_limit,
                                                                 folder_name=folder_name,
                                                                 trace_count=trace_count,
                                                                 signal_file_base=signal_file_base,
                                                                 return_type=return_type,
                                                                 operator_count_limit=operator_count_limit,
                                                                 withoutS=withoutS)  # best formula in prefix form
        cma.cause_mining_main.print_detailed_result(prefix=1, formula=cause_formula_prefix, folder_name=folder_name,
                                                    signal_file_base=signal_file_base,
                                                    signal_file_rest=signal_file_rest, trace_count=trace_count)
        formula_list.append(cause_formula_prefix)
        cause_formula_prefix = helper_funs.concat_with_or_prefix(formula_list)

        sg.controller(folder_name=folder_name, name='test', trace_count=trace_count,  duration=duration,
                      viol_formula=viol_formula_prefix, cause_formula=cause_formula_prefix,
                      step_function=basic_example_step_function, xk_initialized=[0], uk_domain=uk_domain,
                      uk_count=uk_count, num_to_let=False)

        label_cnt = hf.label_count(folder_name=folder_name, label_file_base='test_', label_file_rest='_label',
                                   trace_count=trace_count)
        print("label count after controller " + str(i) + " is: " + str(label_cnt))

        if label_cnt == 0:
            break


def find_best_formula(heuristic, controllable_formulas=True):
    """

    Args:
        heuristic: (bool) True -> search the best formula by heuristic algorithm,
                          False -> search the best formula bu search_all_search_space

    Returns: the best formula in prefix form

    """
    folder_name = 'test_data/basic_example_data/'
    trace_count = 20
    duration = 100
    pc = 0
    return_type = stl_constants.__F_03_SCORE
    cause_limit = 1
    upto = False
    withoutS = True
    if  controllable_formulas:
        oc_limit_lhs = 1
        oc_limit_rhs = 0
        oc_limit = [oc_limit_lhs, oc_limit_rhs]
    else:
        oc_limit = 0

    # for heuristic==True and print_detailed_results
    valuation_limit = 0.01
    signal_file_base = 'test'
    signal_file_rest = ''
    operator_count_limit = 1


    print("operator_count_limit = " + str(oc_limit))
    print("pc = " + str(pc))
    print("return type = " + str(return_type.category))
    print("withoutS = " + str(withoutS))
    print("heuristic = " + str(heuristic))
    if heuristic:
        print("valuation_limit = " + str(valuation_limit))
    else:
        print("cause_limit = " + str(cause_limit))
        print("upto = " + str(upto))

    # generate random traces and check the label count
    generate_basic_traces(folder_name, trace_count, duration)

    if not heuristic:
        best_formula = search_all_search_space_for_basic_example(cause_limit=cause_limit, pc=pc,
                                                                 return_type=return_type,
                                                                 operator_count_limit=oc_limit, upto=upto,
                                                                 withoutS=withoutS, controllable_formulas=controllable_formulas)
        cause_formula_prefix = STL.infix_to_prefix(best_formula)

    else:
        cause_formula_prefix = cause_mining_for_basic_example(pc=pc, valuation_limit=valuation_limit,
                                                              folder_name=folder_name,
                                                              trace_count=trace_count,
                                                              signal_file_base=signal_file_base,
                                                              return_type=return_type,
                                                              operator_count_limit=operator_count_limit,
                                                              withoutS=withoutS, controllable_formulas=controllable_formulas)  # best formula in prefix form
    cma.cause_mining_main.print_detailed_result(prefix=1, formula=cause_formula_prefix, folder_name=folder_name,
                                                signal_file_base=signal_file_base,
                                                signal_file_rest=signal_file_rest, trace_count=trace_count)
    return cause_formula_prefix



def basic_example_main():
    #basic_example(heuristic=False)  # heuristic=True implies heuristic usage, heuristic=False implies search_all_search_space


    p_formula = find_best_formula(heuristic=True, controllable_formulas=False)
    X_formula = scf.return_sc_form(p_formula, prefix=True)
    formula_with_atomic_props, dict = scf.turn_inequalities_to_atomic_propositions(X_formula)
    print(formula_with_atomic_props, dict)
