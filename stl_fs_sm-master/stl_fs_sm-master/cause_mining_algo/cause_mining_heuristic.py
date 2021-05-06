

from optimization import evaluator
from optimization import formula_search
from trace_checker import STL
from constants import stl_constants
from util import metrics_util
from . import helper_funs

import matplotlib.pyplot as plt
import numpy as np


def cause_mining_algorithm(metric_list, control_metrics, set_valued_metrics, parameter_domains, folder_name,
                           trace_count, signal_file_base, process_count, save, result_file, return_type,
                           strictly_increasing_oc, valuation_limit, operator_count_limit, withoutS=False,
                           controllable_formulas=True, time_shift=0):
    """

    Args:
        metric_list:
        control_metrics:
        set_valued_metrics:
        parameter_domains:
        folder_name:
        trace_count:
        signal_file_base:
        process_count:
        save:
        result_file:
        return_type:
        strictly_increasing_oc: (bool) If False, the heuristic is applied while increasing operator count, if True,
        operator count increases by one in each loop.
        valuation_limit: the predefined limit which decides how much of a value addition is enough for a best formula of
        an operator count to enter the past_formula list.
        operator_count_limit: Last operator count. The best_formulas are searched for until operator count reaches this
        integer value.
        controllable_formulas: (bool) if True, cause_mining input is given to formula_search as True, and
                               generate_formula_tree_cause_mining is called inside formula_search_operator_count as a
                               consequence. That is, controllable formulas are synthesized.
                                    if False, cause_mining input is given to formula_search as False, and
                                    generate_formula_tree_iterative is called inside formula_search_operator_count as a
                                    consequence. That is, all kinds of formulas are generated.
                                By default, controllable_formulas = True, so only controllable formulas are generated.
    Returns: FormulaValuation(the resulting formula -small best formulas concatenated with ors- in prefix form, its valuation)

    """
    if type(operator_count_limit) is int:
        oc_rhs_limit = operator_count_limit
    else:
        _, oc_rhs_limit = operator_count_limit

    if controllable_formulas:  # we do this since if controllable_formulas == True, the code will enter generate_formula_tree_iterative and this function cannot process oc = -1
        current_oc = -1
    else:
        current_oc = 0
    past_results = []  # all formulas in past_results must be in prefix form

    if not strictly_increasing_oc:
        last_used_oc = current_oc
        while True:
            results, best_formula = formula_search.formula_search(metric_list=metric_list,
                                                                  set_valued_metrics=set_valued_metrics,
                                                                  operator_counts=[current_oc],
                                                                  parameter_domains=parameter_domains,
                                                                  folder_name=folder_name,
                                                                  trace_count=trace_count, generate_signals="",
                                                                  signal_file_base=signal_file_base,
                                                                  process_count=process_count,
                                                                  save=save, cause_mining=controllable_formulas,
                                                                  return_type=return_type,
                                                                  result_file=result_file,
                                                                  control_metrics=control_metrics,
                                                                  past_results=past_results, withoutS=withoutS,
                                                                  time_shift=time_shift)
            # turn the formula into prefix form, and then append it to past_results.
            best_formula_prefix = stl_constants.FormulaValuation(formula=STL.infix_to_prefix(best_formula.formula),
                                                                  valuation=best_formula.valuation)
            past_results.append(best_formula_prefix)
            if len(past_results) > 1 and (past_results[-1].valuation - past_results[-2].valuation) < valuation_limit:
                past_results.pop()
                if last_used_oc < current_oc:
                    print("break 1")
                    break
                current_oc += 1
                print("oc change to " + str(current_oc))

            elif len(past_results) > 1 and (past_results[-1].valuation - past_results[-2].valuation) > valuation_limit:
                last_used_oc = current_oc
                print("last used oc : " + str(last_used_oc))

            print("?????????????????? PAST RESULTS SO FAR ???????????????????????????")
            print(past_results)
            #helper_funs.print_past_formulas_prefix_infix_valuation(past_results=past_results, folder_name=folder_name,
            #                                                       signal_file_base=signal_file_base,
            #                                                       trace_count=trace_count,
            #                                                       signal_file_rest='', return_type=return_type)

            if current_oc == oc_rhs_limit+1:
                break

    else:  # i.e. if strictly_increasing_oc:

        while True:
            results, best_formula = formula_search.formula_search(metric_list=metric_list,
                                                                  set_valued_metrics=set_valued_metrics,
                                                                  operator_counts=[current_oc],
                                                                  parameter_domains=parameter_domains,
                                                                  folder_name=folder_name,
                                                                  trace_count=trace_count, generate_signals="",
                                                                  signal_file_base=signal_file_base,
                                                                  process_count=process_count,
                                                                  save=save, cause_mining=controllable_formulas,
                                                                  return_type=return_type,
                                                                  result_file=result_file,
                                                                  control_metrics=control_metrics,
                                                                  past_results=past_results,
                                                                  time_shift=time_shift)
            # turn the formula into prefix form, and the append it to past_results.
            best_formula_prefix = stl_constants.FormulaValuation(formula=STL.infix_to_prefix(best_formula.formula),
                                                                  valuation=best_formula.valuation)
            past_results.append(best_formula_prefix)

            if len(past_results) > 1 and (past_results[-1].valuation - past_results[-2].valuation) < valuation_limit:
                past_results.pop()
                print("break 2")
                break
            current_oc += 1
            if current_oc == operator_count_limit+1:
                break

            print("?????????????????? PAST RESULTS SO FAR ???????????????????????????")
            print(past_results)

    past_formulas = [fv.formula for fv in past_results]
    #for formula_valuation in past_results:
        #past_formulas.append(STL.prefix_to_infix(formula_valuation.formula))
    # now the list is consisted of infix formulas, it can go into concat_with_or
    result = stl_constants.FormulaValuation(formula=helper_funs.concat_with_or_prefix(past_formulas),
                                             valuation=past_results[-1].valuation)
    return result


def cause_mining_print_detailed_result(infix_formula, folder_name, signal_file_base, trace_count, signal_file_rest):
    """
        Written as a function to see how "good" a formula is, mainly to help us debug.
        This function prints the false positive, false negative, true positive, true negative, precision,
        recall and various f scores of the infix formula given as an input.
    """

    prefix_formula = STL.infix_to_prefix(infix_formula)
    fp_fn_tp_tn = evaluator.evaluate_signals(formula=prefix_formula, folder_name=folder_name,
                                             signal_file_base=signal_file_base, trace_count=trace_count,
                                             signal_file_rest=signal_file_rest, return_type=stl_constants.__DETAILED)

    print(infix_formula)
    fp = str(fp_fn_tp_tn[0])
    fn = str(fp_fn_tp_tn[1])
    tp = str(fp_fn_tp_tn[2])
    tn = str(fp_fn_tp_tn[3])
    precision = str(metrics_util.calculate_precision(fp_fn_tp_tn))
    recall = str(metrics_util.calculate_recall(fp_fn_tp_tn))
    f1 = str(metrics_util.calculate_f1_score(fp_fn_tp_tn))
    f05 = str(metrics_util.calculate_fhalf_score(fp_fn_tp_tn))
    f09 = str(metrics_util.calculate_f_Beta_score(fp_fn_tp_tn, 0.9))
    f01 = str(metrics_util.calculate_f_Beta_score(fp_fn_tp_tn, 0.1))
    f015 = str(metrics_util.calculate_f_Beta_score(fp_fn_tp_tn, 0.15))
    f02 = str(metrics_util.calculate_f_Beta_score(fp_fn_tp_tn, 0.2))
    f03 = str(metrics_util.calculate_f_Beta_score(fp_fn_tp_tn, 0.3))
    f04 = str(metrics_util.calculate_f_Beta_score(fp_fn_tp_tn, 0.4))

    print('fp: ' + fp + ' fn: ' + fn + ' tp: ' + tp + ' tn: ' + tn +
          ' precision: ' + precision + ' recall: ' + recall +
          ' \nf1 score: ' + f1 + ' f0.5 score: ' + f05 + ' f0.9 score: ' + f09 +
          ' \nf0.1 score: ' + f01 + ' f0.15 score: ' + f015 + ' f0.2 score: ' + f02 +
          ' f0.3 score: ' + f03 + ' \nf0.4 score: ' + f04)

    return fp_fn_tp_tn


def plot_change_wrt_parameter(formula, parameter_name, parameter_domain, folder_name, signal_file_base, trace_count):

    """
        Written as a function to see how "good" a formula is, mainly to help us debug.
        This function takes a formula with one parameter and parameter domain, replaces the parameter name
        with numbers in parameter domain and plots the change in the tp, tn, fp, tp+tn, precision, recall results
    """

    tp_plus_tn = []
    fp_plus_fn = []
    index_cnt = 0
    formulas = np.zeros((len(parameter_domain),
                         13))  # 13 corresponds to the 13 values evaluate_signals_deneme returs: fp,fn,tp,tn,precision,recall,f.5,f.4,f.3,f.2,f.15,f.1
    for i in parameter_domain:
        new_formula = formula.replace(parameter_name, str(i))
        print(new_formula)
        return_type = stl_constants.__DETAILED  # evaluate_signals returns fp,fn,tp,tn
        formulas[index_cnt, :4] = evaluator.evaluate_signals(formula=new_formula, folder_name=folder_name,
                                                             signal_file_base=signal_file_base, trace_count=trace_count,
                                                             signal_file_rest='', return_type=return_type)
        formulas[index_cnt, 5] = metrics_util.calculate_precision(formulas[index_cnt, :4])
        formulas[index_cnt, 6] = metrics_util.calculate_recall(formulas[index_cnt, :4])
        formulas[index_cnt, 7] = metrics_util.calculate_f_Beta_score(formulas[index_cnt, :4], 0.5)  # f0.5
        formulas[index_cnt, 8] = metrics_util.calculate_f_Beta_score(formulas[index_cnt, :4], 0.4)  # f0.4
        formulas[index_cnt, 9] = metrics_util.calculate_f_Beta_score(formulas[index_cnt, :4], 0.3)  # f0.3
        formulas[index_cnt, 10] = metrics_util.calculate_f_Beta_score(formulas[index_cnt, :4], 0.2)  # f0.2
        formulas[index_cnt, 11] = metrics_util.calculate_f_Beta_score(formulas[index_cnt, :4], 0.15)  # f0.15
        formulas[index_cnt, 12] = metrics_util.calculate_f_Beta_score(formulas[index_cnt, :4], 0.1)  # f0.1


        # the code piece between two identical prints only serves the need to see the values in the console, this part is useless for the plot
        #     print('\n#################### plot_change_wrt_parameter #####################')
        #     tp = int(formulas[index_cnt][0])
        #     tn = int(formulas[index_cnt][1])
        #     fp = int(formulas[index_cnt][2])
        #     fn = int(formulas[index_cnt][3])
        #     prec = int(formulas[index_cnt][4])
        #     recall = int(formulas[index_cnt][5])
        #     f1score = int(formulas[index_cnt][6])
        #     fhalfscore = int(formulas[index_cnt][7])
        #     print('tp: '+ str(tp) + ' tn: '+str(tn) + ' fp: '+ str(fp) + ' fn: ' + str(fn) + ' precision: '+ str(prec) + ' recall: ' + str(recall) + ' f1 score: ' + str(f1score) + ' f0.5 score: ' + str(fhalfscore))
        #     print('#################### plot_change_wrt_parameter #####################\n')

        tp_plus_tn.append(formulas[index_cnt][2] + formulas[index_cnt][3])
        fp_plus_fn.append(formulas[index_cnt][0] + formulas[index_cnt][1])
        index_cnt += 1

    t = [i for i in parameter_domain]
    # plot 1 : t vs. True Positive
    plt.subplot(8, 1, 1)
    plt.plot(t, formulas[:, 0], '-go')

    # above operations are done to write the formula in infix form
    stn = STL.SyntaxTreeNode()
    dummy_parameter = '999'  # this parameter is solely used to get our way around the stn.initialize_node function
    # by giving a dummy parameter in stead of parameter name to initialize the node properly. Then we replace this
    # dummy variable with parameter_name again to print the formula in infix form
    formula = formula.replace(parameter_name, dummy_parameter)
    stn.initialize_node(formula.split(), 0)

    plt.title('Formula = ' + stn.to_formula().replace(dummy_parameter, parameter_name))
    plt.ylabel('True Positive')

    # arranging plot 1 view
    [xmin, xmax, ymin, ymax] = plt.axis()
    y_axis_space = (ymax - ymin) / 5
    plt.axis([xmin, xmax, ymin - y_axis_space, ymax + y_axis_space])

    # arranging x axis labels
    ax = plt.gca()
    ax.set_xticks(t)
    ax.set_xticklabels(t)

    # plot 2 : t vs. False Positive
    plt.subplot(8, 1, 2)
    plt.plot(t, formulas[:, 0], '-co')
    plt.ylabel('False Positive')

    # arranging x axis labels
    ax = plt.gca()
    ax.set_xticks(t)
    ax.set_xticklabels(t)

    # plot 3 : t vs. F 0.5 Score
    plt.subplot(8, 1, 3)
    plt.plot(t, formulas[:, 7], '-ro', label="F 0.5")
    plt.ylabel('F 0.5')
    plt.legend()

    # arranging x axis labels
    ax = plt.gca()
    ax.set_xticks(t)
    ax.set_xticklabels(t)

    # plot 4 : t vs. F 0.4 Score
    plt.subplot(8, 1, 4)
    plt.plot(t, formulas[:, 8], '-ro', label="F 0.4")
    plt.ylabel('F 0.4')
    plt.legend()

    # arranging x axis labels
    ax = plt.gca()
    ax.set_xticks(t)
    ax.set_xticklabels(t)

    # plot 5 : t vs. F 0.3 Score
    plt.subplot(8, 1, 5)
    plt.plot(t, formulas[:, 9], '-ro', label="F 0.3")
    plt.ylabel('F 0.3')
    plt.legend()

    # arranging x axis labels
    ax = plt.gca()
    ax.set_xticks(t)
    ax.set_xticklabels(t)

    # plot 6 : t vs. F 0.2 Score
    plt.subplot(8, 1, 6)
    plt.plot(t, formulas[:, 10], '-ro', label="F 0.2")
    plt.ylabel('F 0.2')
    plt.legend()

    # plot 7 : t vs. F 0.15 Score
    plt.subplot(8, 1, 7)
    plt.plot(t, formulas[:, 11], '-ro', label="F 0.15")
    plt.ylabel('F 0.15')
    plt.legend()

    # arranging x axis labels
    ax = plt.gca()
    ax.set_xticks(t)
    ax.set_xticklabels(t)

    # plot 8 : t vs. F 0.1 Score
    plt.subplot(8, 1, 8)
    plt.plot(t, formulas[:, 12], '-ro', label="F 0.1")
    plt.ylabel("F 0.1")
    plt.legend()

    # arranging plot 3 view
    #[xmin, xmax, ymin, ymax] = plt.axis()
    #y_axis_space = (ymax - ymin) / 5
    #plt.axis([xmin, xmax, ymin - y_axis_space, ymax + y_axis_space])

    # arranging x axis labels
    ax = plt.gca()
    ax.set_xticks(t)
    ax.set_xticklabels(t)

    # plt.legend(bbox_to_anchor=(0.8, 1), loc=2, borderaxespad=0.)
    plt.show()

    # plt.plot(t,tp_over_fp_arr,'c-',label = '(tp/fp)*20')
    # plt.plot(t,formulas[:,4],'r-',label = 'precision')
    # plt.plot(t,formulas[:,5]*1000,'y-',label = 'recall*1000')


    #   plt.axis([0,20,0,60])
    #   plt.legend()
    #   plt.show()
    #   for i in xrange(20):
    #       if (tp_over_fp_arr[i]>1 and tp_over_fp_arr[i]<990):
    #        print('i: '  + str(i) + ', val: ' +  str(tp_over_fp_arr[i]))


