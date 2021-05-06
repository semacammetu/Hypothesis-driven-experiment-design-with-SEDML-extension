

import itertools
from . import evaluator

import trace_checker.STL as STL
import plot
from timeit import default_timer as timer
from multiprocessing import Pool
from functools import partial
from constants import stl_constants

def evaluate_signals_from_param(params, parameter_list, formula, folder_name, signal_file_base, trace_count,
                                signal_file_rest, return_type, past_results=[]):

  tmp_formula = formula
  for p, v in zip(parameter_list, params):
    tmp_formula = tmp_formula.replace(p, str(v))

  return evaluator.evaluate_signals(formula=tmp_formula, folder_name=folder_name, signal_file_base=signal_file_base,
                                    trace_count=trace_count, signal_file_rest=signal_file_rest,
                                    return_type=return_type, past_results=past_results), params


def my_test(t, t2, t3):
  print('my test ' + str(t) + ' ' + str(t2) + ' ' + str(t3))
  return t*t


def multip():
  p = Pool(2)
  m = partial(my_test, t2=2, t3=12)
  t = [0, 1, 2, 3, 4, 5]
  r = p.map(m, t)
  print(r)


def grid_search(formula, parameter_list, parameter_domain, folder_name, signal_file_base, trace_count,
                signal_file_rest, process_count, return_type=stl_constants.__MISMATCH, save_result=False,
                past_results=[]):
  """

  Args:
    formula: Prefix Formula, e.g., A pA0 pA1 P pP0 pP1 x > 10
    parameter_list: A list of strings, [p1, p2]
    parameter_domain: A list of lists representing domains for each parameter, [[1,2], [1,2,3,4]]
    folder_name: A string, the files will be read from here.
    signal_file_base: A string,
    trace_count: A string, folder_name + signal_file_base + i + signal_file_rest, i< signal_file_count files will
      be loaded.
    signal_file_rest: A string
    process_count: An integer, process count.
    return_type: An stl_constants ReturnType instance.
    save_result: A boolean. If set, store the results to folder_name/formula_results
    past_results: List of Formula_Valuation's

  Returns:
    The optimal valuation, the optimal parameter set, all results (a list of parameter-valuation pairs),
    and the total computation time.
  """

  best_val = 0
  if return_type.category == stl_constants.CATEGORY_MINIMIZATION:
    best_val = stl_constants.MAX_EVAL
  best_params = None
  start = timer()
  results = []
  if process_count > 0:
    # Create a pool, and perform the evaluation in parallel.
    partial_evaluate_signals = partial(evaluate_signals_from_param, parameter_list=parameter_list, formula=formula,
                                       folder_name=folder_name, signal_file_base=signal_file_base,
                                       trace_count=trace_count, signal_file_rest=signal_file_rest,
                                       return_type=return_type, past_results=past_results)
    pool = Pool(processes=process_count)
    results = pool.map(partial_evaluate_signals, itertools.product(*parameter_domain))
    pool.close()
    pool.join()
    if return_type.category == stl_constants.CATEGORY_MINIMIZATION:
      r = min(results, key=lambda item: item[0])
    else:
      r = max(results, key=lambda item:item[0])

    best_val = r[0]
    best_params = r[1]
    # return r[0], r[1], tp

  else:
    # Sequential evaluation, preferred for debugging.
    for params in itertools.product(*parameter_domain):
      tmp_formula = formula
      for p, v in zip(parameter_list, params):
        tmp_formula = tmp_formula.replace(p, str(v))

      #print "formula: " + tmp_formula
      v = evaluator.evaluate_signals(formula=tmp_formula, folder_name=folder_name, signal_file_base=signal_file_base,
                                     trace_count=trace_count, signal_file_rest=signal_file_rest,
                                     return_type=return_type, stn=None, past_results=past_results)
      if save_result:  # store if it will be saved
        results[params] = v
      if return_type.category == stl_constants.CATEGORY_MINIMIZATION and v < best_val:
        best_params = params
        best_val = v
      if return_type.category == stl_constants.CATEGORY_MAXIMIZATION and v > best_val:
        best_params = params
        best_val = v

  end = timer()
  time_passed = end - start
  if save_result:
    result_file = folder_name + formula + "results"
    plot.convert_save_results(parameter_list, parameter_domain, results, result_file, formula, time_passed,
                              trace_count, process_count, best_val, best_params)

  return best_val, best_params, time_passed

