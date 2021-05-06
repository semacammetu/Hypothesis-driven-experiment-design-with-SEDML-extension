from typing import Any

import trace_checker.STL as STL
from constants import stl_constants
from util import metrics_util
from cause_mining_algo import helper_funs


def evaluate(formula, signal_file_name, label_file_name, stn, return_type, past_results=[]):
    """
    evaluates the given formulas false_positive, false_negative, true_positive, true_negative results in the given files
    end returns the necessary ones based on the result_type. If there are past_results, all formulas are concatenated with
    or and the resulting formula's results are returned.

    Args:
        formula: prefix formula
        signal_file_name:
        label_file_name:
        stn:
        return_type: one of the types in stl_constants, determines the valuation best_result will be chosen based on in
                     evaluate_signals.
        past_results: a list of formula valuations (formulas inside being prefix)
        If past_results is not empty, formula and the formulas in past_results are concatenated using "or" and
        evaluation is done based on the concatenated formula.

    Returns: if return_type is TYPE_RATIO;      true positives / # of data points is returned
             if return_type is TYPE_MISMATCH;   # of data points - true positives is returned
             else;                              detailed_result (i.e. an array of false_positive, false_negative,
                                                true_positive, true_negative is returned

    """

    # Construct syntax tree
    if stn and past_results == []:
        stn.clean()
    else:
        # create new formula by concatenating the formula with past formulas with or, and compute this formula on tests
        new_formula = formula
        for frml in past_results:
            new_formula = ' | ' + new_formula + ' ' + frml.formula
        stn = STL.SyntaxTreeNode()
        stn.initialize_node(new_formula.split(), 0)

    result = 0
    counter = 0
    # detailed result is false_positive, false_negative, true_positive, true_negative
    detailed_result = [0, 0, 0, 0]

    skip_count = 10  # skip the first 10 data points, not important in monitoring.
    sc = 0

    with open(signal_file_name, 'r') as sf, open(label_file_name, 'r') as lf:
        for ts, te in zip(sf, lf):
            s = ts.split()
            t = s[0]
            s = s[1:]
            _, e = te.split()
            t = float(t)
            s = [float(x) for x in s]
            e = float(e)
            while t > stn.nt:
                stn.compute_qv(STL.DataPoint(value=s, time=stn.nt))
                if sc > skip_count:
                    result += (stn.qv > 0) == ep
                    counter += 1
                    # label is false
                    if (ep == 0):
                        # if stn.qv > 0 is true then it is false positive
                        # if stn.qv > 0 is false then it is true negative
                        detailed_result = (detailed_result[0] + int((stn.qv > 0) != ep), detailed_result[1],
                                           detailed_result[2], detailed_result[3] + int((stn.qv > 0) == ep))
                    # label is true
                    else:
                        # if stn.qv > 0 is false then it is false negative
                        # if stn.qv > 0 is true then it is true positive
                        detailed_result = (detailed_result[0], detailed_result[1] + int((stn.qv > 0) != ep),
                                           detailed_result[2] + int((stn.qv > 0) == ep), detailed_result[3])
                else:
                    sc += 1

            stn.compute_qv(STL.DataPoint(time=t, value=s))
            if sc > skip_count:
                result += (stn.qv > 0) == e
                counter += 1
                # label is false
                if (e == 0):
                    # if stn.qv > 0 is true then it is false positive
                    # if stn.qv > 0 is false then it is true negative
                    detailed_result = (
                    detailed_result[0] + int((stn.qv > 0) != e), detailed_result[1], detailed_result[2],
                    detailed_result[3] + int((stn.qv > 0) == e))
                # label is true
                else:
                    # if stn.qv > 0 is false then it is false negative
                    # if stn.qv > 0 is true then it is true positive
                    detailed_result = (detailed_result[0], detailed_result[1] + int((stn.qv > 0) != e),
                                       detailed_result[2] + int((stn.qv > 0) == e), detailed_result[3])
            else:
                sc += 1
            sp = s
            ep = e

    if return_type.type == stl_constants.TYPE_RATIO:
        return float(result) / counter
    if return_type.type == stl_constants.TYPE_MISMATCH:  # return the mismatch count
        return counter - result
    else:  # return detailed results
        return detailed_result


def evaluate_signals(formula, folder_name, signal_file_base, trace_count, signal_file_rest, return_type, stn=None,
                     past_results=[]):
    """
    Checks if the formula's lower bounds & upper bounds are within the limits. Calls evaluate, returns valuation based
    on return_type.
    Args:
        formula: prefix formula
        folder_name:
        signal_file_base:
        trace_count:
        signal_file_rest:
        return_type:
        stn:
        past_results:

    Returns:

    """

    # Below code piece checks if lower bounds are smaller than upper bounds in "formula",
    # if not, it returns the worst value.
    if not stn:
        stn = STL.SyntaxTreeNode()
        stn.initialize_node(formula.split(), 0)

    flag = helper_funs.traverse_formula_check_intervals(stn)
    if not flag:
        if return_type.category == stl_constants.CATEGORY_MAXIMIZATION:
            return 0.0
        elif return_type.type == stl_constants.__DETAILED:
            return [0, 0, 0, 0]
        elif return_type.category == stl_constants.CATEGORY_MINIMIZATION:
            return stl_constants.MAX_EVAL

    # start evaluation
    count = 0
    total = 0
    detailed_result = [0, 0, 0, 0]
    for i in range(trace_count):
        s_file = folder_name + signal_file_base + '_' + str(i) + signal_file_rest
        label_file = s_file + "_label"
        r = evaluate(formula=formula, signal_file_name=s_file, label_file_name=label_file, stn=stn,
                     return_type=return_type, past_results=past_results)
        count += 1
        if return_type.type == stl_constants.TYPE_RATIO or return_type.type == stl_constants.TYPE_MISMATCH:
            total += r  # total number of mismatches for ret_type = MISMATCH
        else:
            detailed_result = [detailed_result[0] + r[0], detailed_result[1] + r[1], detailed_result[2] + r[2],
                               detailed_result[3] + r[3]]  # fp, fn, tp, tn

    if return_type.type == stl_constants.TYPE_RATIO:
        return total / count
    elif return_type.type == stl_constants.TYPE_MISMATCH:
        return total
    elif return_type.type == stl_constants.TYPE_PRECISION:
        return float(metrics_util.calculate_precision(detailed_result))
    elif return_type.type == stl_constants.TYPE_RECALL:
        return float(metrics_util.calculate_recall(detailed_result))
    elif return_type.type == stl_constants.TYPE_F1_SCORE:
        return float(metrics_util.calculate_f1_score(detailed_result))
    elif return_type.type == stl_constants.TYPE_FHALF_SCORE:
        return float(metrics_util.calculate_fhalf_score(detailed_result))
    elif return_type.type == stl_constants.TYPE_F_015_SCORE:
        return float(metrics_util.calculate_f_Beta_score(detailed_result, 0.15))
    elif return_type.type == stl_constants.TYPE_F_02_SCORE:
        return float(metrics_util.calculate_f_Beta_score(detailed_result, 0.2))
    elif return_type.type == stl_constants.TYPE_F_03_SCORE:
        return float(metrics_util.calculate_f_Beta_score(detailed_result, 0.3))
    elif return_type.type == stl_constants.TYPE_F_04_SCORE:
        return float(metrics_util.calculate_f_Beta_score(detailed_result, 0.4))
    else:
        return detailed_result
