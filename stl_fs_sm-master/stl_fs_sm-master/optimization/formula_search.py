

from signal_generation import generator
from trace_checker import formula_generator
from trace_checker import STL
from optimization import grid_search
import plot
import scipy.io
from constants import stl_constants




def save_formula_search_results(folder_name, results, best_formulas, result_file):
  """

  Args:
    folder_name:
  """
  file_name = folder_name + 'formula_search_results' + result_file
  r = dict()
  r['results'] = results
  r['best_formulas'] = best_formulas
  scipy.io.savemat(file_name, r)



def formula_search(metric_list, set_valued_metrics, operator_counts, parameter_domains, folder_name, trace_count,
                   generate_signals, signal_file_base, process_count, save, return_type, result_file,
                   cause_mining=False, control_metrics=[], past_results=[], withoutS=False, time_shift = 0):
  """
  calls formula_search_operator_count to find a best formula for all given oc's in operator_counts list, returns all of
  the best formulas and the best of them

  Args:
    metric_list: all metrics that will be used in generated formulas
    set_valued_metrics: metrics that take discrete values within a given set
    operator_counts: (list of integers with ascending order !!) how many operators will be within metrics in the
    generated formulas. formula_search will find a best_formula (based on the given valuation method) f
    or all operator_counts given in this list
    parameter_domains:
    folder_name:
    trace_count:
    generate_signals:
    signal_file_base:
    process_count: for parallel processing
    save:
    return_type: determines the valuation that will be used to choose the best formulas. One of the types
    from stl_constants.
    result_file:
    cause_mining: (bool) formulas will be generated with generate_formula_tree_A_added if cause_mining==True, otherwise,
    they will be generated with generate_formula_tree
    control_metrics: the metrics that we have the control of, i.e. can change in the controller (for traffic system case
    control metrics are traffic lights whereas other metrics are road business rates)
    past_results: past best formulas. New formulas will be chosen according to their valuation "together with" the past
    best formulas.
    withoutS: (bool) if True, the formulas are generated without Since
  Returns: best_formulas (best formulas of all operator counts in operator_counts list), formula (the formula with
  the biggest oc i.e. necessarily the formula with the best valuation)
"""

  # If needed, generate signals.
  if generate_signals == "GAUS":
    generator.generate_signals(folder_name, signal_file_base, trace_count, process_count)
  elif generate_signals == "PUSH":
    generator.generate_signals_push(folder_name, signal_file_base, trace_count, process_count)

  # Perform the search for all given formula counts.

  results = {oc: [] for oc in operator_counts}
  best_formulas = {oc: [] for oc in operator_counts}
  for oc in operator_counts:
    results[oc], best_formulas[oc] = formula_search_operator_count(metric_list=metric_list,
                                                                   control_metrics=control_metrics,
                                                                   set_valued_metrics=set_valued_metrics, oc=oc,
                                                                   parameter_domains=parameter_domains,
                                                                   folder_name=folder_name,
                                                                   trace_count=trace_count,
                                                                   signal_file_base=signal_file_base,
                                                                   cause_mining=cause_mining,
                                                                   process_count=process_count,
                                                                   return_type=return_type,
                                                                   past_results=past_results, withoutS=withoutS,
                                                                   time_shift=time_shift)


    #print "Results for oc %d " % oc
    #if cause_mining:
    #  print best_formulas[oc]
    if best_formulas[oc].valuation == stl_constants.MIN_EVAL and return_type.category == stl_constants.CATEGORY_MINIMIZATION:
      break

  print("----------- END OF FORMULA SEARCH, PRINT RESULTS FOR EACH OPERATOR COUNT ------------- ")
  print(best_formulas)
  #if save:
    #save_formula_search_results(folder_name, results, best_formulas, result_file)

  formula = best_formulas[oc]
  if return_type.category == stl_constants.CATEGORY_MINIMIZATION:
    for oc in operator_counts:
      if best_formulas[oc] and formula.valuation > best_formulas[oc].valuation:
        formula = best_formulas[oc]
  elif return_type.category == stl_constants.CATEGORY_MAXIMIZATION:
    for oc in operator_counts:
      if best_formulas[oc] and formula.valuation < best_formulas[oc].valuation:
        formula = best_formulas[oc]

  return best_formulas, formula

def formula_search_operator_count( metric_list, set_valued_metrics, oc, parameter_domains, folder_name, trace_count,
                                  signal_file_base, process_count, return_type, cause_mining=False, control_metrics=[],
                                   past_results=[], withoutS=False, time_shift=0):
  """
   For the given operator count, compute the number of template formulas and
      run grid search for each template formula.

   Args:
      metric_list: list of metrics that will appear in formulas
      set_valued_metrics: metrics that take discrete values from a predefined set
      oc: (integer) how many operators will be in the resulting formula between metrics
      parameter_domains:
      folder_name:
      trace_count:
      signal_file_base:
      return_type: determines the valuation that will be used to choose the best formulas. One of the types
      from stl_constants
      cause_mining: (boolean) if we are using this function for cause mining, the generated formulas will be A added
      process_count: for parallel processing
      control_metrics: the metrics that we can control/change. These metrics' values will be changed and the systems
      will be resimulated to reduce the number of bad labeled data points in the future. In the traffic system case,
      control metrics are traffic lights and the other metrics are road business rates.
      past_results: past best formulas. New formulas will be chosen according to their valuation "together with" the
      past best formulas.
      withoutS: (bool) if True, the formulas are generated without Since

  Returns: results (all formulas generated with given oc and their valuations), best formula (and its valuation)
  """
  if cause_mining:
    template_formula_list = formula_generator.generate_formula_tree_for_cause_mining(metric_list=metric_list,
                                                                                     control_metrics=control_metrics,
                                                                                     operator_count=oc,
                                                                                     set_valued_metrics=set_valued_metrics,
                                                                                     withoutS=withoutS)

  else:
    template_formula_list = formula_generator.generate_formula_tree_iterative(metric_list, oc, return_formula_string=True,
                                                                    set_valued_metrics=set_valued_metrics, withoutS=withoutS)
    if time_shift > 0:
        time_shift_str = str(time_shift) + " " + str(time_shift)
        template_formula_list = ['P ' + time_shift_str + " ( " + f + " )" for f in template_formula_list]

  #print "----------- For operator count " + str(oc) + ", " + str(len(template_formula_list)) + " formulas will be tested."
  # Process and remove the formulas with double Since.
  #template_formula_list = [formula for formula in template_formula_list if formula.split().count('S') == 0]
  print("----------- For operator count " + str(oc) + ", " + str(len(template_formula_list)) + " formulas will be tested.")


  # For each template formula, run a grid search. Store the results, remember the best one.
  results = {f:{} for f in template_formula_list}
  best_formula = stl_constants.FormulaValuation(formula='False', valuation=stl_constants.MIN_EVAL)
  if return_type.category == stl_constants.CATEGORY_MINIMIZATION:
    best_formula = stl_constants.FormulaValuation(formula='False', valuation=stl_constants.MAX_EVAL)

  for template_formula in template_formula_list:
    formula, parameter_domains_for_formula = generate_formula_from_template(template_formula, parameter_domains)

    results[template_formula] = parameter_search_for_formula(formula=formula,
                                                             parameter_domains_for_formula=parameter_domains_for_formula,
                                                             folder_name=folder_name,
                                                             trace_count=trace_count,
                                                             signal_file_base=signal_file_base,
                                                             process_count=process_count, return_type=return_type,
                                                             past_results=past_results)

    if (return_type.category == stl_constants.CATEGORY_MAXIMIZATION and
            results[template_formula].valuation > best_formula.valuation) or (
        return_type.category == stl_constants.CATEGORY_MINIMIZATION and
            results[template_formula].valuation < best_formula.valuation):
      #  UPDATE BEST:
      best_formula = results[template_formula]
      print("(***   UPDATE BEST: " + best_formula.formula + " " + str(best_formula.valuation))
      if return_type.category == stl_constants.CATEGORY_MINIMIZATION and best_formula.valuation == stl_constants.MIN_EVAL:
        break # No need to check the rest
  return results, best_formula

def parameter_search_for_formula(formula, parameter_domains_for_formula, folder_name, trace_count, signal_file_base,
                                 process_count, return_type, past_results=[]):
  parameter_list = list(parameter_domains_for_formula.keys())
  parameter_domain = [parameter_domains_for_formula[pa] for pa in parameter_list]

  prefix_formula = STL.infix_to_prefix(formula)

  best_v, params, time_passed = grid_search.grid_search(formula=prefix_formula, parameter_list=parameter_list,
                                                        parameter_domain=parameter_domain, folder_name=folder_name,
                                                        signal_file_base=signal_file_base, trace_count=trace_count,
                                                        signal_file_rest='', process_count=process_count,
                                                        return_type=return_type, past_results=past_results)

  #result_file = folder_name + "".join(formula.split()) + ".mat"
  #_ = plot.convert_save_results(parameter_list, parameter_domain, all_results, result_file, formula,
  #                                                  time_passed, trace_count, process_count, best_v, params)

  formula_n = formula
  if params == None:
    print( "There are no best parameters for the formula: " + formula )
  else:
    for p, v in zip(parameter_list, params):
      formula_n = formula_n.replace(p, str(v))
    print("With valuation " + str(best_v) + " ,best parameters form " + formula_n + " ,with prefix form: " +
          STL.infix_to_prefix(formula_n) + " ,in time: " + str(time_passed))
  return stl_constants.FormulaValuation(formula=formula_n, valuation=best_v)


def generate_formula_from_template(template_formula, parameter_domains):

  # first process the formula:
  formula_tokens = template_formula.split()
  # tokens that start with p and has 2 characters:
  parameters = [p for p in formula_tokens if p[0] == 'p'] # and len(p) == 2] kismini sildim cunku hem p'yikontrol etmek yeterli, hem de parametre sayisi 9u gectiginde hata verecekti eski durumda
  parameters_set = list(set(parameters))  # make unique

  parameter_domains_in_formula = {}
  for p in parameters_set:
    last_index_found = 0
    for i in range(parameters.count(p)):
      p_new = p + str(i)
      for j in range(last_index_found, len(formula_tokens)):
        if formula_tokens[j] == p:
          last_index_found = j
          # If formula_tokens[j][1] is 'T', then it is P pT pT, we want both to take the same value, like P 1 1, P 2 2, ... so we want both to become pT0 pT0. Since there is only 2 pT's in each formula, we can initialize them by hand
          if formula_tokens[j][1] == 'T':
            formula_tokens[j] = 'pT0'
            parameter_domains_in_formula['pT0'] = parameter_domains[p]
            break
          formula_tokens[j] = p_new  # Burda find kullancaktim ama find da lineer zamanda is yapiyormus ve bulamayinca ValueError veriyor
          parameter_domains_in_formula[p_new] = parameter_domains[p]  # Bu da daha efektif yapilabilir.
          break
          # new_formula = new_formula.replace(p, p_new, 1)

  new_formula = " ".join(formula_tokens)
  print(new_formula)
  return new_formula, parameter_domains_in_formula



