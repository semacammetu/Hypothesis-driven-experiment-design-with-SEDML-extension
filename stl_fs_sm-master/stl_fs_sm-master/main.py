import plot
from cause_mining_algo import cause_mining_heuristic
from cause_mining_algo import search_all_search_space
from constants import stl_constants
from optimization import evaluator
from optimization import formula_search
from optimization import genetic_algorithm
from optimization import grid_search
from random_walk import random_walk_tree
from signal_generation import generator
from trace_checker import STL
from trace_checker import formula_generator
from util import genetic_algorithm_util

"""
This file contains basic functions to call methods implemented for STL synthesis and evaluation.
"""


def evaluate_signals(formula, folder_name, sf_base, sfc):
    """
    This function evaluates the signal in folder_name/sf_base_(%d sfc) against STL formula.
    It also plots and saves the results.

    Args:
      formula: A string representing an STL formula in prefix from.
      folder_name: A string.
      sf_base: A string
      sfc: An integer

    """
    stn = STL.SyntaxTreeNode()
    stn.initialize_node(formula.split(), 0)

    avg = 0
    i = sfc
    s_file_name = (sf_base + "_%d") % i
    t, signal = plot.read_into_arrays(folder_name + s_file_name)
    t, label = plot.read_into_arrays(folder_name + s_file_name + "_label")

    result = stn.compute_along_signal(signal, t)
    binary_result = [x > 0 for x in result]
    plot.plot_with_evaluation(signal, label, t, i, result, binary_result)
    t = 0
    file_name = folder_name + s_file_name + formula + ".png"
    file_name = file_name.replace(" ", "")
    plot.save(file_name)
    print("The figure is saved as " + file_name)

    # Ignore first 10:
    label[0:10] = []
    result[0:10] = []
    for l, r in zip(label, result):
        if (r >= 0 and l > 0) or (r < 0 and l == 0):
            t += 1
    avg += (float(t)) / len(label)
    print("Average fit" + str(avg))
    plot.show()


def plot_for_paper():
    """

    This function is simply to generate plots used in the papers, the numbers given below are obtained from
    optimization results and plots are generated accordingly. Change when needed.

    """
    folder_name = 'test_data/gauss_test_all_formulas/'
    folder_name = 'test_data/test_data_gauss_codit_from_holy/'
    folder_name = 'test_data/test_data_push_codit/'
    # folder_name = 'test_data/push_test/'
    signal_file_base = 'sgt'
    trace_count = 4

    # Ressults for Codit 2018 paper.
    # formula = "x0 > 38" # mismatch 5787
    # evaluate_signals(formula, folder_name, signal_file_base, trace_count, [38])
    # plot.show()
    #
    # formula = "A 0 52 ( x0 > 18 )" # 766
    # prefix_formula = STL.infix_to_prefix(formula)
    # evaluate_signals(prefix_formula, folder_name, signal_file_base, trace_count, [18])
    # plot.show()

    # formula = "( x0 > 22 ) & ( A 0 52 ( x0 > 18 ) )" # 697
    # prefix_formula = STL.infix_to_prefix(formula)
    # evaluate_signals(prefix_formula, folder_name, signal_file_base, trace_count, [18])
    # plot.show()

    formula = "( x1 > 10 ) & ( x0 < 1 )"
    prefix_formula = STL.infix_to_prefix(formula)
    evaluate_signals(prefix_formula, folder_name, signal_file_base, trace_count, [10])
    plot.show()


def search_parameters_push_restart():
    """
    Prepares parameters, calls grid search for push restart data.
    """

    folder_name = 'test_data/push_restart/'
    signal_file_base = 'sgt'
    trace_count = 5
    pc = 4

    # to generate
    # generator.generate_signals_push(folder_name, signal_file_base, trace_count, pc)

    formula = '( x1 > px1 ) & ( x0 = px0 )'
    formula = STL.infix_to_prefix(formula)

    parameter_list = ['px0', 'px1']
    parameter_domain = [list(range(0, 2, 1)), list(range(10, 11, 10))]
    result_file = folder_name + 'test_result.mat'
    best_v, params, time_passed = grid_search.grid_search(
        formula, parameter_list, parameter_domain, folder_name, signal_file_base, trace_count, '', pc)
    # all_results_converted = plot.convert_save_results(parameter_list, parameter_domain, all_results, result_file, formula,
    #                                                   time_passed, trace_count, pc, best_v, params)
    print(best_v)
    print(params)

    optimized_formula = formula
    optimized_formula = optimized_formula.replace('px0', str(params[0]))
    optimized_formula = optimized_formula.replace('px1', str(params[1]))
    evaluate_signals(optimized_formula, folder_name, signal_file_base, 2)
    plot.show()


def search_all_formulas_push_restart():
    """ Prepares parameters, calls formula search method for push restart data."""

    folder_name = 'test_data/push_restart/'

    signal_file_base = 'sgt'
    trace_count = 5
    pc = 0  # not parallel
    operator_counts = [0, 1, 2]

    parameter_domains = {'p0': range(0, 2, 1), 'p1': range(10, 40, 20), 'pA': range(20, 80, 20),
                         'pP': range(20, 80, 20), 'pS': range(20, 80, 20)}
    # parameter_domains = {'px': xrange(10,50,4), 'pA': xrange(20, 80, 4), 'pP': xrange(20, 100, 4), 'pS': xrange(20, 80, 4)}
    # parameter_domains = {'p0': xrange(10,40,20), 'pA': xrange(20, 80, 10), 'pP': xrange(20, 80, 10), 'pS': xrange(20, 80, 10)}

    result_file = 'min_max'
    metric_list = ['0', '1']
    set_valued_metrics = ['0']

    return_type = stl_constants.__MISMATCH

    best_formulas, formula = formula_search.formula_search(metric_list=metric_list,
                                                           set_valued_metrics=set_valued_metrics,
                                                           operator_counts=operator_counts,
                                                           parameter_domains=parameter_domains, folder_name=folder_name,
                                                           trace_count=trace_count, generate_signals=False,
                                                           signal_file_base=signal_file_base, process_count=pc,
                                                           save=True,
                                                           return_type=return_type, result_file=result_file)

    formula_prefix = STL.infix_to_prefix(formula.formula)
    print(formula)
    # return best_formulas
    evaluate_signals(formula_prefix, folder_name, signal_file_base, 4)
    plot.show()


def search_all_formulas_cpu():
    """ Prepares parameters, calls formula search method for cpu data."""

    folder_name = 'test_data/cpu/'

    signal_file_base = 'sgt'
    trace_count = 5
    pc = 4  # not parallel
    operator_counts = [0, 1, 2]

    parameter_domains = {'p0': range(0, 2, 1), 'pA': range(20, 80, 20), 'pP': range(20, 80, 20),
                         'pS': range(20, 80, 20)}

    result_file = 'min_max'
    metric_list = ['0']
    set_valued_metrics = []

    return_type = stl_constants.__MISMATCH

    best_formulas, formula = formula_search.formula_search(metric_list=metric_list,
                                                           set_valued_metrics=set_valued_metrics,
                                                           operator_counts=operator_counts,
                                                           parameter_domains=parameter_domains, folder_name=folder_name,
                                                           trace_count=trace_count, generate_signals=False,
                                                           signal_file_base=signal_file_base, process_count=pc,
                                                           save=True,
                                                           return_type=return_type, result_file=result_file)

    # formula = best_formulas[len(best_formulas)-1].formula
    formula_prefix = STL.infix_to_prefix(formula.formula)
    print(formula)
    # return best_formulas
    evaluate_signals(formula_prefix, folder_name, signal_file_base, 4)
    plot.show()


def show_results(formulas, folder_name, signal_file_base):
    """Plot results for the given set of formulas"""
    for _, formula in formulas.items():
        formula_prefix = STL.infix_to_prefix(formula.formula)
        print(formula)
        print(formula_prefix)
        evaluate_signals(formula_prefix, folder_name, signal_file_base, 3)
    plot.show()


def search_by_genetic_algorithm():

    # folder_name = 'test_data/gauss_test_all_formulas/'
    #folder_name = 'test_data/gaus_test_formula_search_codit/'
    folder_name = 'test_data/push_restart/'

    signal_file_base = 'sgt'

    trace_count = 500
    pc = 4
    operator_counts = [1, 2, 3]
    #return_type = stl_constants.__MISMATCH
    return_type = stl_constants.__MISMATCH
    maximum_operator_count = 4
    parameter_domains = {'p0': (10, 40), 'p1': (10, 40), 'pA': (20, 80), 'pP': (20, 80), 'pS': (20, 80)}

    #metric_list = ['0']
    metric_list = ['0', '1']
    set_valued_metrics = ['0']
    result, best_formula = genetic_algorithm.formula_search(metric_list=metric_list, set_valued_metrics=set_valued_metrics,
                                                            operator_counts=operator_counts,
                                                            folder_name=folder_name,
                                                            trace_count=trace_count, generate_signals='',
                                                            signal_file_base=signal_file_base, process_count=pc,
                                                            save=True,
                                                            return_type=return_type,
                                                            maximum_operator_count=maximum_operator_count,
                                                            parameter_domains=parameter_domains)

    print(best_formula)
    print(result)
    # return best_formulas
    # evaluate_signals(formula_prefix, folder_name, signal_file_base, 4)
    # plot.show()


def test_detailed_output():
    total = [0, 0, 0, 0]
    count = 0
    formula = " A 0 40 x0 > 10 "
    for i in range(5):
        s_file_name = ('sgt' + "_%d") % i
        s_file = 'test_data/gauss_test_all_formulas/' + s_file_name
        label_file = s_file + "_label"

        return_type = stl_constants.__DETAILED

        r = evaluator.evaluate(formula, s_file, label_file, None, return_type=return_type)
        count += 1
        total = [total[0] + r[0], total[1] + r[1], total[2] + r[2], total[3] + r[3]]
        print(str(r))
    print(str(total))


def traffic_signal_generator():
    # This function uses the package "signal_generation". This is for "cause mining."
    # generates new traffic_signal data with given violation_formula, trace_count and duration.
    folder_name = "test_data/traffic_data/test2/"
    viol_formula_yes_soln = "x0 < 30 & x1 < 30 & x2 < 30 & x3 < 15 & x4 < 15"  # viol formula for l5_system
    viol_formula_no_soln = "x0 < 32 & x1 < 32 & x2 < 32 & x3 < 16 & x4 < 16"  # viol formula for l5_system_no_soln
    viol_formula_prefix = STL.infix_to_prefix(viol_formula_yes_soln)
    trace_count = 20
    duration = 100
    generator.generate_traffic_traces(folder_name=folder_name, file_name="test", trace_count=trace_count,
                                      viol_formula=viol_formula_prefix, traffic_file="test_data/traffic_data/l5_system",
                                      duration=duration, pc=4)


def cause_mining_for_traffic_data():
    """
    Calls cause_mining_algorithm from cause_mining_algo package with traffic data.

    Returns the best formula (string) in prefix form

    """
    save = True
    folder_name = 'test_data/traffic_data/test2/'
    trace_count = 20
    pc = 8
    signal_file_base = 'test'
    metric_list = ['6', '1', '2', '3', '4', '5', '0']
    control_metrics = ['5', '6']
    set_valued_metrics = ['6', '5']
    parameter_domains = {'p1': range(0, 20, 5), 'p2': range(0, 20, 5), 'p3': range(0, 20, 5), 'p0': range(0, 20, 5),
                         'p6': range(0, 2, 1), 'p4': range(0, 20, 5), 'p5': range(0, 2, 1), 'pA': range(1, 10, 2),
                         'pP': range(1, 15, 3), 'pS': range(20, 80, 10)}
    result_file = 'min_max'
    return_type = stl_constants.__F_015_SCORE
    strictly_increasing_oc = False
    valuation_limit = 0.01
    operator_count = 1  # search until oc == 1
    best_result = cause_mining_heuristic.cause_mining_algorithm(metric_list=metric_list, control_metrics=control_metrics,
                                                                set_valued_metrics=set_valued_metrics,
                                                                parameter_domains=parameter_domains,
                                                                folder_name=folder_name, trace_count=trace_count,
                                                                signal_file_base=signal_file_base, process_count=pc,
                                                                save=save, result_file=result_file,
                                                                return_type=return_type,
                                                                strictly_increasing_oc=strictly_increasing_oc,
                                                                valuation_limit=valuation_limit,
                                                                operator_count_limit=operator_count)  # type: FormulaValuation
                                                                                                      # formula is in prefix form

    print('### --------end of cause mining for traffic data-------- ### ')
    print("Best Result is : " + best_result.formula + "\nWith the Valuation : " + str(best_result.valuation))


def search_all_search_space_for_traffic_data():
    """
    Calls search_all_search_space from  cause_mining_algo package with traffic data.
    """

    folder_name = 'test_data/traffic_data/test2/'
    trace_count = 20
    pc = 8
    signal_file_base = 'test'
    metric_list = ['6', '1', '2', '3', '4', '5', '0']
    control_metrics = ['5', '6']
    set_valued_metrics = ['6', '5']
    parameter_domains = {'p1': range(0, 20, 5), 'p2': range(0, 20, 5), 'p3': range(0, 20, 5), 'p0': range(0, 20, 5),
                         'p6': range(0, 2, 1), 'p4': range(0, 20, 5), 'p5': range(0, 2, 1), 'pA': range(1, 10, 2),
                         'pP': range(1, 15, 3), 'pS': range(20, 80, 10)}
    return_type = stl_constants.__F_015_SCORE
    operator_count = 1  # search until oc == 1
    best_result = search_all_search_space.search_all_search_space(metric_list=metric_list,
                                                                  control_metrics=control_metrics,
                                                                  set_valued_metrics=set_valued_metrics,
                                                                  parameter_domains=parameter_domains,
                                                                  folder_name=folder_name, trace_count=trace_count,
                                                                  signal_file_base=signal_file_base,
                                                                  process_count=pc, return_type=return_type,
                                                                  n=operator_count)  # type: FormulaValuation

    print('### --------end of search all search space for traffic data-------- ### ')
    print("Best Result is : " + best_result.formula + "\nWith the Valuation : " + str(best_result.valuation))


def test_crossover_with_new_random_node():

   formula1 = '| P 0 1 x0 = 21 x1 = 10'
   formula = '& x5 = 0 A 0 1 x3 > 15'
   stn = STL.SyntaxTreeNode()
   stn.initialize_node(formula.split(), 0)
   stn1 = STL.SyntaxTreeNode()
   stn1.initialize_node(formula1.split(), 0)
   parameter_domains = {'p3': (0, 40), 'p5': (0, 40), 'pA': (0, 80), 'pP': (20, 80), 'pS': (20, 80)}
   #print(stn.to_formula())
   #stn.mutate(parameter_domains)
   print(stn.to_formula())
   new_gen1, new_gen2 = genetic_algorithm_util.crossover(stn, stn1, 4)
   print(stn.to_formula())
   print(new_gen1.to_formula())

   print("-------------------------------")

   print(stn1.to_formula())
   print(new_gen2.to_formula())


def formula_generator_simplification():

  print("Generate parametric formulas with and without simplification, compare results.")
  metric_list = ['0', '1']
  set_valued_metrics = []
  operator_counts = [0, 1, 2]
  print_details = False
  for operator_count in operator_counts:
    formula_list = formula_generator.generate_formula_tree_iterative(metric_list, operator_count,
                                                                     return_formula_string=True,
                                                                     set_valued_metrics=set_valued_metrics,
                                                                     simplify=False);
    formula_list_simplified = formula_generator.generate_formula_tree_iterative(metric_list, operator_count,
                                                                     return_formula_string=True,
                                                                     set_valued_metrics=set_valued_metrics,
                                                                     simplify=True);
    print("\t\t\tRESULTS FOR OPERATOR COUNT %d" % operator_count)
    print("\t\t Formula count %d" % len(formula_list))
    print("\t\t Formula count - simplified %d" % len(formula_list_simplified))
    print("\t\t Difference %d" % (len(formula_list) - len(formula_list_simplified)))
    if print_details:
      removed_formula = set(formula_list)
      removed_formula.difference_update(set(formula_list_simplified))
      i=1
      for f in removed_formula:
        print("\t\t\t\t %i   ----   %s" % (i, f))
        i += 1

      print(" All formulas in the original list:")
      i=1
      for f in formula_list:
        print("\t\t\t\t %i   ----   %s" % (i, f))
        i += 1

      print(" All formulas in the simplified list:")
      i = 1
      for f in formula_list_simplified:
        print("\t\t\t\t %i   ----   %s" % (i, f))
        i += 1

  def random_walk():
    formula = "A 0 40 A 0 20 x0 > 1"
    folder_name = 'test_data/test_data_gauss_codit_from_holy/'
    trace_count = 4
    signal_file_base = 'sgt'
    rwt = random_walk_tree.RandomWalkTree()
    return_type = stl_constants.__F1_SCORE

    rwt.init_random_walk_tree(formula=formula)
    step_sizes = {'x0': (1, (0, 80)), 'A': (3, (0, 60))}
    iteration_limit = 3
    # walker.walk(rwt,step_sizes)
    tuple = rwt.generate_best_formula(step_sizes, iteration_limit=iteration_limit, folder_name=folder_name,
                                      sf_base=signal_file_base, trace_count=trace_count,
                                      return_type=return_type, include_lower_bounds=True)
    # rwt.walk(step_sizes, iteration_limit=iteration_limit, folder_name=folder_name, sf_base=signal_file_base, trace_count = trace_count,
    #                          return_type=return_type)


    print(rwt)
    print(tuple)




def test_data():
    folder_name = 'D:/CASE STUDY/ptSTL/stl_fs_sm-master/stl_fs_sm-master/test_data/hospital_bed_data/'
    signal_file_base = 'test'
    trace_count = 20
    phi_1 = ' ( P 1 1 ( ( v1 > 1500 ) & ( v6 > 3000 ) & ( v7 > 50 ) ) ) '
    phi_2 = ' ( P 1 1 ( ( v1 > 2500 ) & ( v6 > 3000 ) ) ) '
    phi_3 = ' ( P 1 1 ( ( v4 > 900 ) & ( v6 > 3000 ) & ( v7 > 50 ) ) )'
    optimized_formula = phi_1 + ' | ' + phi_2 + ' | ' + phi_3
    result = evaluator.evaluate_signals(STL.infix_to_prefix(optimized_formula), folder_name, signal_file_base, 1,
                                        '',
                                        stl_constants.__DETAILED, stn=None,
                                        past_results=[])
   # print('for formula = ' + optimized_formula + ' result is: ' + str(result))
    print('Optimized Formula: ' + optimized_formula)
    print('Result: ' + str(result))

def test_data_2():
    folder_name = 'D:/CASE STUDY/ptSTL/stl_fs_sm-master/stl_fs_sm-master/test_data/traffic_data/traffic_data_l6/'
    signal_file_base = 'test'
    trace_count = 20
    phi_1 = ' ( P 1 1 ( ( v1 > 15 ) & ( v7 = 1 ) & ( v6 = 0 ) ) ) '
    phi_2 = ' ( P 1 1 ( ( v1 > 25 ) & ( v7 = 1 ) ) ) '
    phi_3 = ' ( P 1 1 ( ( v4 < 10 ) & ( v7 = 1 ) & ( v6 = 0 ) ) )'
    optimized_formula = phi_1 + ' | ' + phi_2 + ' | ' + phi_3
    result = evaluator.evaluate_signals(STL.infix_to_prefix(optimized_formula), folder_name, signal_file_base, 20,
                                        '',
                                        stl_constants.__DETAILED, stn=None,
                                        past_results=[])
   # print('for formula = ' + optimized_formula + ' result is: ' + str(result))
    print('Optimized Formula: ' + optimized_formula)
    print('Result: ' + str(result))

if __name__ == '__main__':
    # Comment out a function to run the corresponding optimization, or to show the results.
    # Fix the paths within the function


    # cmm.cause_mining_main()
    test_data()


    # Sample usages:
    # Evaluate a signal, plot and save the figure.
    # evaluate_signals("A 0 40 x0 > 10", "test_data/cpu/", "sgt", 1)

    # search_parameters_push_restart()
    # search_all_formulas_push_restart()
    # search_all_formulas_cpu()
    # search_parameters_push_restart()
    # plot_for_paper()
    # traffic_signal_generator()
    # test_detailed_output()
    #start_time = time.time()
    # search_by_genetic_algorithm()
    # test_crossover_with_new_random_node()
    #cma.cause_mining_main()

    # formula_generator_simplification()

    #print("--- %s seconds of execution time---" % (time.time() - start_time))


