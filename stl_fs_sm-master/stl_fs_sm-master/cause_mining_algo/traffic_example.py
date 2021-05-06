from optimization import evaluator
from optimization import grid_search
from optimization import formula_search
from trace_checker import STL
from signal_generation import generator
from constants import stl_constants
from cause_mining_algo import cause_mining_heuristic
from cause_mining_algo import search_all_search_space
from trace_checker import formula_generator
from cause_mining_algo import helper_funs
from cause_mining_algo import controller_helper_funs as hf
from signal_generation import sg
import cause_mining_algo as cma
from . import cause_mining_main as cmm

import time
import random
import numpy as np

from . import syntactically_cosafe_form as scf

# must be uncommented before calling traffic_example_main
import network # why are they red but not give out an error?
#import read_input



def traffic_signal_generator(folder_name, pc):
    # This function uses the package "signal_generation". This is for "cause mining."
    # generates new traffic_signal data with given violation_formula, trace_count and duration.
    #viol_formula = "( ( ( ( ( x0 < 30 ) & ( x1 < 30 ) ) & ( x2 < 30 ) ) & ( x3 < 15 ) ) & ( x4 < 15 ) )"
    #viol_formula_no_soln = "( ( ( ( ( x0 < 32 ) & ( x1 < 32 ) ) & ( x2 < 32 ) ) & ( x3 < 16 ) ) & ( x4 < 16 ) )"
    #viol_formula_no_soln2 = "( ( ( ( ( x0 < 30 ) & ( x1 < 30 ) ) & ( x2 < 30 ) ) & ( x3 < 15 ) ) & ( x4 < 15 ) )"
    viol_formula_no_soln3 = "( ( ( ( ( x0 < 30 ) & ( x1 < 30 ) ) & ( x2 < 30 ) ) & ( x3 < 15 ) ) & ( x4 < 15 ) )"
    viol_formula_prefix = STL.infix_to_prefix(viol_formula_no_soln3)
    trace_count = 20
    duration = 100
    #traffic_file = "test_data/traffic_data/l5_system"
    #traffic_file_no_soln =  "test_data/traffic_data/l5_system_no_soln"
    #traffic_file_no_soln2 =  "test_data/traffic_data/l5_system_no_soln2"
    traffic_file_no_soln3 =  "test_data/traffic_data/l5_system_no_soln3"

    generator.generate_traffic_traces(folder_name=folder_name, file_name="test", trace_count=trace_count,
                                      viol_formula=viol_formula_prefix, traffic_file=traffic_file_no_soln3,
                                      duration=duration, pc=pc)


def cause_mining_traffic_data(pc, valuation_limit, folder_name, trace_count, signal_file_base, return_type,
                              operator_count_limit, withoutS=False, controllable_formulas = True):
    """
    Calls cause_mining_algorithm from cause_mining_algo package with traffic data.

    Returns: best formula in prefix form

    """
    print("---------------------------------------------------------------------------------------")
    print("                         cause_mining_traffic_data ")
    print("---------------------------------------------------------------------------------------")
    start_time = time.time()
    save = True
    metric_list = ['6', '1', '2', '3', '4', '5', '0']
    control_metrics = ['5', '6']
    set_valued_metrics = ['6', '5']
    parameter_domains = {'p0': range(10, 40, 5), 'p1': range(10, 40, 5), 'p2': range(10, 40, 5), 'p3': range(5, 20, 5),
                         'p4': range(5, 20, 5), 'p5': range(0, 2, 1), 'p6': range(0, 2, 1),  'pA': range(0, 6, 1),
                         'pP': range(0, 6, 1), 'pS': range(0, 6, 2), 'pT': [1, 2]}
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
                                                                controllable_formulas=controllable_formulas,
                                                                time_shift=1)  # type: FormulaValuation

    print('### --------end of cause mining for traffic data-------- ### ')
    print("Best Result in prefix form : " + best_result.formula +\
          "\nBest Result in infix form: " + STL.prefix_to_infix(best_result.formula) + \
          "\nWith the Valuation : " + str(best_result.valuation))
    end_time = time.time()
    print("")
    print("---------------------------------------------------------------------------------------")
    print("cause_mining_traffic_data ended in %s seconds" % str(end_time - start_time))
    print("---------------------------------------------------------------------------------------")
    print("folder name: " + folder_name)
    print("trace count: " + str(trace_count))
    print("processor count: " + str(pc))
    print("parameter domains: " + str(parameter_domains))
    print("return type: " + return_type.name)
    print("strictly increasing: " + str(strictly_increasing_oc))
    print("searched until operator count: " + str(operator_count_limit))

    return best_result.formula


def search_all_search_space_traffic_data(return_type, cause_limit, folder_name, trace_count, signal_file_base, pc,
                                         operator_count_limit=-1, upto=True, withoutS=False, controllable_formulas=True):
    """
    Calls search_all_search_space from  cause_mining_algo package with traffic data.
    cause_limit: max number of formula components in the end formula. That is, n if the end formula Phi is
    Phi:= phi_1 | phi_2 | ... | phi_n
    """

    print("---------------------------------------------------------------------------------------")
    print("                       search_all_search_space_traffic_data ")
    print("---------------------------------------------------------------------------------------")
    start_time = time.time()
    time_shift = 1
    metric_list = ['6', '1', '2', '3', '4', '5', '0']
    control_metrics = ['5', '6']
    set_valued_metrics = ['6', '5']
    parameter_domains = {'p0': range(10, 40, 10), 'p1': range(10, 40, 10), 'p2': range(10, 40, 10),
                         'p3': range(10, 20, 5), 'p4': range(10, 20, 5), 'p5': range(0, 2, 1), 'p6': range(0, 2, 1),
                         'pA': range(0, 6, 2), 'pP': range(0, 6, 2), 'pS': range(0, 6, 2), 'pT': [1, 2]}
    best_result = search_all_search_space.search_all_search_space(metric_list=metric_list,
                                                                  control_metrics=control_metrics,
                                                                  set_valued_metrics=set_valued_metrics,
                                                                  parameter_domains=parameter_domains,
                                                                  folder_name=folder_name, trace_count=trace_count,
                                                                  signal_file_base=signal_file_base,
                                                                  process_count=pc, return_type=return_type,
                                                                  oc_limit=operator_count_limit, cause_limit=cause_limit,
                                                                  upto=upto, withoutS=withoutS,
                                                                  controllable_formulas=controllable_formulas,
                                                                  time_shift=time_shift)  # type: FormulaValuation

    print('### --------end of search all search space for traffic data-------- ### ')
    print("Best Result is : " + best_result.formula + "\nWith the Valuation : " + str(best_result.valuation))

    print('### --------end of search all search space for traffic data-------- ### ')
    print("Best Result is : " + best_result.formula + "\nWith the Valuation : " + str(best_result.valuation))
    end_time = time.time()
    print("")
    print("---------------------------------------------------------------------------------------")
    print("search_all_search_space_traffic_data ended in %s seconds" % str(end_time - start_time))
    print("---------------------------------------------------------------------------------------")
    print("folder name: " + folder_name)
    print("trace count: " + str(trace_count))
    print("processor count: " + str(pc))
    print("parameter domains: " + str(parameter_domains))
    print("return type: " + return_type.name)
    print("cause_limit: " + str(cause_limit))
    print("searched until operator count: " + str(operator_count_limit))

    return best_result


def controller_traffic_data(viol_formula, folder_name, trace_count, duration, pc, cause_formula):
    """

    Args:
        cause_formula: formula got from cause_mining_traffic_data (in prefix form)

    Returns: nothing

    """
    #traffic_file = "test_data/traffic_data/l5_system"
    #traffic_file_no_soln = "test_data/traffic_data/l5_system_no_soln"
    #traffic_file_no_soln2 = "test_data/traffic_data/l5_system_no_soln2"
    traffic_file_no_soln3 = "test_data/traffic_data/l5_system_no_soln3"
    link_dict, intersection_dict = read_input.load_from_annotated_file(traffic_file_no_soln3)
    tn = network.Network(link_dict, intersection_dict, scale=5)

    uk_count = tn.get_intersection_count()
    xk_initialized = np.zeros(tn.get_link_count())
    tn.initialize_links(xk_initialized, 0.1)

    viol_formula_prefix = STL.infix_to_prefix(viol_formula)
    sg.controller(folder_name=folder_name, name='test', trace_count=trace_count,  duration=duration, viol_formula=viol_formula_prefix,
                  cause_formula=cause_formula, step_function=tn.step, xk_initialized=xk_initialized, uk_domain=[0, 1],
                  uk_count=uk_count, num_to_let=True)


def give_average_violation_cnt_reducement_ratio_fp_count_and_formula_length(sabit_folder, test_folder, viol_formula,
    return_type, operator_count_limit, pc, loop_count, signal_file_base, signal_file_rest, trace_count, duration,
    valuation_limit=0.1, heuristic=True, upto=True, cause_limit=1, withoutS=False):
    """

    Args:
        sabit_folder: if it is None, then we generate signals and find cause formulas all over again in every loop,
        if not, we find the cause formula once and generate controllers with it loop_count many times.
        test_folder:
        viol_formula:
        return_type:
        operator_count_limit:
        pc:
        loop_count:
        signal_file_base:
        signal_file_rest:
        trace_count:
        duration:
        valuation_limit:
        heuristic: (bool) if True, use cause mining heuristic algorithm, if False use search all search space.
        upto:
        cause_limit:
        withoutS:  (bool) if True, the formulas are generated without Since

    Returns: nothing

    """


    average_reducement_ratio = 0
    average_formula_fp_count = 0
    average_formula_length = 0
    average_violation_count = 0

    if sabit_folder == None:
        for i in range(loop_count):
            traffic_signal_generator(test_folder, pc)
            violation_count_1 = cma.controller_helper_funs.label_count(test_folder, 'test_', '_label', 20)
            print("violation count beginning: " + str(violation_count_1))
            if heuristic:
                cause_formula_prefix = cause_mining_traffic_data(pc=pc, valuation_limit=valuation_limit, folder_name=test_folder,trace_count=trace_count, signal_file_base=signal_file_base,
                                                                     return_type=return_type, operator_count_limit=operator_count_limit,
                                                                     withoutS=withoutS)  # best formula in prefix form
            else:
                best_result = search_all_search_space_traffic_data(pc=pc, return_type=return_type,
                                                                   folder_name=test_folder, trace_count=trace_count,
                                                                   signal_file_base=signal_file_base, cause_limit=cause_limit,
                                                                   operator_count_limit=operator_count_limit, upto=upto,
                                                                   withoutS=withoutS)
                cause_formula_prefix = STL.infix_to_prefix(best_result.formula)

            average_formula_length += helper_funs.count_formula_components(cause_formula_prefix)+1
            cmm.print_detailed_result(prefix=1, formula=cause_formula_prefix, folder_name=test_folder,
                                  signal_file_base=signal_file_base, signal_file_rest=signal_file_rest,
                                  trace_count=trace_count)

            fp_fn_tp_tn = evaluator.evaluate_signals(formula=cause_formula_prefix, folder_name=test_folder,
                                                     signal_file_base=signal_file_base, trace_count=trace_count,
                                                     signal_file_rest=signal_file_rest,
                                                     return_type=stl_constants.__DETAILED)
            formula_fp_count = fp_fn_tp_tn[0]
            average_formula_fp_count += formula_fp_count
            controller_traffic_data(folder_name=test_folder, viol_formula=viol_formula,trace_count=trace_count,
                                    duration=duration, pc=pc, cause_formula=cause_formula_prefix)
            violation_count_2 = cma.controller_helper_funs.label_count(test_folder, 'test_', '_label', 20)
            print("violation count end: " + str(violation_count_2))
            violation_red_ratio = 1 - (float(violation_count_2) / float(violation_count_1))
            average_violation_count += violation_count_2
            average_reducement_ratio += violation_red_ratio
            print("v_c_1: " + str(violation_count_1) + "   v_c_2: " + str(violation_count_2))

        average_formula_fp_count /= float(loop_count)
        average_formula_length /= float(loop_count)

    else:
        violation_count_beginning = cma.controller_helper_funs.label_count(sabit_folder, 'test_', '_label', 20)
        print("violation count of sabit folder is " + str(violation_count_beginning))
        if heuristic:
            cause_formula_prefix = cause_mining_traffic_data(pc=pc, valuation_limit=valuation_limit,
                                                             folder_name=sabit_folder,
                                                             trace_count=trace_count,
                                                             signal_file_base=signal_file_base,
                                                             return_type=return_type,
                                                             operator_count_limit=operator_count_limit,
                                                             withoutS=withoutS)  # best formula in prefix form
        else:
            best_result = search_all_search_space_traffic_data(pc=pc, return_type=return_type,
                                                               folder_name=sabit_folder, trace_count=trace_count,
                                                               signal_file_base=signal_file_base,
                                                               cause_limit=cause_limit,
                                                               operator_count_limit=operator_count_limit, upto=upto,
                                                               withoutS=withoutS)
            cause_formula_prefix = STL.infix_to_prefix(best_result.formula)

        average_formula_length = helper_funs.count_formula_components(cause_formula_prefix) + 1
        cmm.print_detailed_result(prefix=1, formula=cause_formula_prefix, folder_name=sabit_folder,
                                  ignal_file_base=signal_file_base, signal_file_rest=signal_file_rest,
                                  trace_count=trace_count)

        fp_fn_tp_tn = evaluator.evaluate_signals(formula=cause_formula_prefix, folder_name=sabit_folder,
                                                 signal_file_base=signal_file_base, trace_count=trace_count,
                                                 signal_file_rest=signal_file_rest,
                                                 return_type=stl_constants.__DETAILED)
        average_formula_fp_count = fp_fn_tp_tn[0]


        for i in range(loop_count):
            controller_traffic_data(folder_name=test_folder, viol_formula=viol_formula, trace_count=trace_count,
                                    duration=duration, pc=pc, cause_formula=cause_formula_prefix)
            violation_count = cma.controller_helper_funs.label_count(test_folder, 'test_', '_label', 20)
            print("violation count in loop: " + str(i) + " is " + str(violation_count))
            average_violation_count += violation_count
            violation_red_ratio = 1 - (float(violation_count) / float(violation_count_beginning))
            average_reducement_ratio += violation_red_ratio

    average_reducement_ratio /= float(loop_count)
    average_violation_count /= float(loop_count)

    return average_violation_count, average_reducement_ratio, average_formula_fp_count, average_formula_length


def controller_n_times(n, sabit_folder, test_folder, viol_formula, return_type, operator_count_limit, pc,
                       signal_file_base, signal_file_rest, trace_count, duration, valuation_limit=0.1, heuristic=True,
                       upto=True, cause_limit=1, withoutS=False):
    """

    Args:
        n: how many times will we iterate in controller refinement?
        sabit_folder:  if it is None, then we generate a random initial file and mine it to find the cause formula;
        if it is not None, we will mine sabit_folder to find the cause formula initially.
        test_folder: this is the folder in which we will create the traffic data generated by the controller and rewrite
        it in every loop
        viol_formula:
        return_type: fitness value
        operator_count_limit:
        pc:
        signal_file_base:
        signal_file_rest:
        trace_count:
        duration:
        valuation_limit: used iff heuristic==True. A formula stays as a component of the big formula iff the valuation
        it adds to the big formula is bigger than the valuation_limit.
        heuristic: (bool) if True, use cause mining heuristic algorithm, if False use search all search space.
        upto: used iff heuristic == False. If True, consider all formulas with operator counts upto the given
        operator_count limit, if False, consider only the formulas with operator_count = given operator_count_limit.
        cause_limit: used iff heuristic == False. In search_all_search_space, find cause_formulas with cause_limit
        many subformulas concatenated with |.
        withoutS: (bool) if True, the formulas are generated without Since.

    Returns:

    """

    print("--------------------entering controller_n_times-----------------------")

    violation_counts = []
    cause_formula_list = []

    if not sabit_folder:
        traffic_signal_generator(test_folder, pc)
        folder_name = test_folder
    else:
        folder_name = sabit_folder

    vc = cma.controller_helper_funs.label_count(folder_name, 'test_', '_label', 20)
    violation_counts.append(vc)
    print("initial violation count : " + str(vc))

    if heuristic: # heuristic cannot be used yet for oc_limit = [oc_limit_lhs, oc_limit_rhs] form
        cause_formula_prefix = cause_mining_traffic_data(pc=pc, valuation_limit=valuation_limit,
                                                         folder_name=folder_name,
                                                         trace_count=trace_count, signal_file_base=signal_file_base,
                                                         return_type=return_type,
                                                         operator_count_limit=operator_count_limit,
                                                         withoutS=withoutS)  # best formula in prefix form
    else:
        best_result = search_all_search_space_traffic_data(pc=pc, return_type=return_type,
                                                           folder_name=folder_name, trace_count=trace_count,
                                                           signal_file_base=signal_file_base,
                                                           cause_limit=cause_limit,
                                                           operator_count_limit=operator_count_limit, upto=upto,
                                                           withoutS=withoutS)
        cause_formula_prefix = STL.infix_to_prefix(best_result.formula)

    cause_formula_infix = STL.prefix_to_infix(cause_formula_prefix)
    cause_formula_list.append(cause_formula_infix)

    cmm.print_detailed_result(prefix=1, formula=cause_formula_prefix, folder_name=folder_name,
                              signal_file_base=signal_file_base, signal_file_rest=signal_file_rest,
                              trace_count=trace_count)

    folder_name = test_folder
    for i in range(1, n+1):
        print("-- -- -- In iteration number " + str(i) + " -- -- -- ")
        cause_formula = helper_funs.concat_with_or_infix(cause_formula_list)
        cause_formula = STL.infix_to_prefix(cause_formula)

        print("- - results of the whole cause formula - - ")
        cmm.print_detailed_result(prefix=1, formula=cause_formula, folder_name=folder_name,
                                  signal_file_base=signal_file_base, signal_file_rest=signal_file_rest,
                                  trace_count=trace_count)

        controller_traffic_data(folder_name=folder_name, viol_formula=viol_formula, trace_count=trace_count,
                                duration=duration, pc=pc, cause_formula=cause_formula)

        violation_counts.append(cma.controller_helper_funs.label_count(test_folder, 'test_', '_label', 20))
        print("violation count: " + str(violation_counts[i]))
        if violation_counts[i] == 0:
            break

        if not i == n:
            if heuristic:
                last_formula_prefix = cause_mining_traffic_data(pc=pc, valuation_limit=valuation_limit,
                                                                folder_name=folder_name, trace_count=trace_count,
                                                                signal_file_base=signal_file_base,
                                                                return_type=return_type,
                                                                operator_count_limit=operator_count_limit,
                                                                withoutS=withoutS)  # best formula in prefix form
            else:
                best_result = search_all_search_space_traffic_data(pc=pc, return_type=return_type,
                                                                   folder_name=folder_name, trace_count=trace_count,
                                                                   signal_file_base=signal_file_base,
                                                                   cause_limit=cause_limit,
                                                                   operator_count_limit=operator_count_limit,
                                                                   upto=upto, withoutS=withoutS)
                last_formula_prefix = STL.infix_to_prefix(best_result.formula)

            last_formula_infix = STL.prefix_to_infix(last_formula_prefix)
            cause_formula_list.append(last_formula_infix)
            print("- - results of the last formula - - ")
            cmm.print_detailed_result(prefix=1, formula=last_formula_prefix, folder_name=folder_name,
                                      signal_file_base=signal_file_base, signal_file_rest=signal_file_rest,
                                      trace_count=trace_count)

    print("--------------------exiting controller_n_times-----------------------")

def find_best_formula(folder_name, trace_count, heuristic, duration, signal_file_base, signal_file_rest, return_type,
                      operator_count_limit, pc, upto, cause_limit, withoutS, valuation_limit=None):
    """

    Returns: the best formula found with heuristic algorithm if heuristic == True, found with search_all_search_space if
    heuristic == False.

    """
    if not heuristic:
        best_result = search_all_search_space_traffic_data(pc=pc, return_type=return_type,
                                                           folder_name=folder_name, trace_count=trace_count,
                                                           signal_file_base=signal_file_base,
                                                           cause_limit=cause_limit,
                                                           operator_count_limit=operator_count_limit, upto=upto,
                                                           withoutS=withoutS)
        cause_formula_prefix = STL.infix_to_prefix(best_result.formula)

    else:
        cause_formula_prefix = cause_mining_traffic_data(pc=pc, valuation_limit=valuation_limit,
                                                        folder_name=folder_name, trace_count=trace_count,
                                                        signal_file_base=signal_file_base,
                                                        return_type=return_type,
                                                        operator_count_limit=operator_count_limit,
                                                        withoutS=withoutS)  # best formula in prefix form

    cmm.print_detailed_result(prefix=1, formula=cause_formula_prefix, folder_name=folder_name,
                              signal_file_base=signal_file_base, signal_file_rest=signal_file_rest,
                              trace_count=trace_count)
    return cause_formula_prefix

def look_for_any_formula(folder_name, trace_count, heuristic, duration, signal_file_base, signal_file_rest, return_type,
                      operator_count_limit, pc, upto, cause_limit, withoutS, valuation_limit=None):
    if not heuristic:
        best_result = search_all_search_space_traffic_data(pc=pc, return_type=return_type,
                                                           folder_name=folder_name, trace_count=trace_count,
                                                           signal_file_base=signal_file_base,
                                                           cause_limit=cause_limit,
                                                           operator_count_limit=operator_count_limit, upto=upto,
                                                           withoutS=withoutS, controllable_formulas=False)
        cause_formula_prefix = STL.infix_to_prefix(best_result.formula)

    else:
        cause_formula_prefix = cause_mining_traffic_data(pc=pc, valuation_limit=valuation_limit,
                                                        folder_name=folder_name, trace_count=trace_count,
                                                        signal_file_base=signal_file_base,
                                                        return_type=return_type,
                                                        operator_count_limit=operator_count_limit,
                                                        withoutS=withoutS, controllable_formulas=False)  # best formula in prefix form

    cmm.print_detailed_result(prefix=1, formula=cause_formula_prefix, folder_name=folder_name,
                              signal_file_base=signal_file_base, signal_file_rest=signal_file_rest,
                              trace_count=trace_count)
    return cause_formula_prefix

def traffic_example_main():

    #plot_folder = 'test_data/traffic_data/plot-folder/'
    #test_file_name = 'test_data/traffic_data/plot-folder/test_sabit_test_0'
    #label_file_name = test_file_name +'_label'
    #cause_formula_label_file_name = test_file_name + '_cause_formula_label'
    #cause_formula_infix = '( ( ( A 1 3 ( x5 = 0.0 ) ) | ( A 1 3 ( x6 = 0.0 ) ) ) | ( ( A 1 1 ( x5 = 0.0 ) ) & ( P 1 1 ( x3 > 10.0 ) ) ) ) | ( ( A 1 1 ( x6 = 0.0 ) ) & ( P 1 1 ( x4 > 10.0 ) ) ) '#'( ( A 0 2 ( x6 = 0.0 ) ) & ( P 1 1 ( x4 > 10.0 ) ) ) | ( ( A 0 2 ( x5 = 0.0 ) ) & ( P 1 1 ( x3 > 10.0 ) ) )'
    #cause_formula_prefix = STL.infix_to_prefix(cause_formula_infix)
    #sg.label_test_file(test_file_name=test_file_name, label_file_name=cause_formula_label_file_name, viol_formula=cause_formula_prefix, duration=100)

    #sabit_folder = 'test_data/traffic_data/sabit-folder/'
    #cmm.print_detailed_result(prefix=1, formula=cause_formula_prefix, folder_name=sabit_folder,
    #                          signal_file_base='test', signal_file_rest='',
    #                          trace_count=1)
    #
    #print "violation count sabit_folder: " + str(cma.controller_helper_funs.file_label_count(plot_folder+'test_sabit_test_0_label'))
    #print "violation count cause formula label: " + str(cma.controller_helper_funs.file_label_count(plot_folder+'test_sabit_test_0_cause_formula_label'))

    sabit_folder = 'test_data/traffic_data/sabit-folder/'
    #test_folder = 'test_data/traffic_data/test2/'
    #viol_formula = "x0 < 30 & x1 < 30 & x2 < 30 & x3 < 15 & x4 < 15"
    #viol_formula_no_soln = "x0 < 32 & x1 < 32 & x2 < 32 & x3 < 16 & x4 < 16"
    #viol_formula_no_soln2 = "x0 < 30 & x1 < 30 & x2 < 30 & x3 < 15 & x4 < 15"
    #viol_formula_no_soln3 = "x0 < 30 & x1 < 30 & x2 < 30 & x3 < 15 & x4 < 15"
    signal_file_base = 'test'
    signal_file_rest = ''
    trace_count = 20
    duration = 100
    controllable_formulas = False
    if controllable_formulas:
        oc_limit_lhs = 1
        oc_limit_rhs = 0
        oc_limit = [oc_limit_lhs, oc_limit_rhs]
    else:
        oc_limit = 1
    cause_limit = 1
    pc = 8

    return_type = stl_constants.__F_03_SCORE
    upto = False  # look for formulas with exactly cause_limit many components
    withoutS = True
    heuristic = False

    iteration_cnt = 100
    valuation_limit = 0.01

    #print("operator_count_limit = " + str(oc_limit))
   # print("pc = " + str(pc))
   # print("return type = " + str(return_type.category))
    #print("withoutS = " + str(withoutS))
   # print("heuristic = " + str(heuristic))
    #if heuristic:
     #   print("iteration_cnt = " + str(iteration_cnt))
     #   print("valuation_limit = " + str(valuation_limit))
        #     else:
        #     print("cause_limit = " + str(cause_limit))
        #        print("upto = " + str(upto))

    #look_for_any_formula(sabit_folder, trace_count, heuristic, duration, signal_file_base, signal_file_rest, return_type,
    #                      oc_limit, pc, upto, cause_limit, withoutS, valuation_limit)

    # ---------------------------------------------------------------------------------------------------------------

    #controller_n_times(n=iteration_cnt, test_folder=test_folder, sabit_folder=None, viol_formula=viol_formula_no_soln3,
    #                   trace_count=trace_count, duration=duration, signal_file_base=signal_file_base,
    #                   signal_file_rest=signal_file_rest, return_type=return_type, operator_count_limit=oc_limit, pc=pc,
    #                  valuation_limit=valuation_limit, heuristic=heuristic, upto=upto, cause_limit=cause_limit, withoutS=withoutS)


    p_formula = find_best_formula(folder_name=sabit_folder, trace_count=trace_count, duration=duration, heuristic=heuristic,
                                  signal_file_base=signal_file_base, signal_file_rest=signal_file_rest,
                                 return_type=return_type, operator_count_limit=oc_limit, pc=pc, upto=upto,
                                  cause_limit=cause_limit, withoutS=withoutS, valuation_limit=valuation_limit)
    #X_formula = scf.return_sc_form('A 1 1 ( x5 = 0.0 )  & ( A 1 2 ( P 1 1 ( ( x3 > 10.0 ) & ( x3 < 5 ) ) ) )', prefix=False)
   # p_formula =  'P 1 1 ( ( A 0 2 ( x1 = 1 ) ) | ( A 0 1 ( x2 = 2 ) ) )'
    xed_formula = '( !p3 & ( X ( ( !p1 & p2 ) | ( !p0 & p2 ) | ( !p1 & !p2 ) | ( !p0 & ! p2 ) ) ) )| ( !p2 & ( X ( ( !p1 & !p2 ) | ( !p0 & !p2 ) ) ) )'
    X_formula = scf.return_sc_form(p_formula, prefix=False)
    # print(X_formula)
    formula_with_atomic_props, dict = scf.turn_inequalities_to_atomic_propositions(X_formula)
    print(formula_with_atomic_props, dict)

    # ---------------------------------------------------------------------------------------------------------------

    #best_result = search_all_search_space_traffic_data(return_type=return_type, cause_limit=cause_limit, operator_count_limit=oc_limit, upto=upto, folder_name=sabit_folder, trace_count=trace_count, signal_file_base=signal_file_base, pc=pc, withoutS=withoutS)
    #cause_formula_prefix = STL.infix_to_prefix(best_result.formula)

    #avc, avrr, afpc, afl = give_average_violation_cnt_reducement_ratio_fp_count_and_formula_length(
    #    test_folder=test_folder, sabit_folder=sabit_folder, viol_formula=viol_formula, trace_count=trace_count, duration=duration,
    #    signal_file_base=signal_file_base, signal_file_rest=signal_file_rest, return_type=return_type,
    #    operator_count_limit=oc_limit, pc=pc, loop_count=30, valuation_limit=0.1, heuristic=False, upto=upto,
    #    cause_limit=cause_limit, withoutS=withoutS)

    #print "Average Violation Count: " + str(avc)
    #print "Average Violation Reducement Ratio : " + str(avrr)
    #print "Average False Positive Count : " + str(afpc)



    #cause_formula_infix = '( ( ( A 1 3 ( x5 = 0.0 ) ) | ( A 1 3 ( x6 = 0.0 ) ) ) | ( ( A 1 1 ( x5 = 0.0 ) ) & ( P 1 1 ( x3 > 10.0 ) ) ) ) | ( ( A 1 1 ( x6 = 0.0 ) ) & ( P 1 1 ( x4 > 10.0 ) ) ) '#'( ( A 0 2 ( x6 = 0.0 ) ) & ( P 1 1 ( x4 > 10.0 ) ) ) | ( ( A 0 2 ( x5 = 0.0 ) ) & ( P 1 1 ( x3 > 10.0 ) ) )'
    #cause_formula_prefix = STL.infix_to_prefix(cause_formula_infix)
    #viol_cnt = 0
    #fp_cnt = 0
    #tp_cnt = 0
    #for i in xrange(0,10):
    #    traffic_signal_generator(test_folder, pc)
    #    viol_cnt += cma.controller_helper_funs.label_count(folder_name=test_folder, label_file_base='test_', label_file_rest='_label', trace_count=20)
    #    fp_fn_tp_tn = cmm.print_detailed_result(prefix=1, formula=cause_formula_prefix, folder_name=test_folder,
    #                              signal_file_base=signal_file_base, signal_file_rest=signal_file_rest,
    #                              trace_count=trace_count)
    #    fp_cnt += fp_fn_tp_tn[0]
    #    tp_cnt += fp_fn_tp_tn[2]

    #print "violation count: " + str(viol_cnt)
    #print "fp count: " + str(fp_cnt)
    #print "tp count: " + str(tp_cnt)


    #avg_viol_cnt = 0
    #avg_fp_cnt = 0
    #formula_infix = '( ( A 0 2 ( x6 = 0.0 ) ) & ( P 1 1 ( x4 > 10.0 ) ) ) | ( ( A 0 2 ( x5 = 0.0 ) ) & ( P 1 1 ( x3 > 10.0 ) ) )'
    #formula_prefix = STL.infix_to_prefix(formula_infix)
    #for j in xrange(60):
    #traffic_signal_generator(test_folder, pc=0)
    #    fp_fn_tp_tn = evaluator.evaluate_signals(formula=formula_prefix, folder_name=test_folder,
    #                                             signal_file_base=signal_file_base, trace_count=trace_count,
    #                                             signal_file_rest=signal_file_rest,
    #                                             return_type=stl_constants.__DETAILED)
    #    avg_fp_cnt += fp_fn_tp_tn[0]
        #vc = cma.controller_helper_funs.label_count(test_folder, 'test_', '_label', 20)
        #avg_viol_cnt += vc
    #avg_fp_cnt /= 60
    #print "avg tp cnt : " + str(avg_fp_cnt)
    # 0.6, 717.7
