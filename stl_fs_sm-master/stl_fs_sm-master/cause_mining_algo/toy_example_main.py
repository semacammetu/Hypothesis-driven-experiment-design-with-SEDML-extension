import numpy
import copy
import random
import time

import cause_mining_algo as cma
from constants import stl_constants
from signal_generation import sg
from trace_checker import STL
from cause_mining_algo import controller_helper_funs as hf
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from . import syntactically_cosafe_form as scf

Game_Matrix = "global"

"""
read_game_map() reads the file in 'test_data/toy_example_data/game_map' and copies the values to the global Game_Matrix.
The game has one control input u in {1,2,3,4} the values of which correspond to {north,east,south,west}.
The game has one system input x = (row_no, coloumn_no).
If the location of the robot (i.e. xk = (row_no, coloumn_no)) correspond to a value marked by 1 in the game_map 
(i.e. Game_Map[row_no,coloumn_no]==1), then in the label file, the time point k is marked 1. Otherwise, it is marked 0.
toy_example_step_function(xk, uk) takes the values of x and u in time point k and returns the value of x in time point 
k+1 (the u value this function returns is unimportant and is not used anywhere, I just tried to make in the same form 
as some other functions)
generate_random_traces() generates random traces from the given game_map.

"""

def generate_random_traces():
    trace_count = 20
    duration = 100
    folder_name = 'test_data/toy_example_data/'
    tc = 0
    while tc < trace_count:
        f_signal_name = folder_name + "test_" + str(tc)
        f_label_name = f_signal_name + "_label"
        f_s = open(f_signal_name, 'w')
        f_l = open(f_label_name, 'w')

        time = 0
        row_cnt, col_cnt = numpy.shape(Game_Matrix)
        # comment one of the two following lines to decide on the initial position of the robot.
        # x = (3, 2)  # initially the robot starts from the left top corner of the rectangle
        x = (random.randint(0, row_cnt-1), random.randint(0, col_cnt-1))  # initial point completely random
        while time <= duration:
            u = random.choice([1, 2, 3, 4])  # [north, east, south, west]
            f_s.write(
                "%s %s %s\n" % (str(time), " ".join([str(x[0]) + " " + str(x[1])]), " ".join([str(u)])))
            qual = 1 if (Game_Matrix[x[0]][x[1]] == 1) else 0
            f_l.write("%s %s\n" % (str(time), str(qual)))
            x, _ = toy_example_step_function(x, u)

            time += 1

        f_s.close()
        f_l.close()
        print("Toy Ex: Done with generate basic traces, trace no" + str(tc))
        tc += 1

def read_game_map():
    file_name = 'test_data/toy_example_data/game_map'
    file = open(file_name, 'r')
    line1 = file.readline()[0:-1]
    file_array = []
    file_array.append(line1)
    for line in file:
        if len(line)>2:
            file_array.append(line[0:-1])
    coloumns = len(line1)-2
    rows = len(file_array)-2
    Game_Matrix = numpy.zeros(shape=(rows, coloumns), dtype=int)  # a boolean matrix where unpassable places are 1,
    #  whereas passables are 0.

    for line_no in range(1, len(file_array)-1):
        for letter in range(1, len(line1)-1):
            if file_array[line_no][letter] == str(1):
                Game_Matrix[line_no-1][letter-1] = 1
    return Game_Matrix

def toy_example_step_function(xk, uk):
    """

    Args:
        xk: a tuple identifying the place of the robot in the matrix by row and coloumn number i.e. (row, coloumn)
        uk: in {1,2,3,4}: {north, east, south, west}

    Returns: the new place of the robot, i.e. a new xk tuple and a random uk

    """

    row, col = xk
    row_cnt, col_cnt = numpy.shape(Game_Matrix)

    if type(uk) == list:
        uk = uk[0]

    if uk == 1:
        new_place = (row-1, col)
    elif uk == 2:
        new_place = (row, col+1)
    elif uk == 3:
        new_place = (row+1, col)
    elif uk == 4:
        new_place = (row, col-1)
    else:
        new_place = (0, 0)
        print("there is a problem in the toy example about the control inputs")

    if new_place[0] < 0:
        new_place = (0, new_place[1])
    elif new_place[0] >= row_cnt - 1:
        new_place = (row_cnt - 1, new_place[1])
    if new_place[1] < 0:
        new_place = (new_place[0], 0)
    elif new_place[1] >= col_cnt - 1:
        new_place = (new_place[0], col_cnt - 1)

    GM_cpy = copy.deepcopy(Game_Matrix)
    GM_cpy[new_place[0]][new_place[1]] = 8
    #print GM_cpy
    return new_place, uk

def heuristic_toy_example(pc, valuation_limit, folder_name, trace_count, signal_file_base, return_type,
                          operator_count_limit, withoutS=False, controllable_formulas=True):
    """
    Calls cause_mining_algorithm from cause_mining_algo package with traffic data.

    Returns: best formula in prefix form

    """


    print("---------------------------------------------------------------------------------------")
    print("                           heuristic_toy_example ")
    print("---------------------------------------------------------------------------------------")
    start_time = time.time()
    metric_list = ['0', '1', '2']
    control_metrics = ['2']
    set_valued_metrics = ['2']

    row_cnt, col_cnt = numpy.shape(Game_Matrix)

    parameter_domains = {'p0': range(0, row_cnt, 1), 'p1': range(0, col_cnt, 1), 'p2': [1, 2, 3, 4],
                         'pA': range(0, 4, 1), 'pP': range(0, 6, 2), 'pS': range(0, 3, 1), 'pT': [1,2]}
    save = True
    result_file = 'min_max'
    strictly_increasing_oc = False
    # operator_count = -1  # search until oc == operator_count (operator_count included)
    best_result = cma.cause_mining_heuristic.cause_mining_algorithm(metric_list=metric_list, control_metrics=control_metrics,
                                                                set_valued_metrics=set_valued_metrics,
                                                                parameter_domains=parameter_domains,
                                                                folder_name=folder_name, trace_count=trace_count,
                                                                signal_file_base=signal_file_base, process_count=pc,
                                                                save=save, result_file=result_file,
                                                                return_type=return_type,
                                                                strictly_increasing_oc=strictly_increasing_oc,
                                                                valuation_limit=valuation_limit,
                                                                operator_count_limit=operator_count_limit,
                                                                withoutS=withoutS, controllable_formulas=controllable_formulas)  # type: FormulaValuation
                                                                                    # formula is in prefix form
    print("Best Result is : " + best_result.formula + "\nWith the Valuation : " + str(best_result.valuation))

    end_time = time.time()
    print("")
    print("---------------------------------------------------------------------------------------")
    print("heuristic_toy_example ended in %s seconds" % str(end_time - start_time))
    print("---------------------------------------------------------------------------------------")
    print("folder name: " + folder_name)
    print("trace count: " + str(trace_count))
    print("processor count: " + str(pc))
    print("parameter domains: " + str(parameter_domains))
    print("return type: " + return_type.name)
    print("strictly increasing: " + str(strictly_increasing_oc))
    print("heuristic searched until operator count: " + str(operator_count_limit))
    print("valuation limit: " + str(valuation_limit))


    return best_result.formula  # prefix formula (string)

def search_all_search_space_toy_example(cause_limit, pc, return_type, folder_name, trace_count, signal_file_base,
                                        operator_count_limit=-1, upto=True, withoutS=False, controllable_formulas=True):
        print("---------------------------------------------------------------------------------------")
        print("                           search_all_search_space_toy_example ")
        print("---------------------------------------------------------------------------------------")
        start_time = time.time()
        metric_list = ['0', '1', '2']
        control_metrics = ['2']
        set_valued_metrics = ['2']

        row_cnt, col_cnt = numpy.shape(Game_Matrix)

        parameter_domains = {'p0': range(0, row_cnt, 1), 'p1': range(0, col_cnt, 1), 'p2': [1, 2, 3, 4],
                             'pA': range(0, 4, 1), 'pP': range(0, 6, 2), 'pS': range(0, 3, 1), 'pT': [1, 2]}

        best_result = cma.search_all_search_space.search_all_search_space(metric_list=metric_list,
                                                                      control_metrics=control_metrics,
                                                                      set_valued_metrics=set_valued_metrics,
                                                                      parameter_domains=parameter_domains,
                                                                      folder_name=folder_name, trace_count=trace_count,
                                                                      signal_file_base=signal_file_base,
                                                                      process_count=pc, return_type=return_type,
                                                                      oc_limit=operator_count_limit,
                                                                      cause_limit=cause_limit, upto=upto,
                                                                      withoutS=withoutS, controllable_formulas=controllable_formulas)  # type: FormulaValuation
        print("Best Result is : " + best_result.formula + "\nWith the Valuation : " + str(best_result.valuation))

        end_time = time.time()
        print("")
        print("---------------------------------------------------------------------------------------")
        print("search_all_search_space_toy_example ended in %s seconds" % str(end_time - start_time))
        print("---------------------------------------------------------------------------------------")
        print("folder name: " + folder_name)
        print("trace count: " + str(trace_count))
        print("processor count: " + str(pc))
        print("parameter domains: " + str(parameter_domains))
        print("return type: " + return_type.name)
        print("searched until operator count: " + str(operator_count_limit))
        return best_result.formula


def controller_n_iterations(n, heuristic):
    folder_name = 'test_data/toy_example_data/'
    trace_count = 20
    signal_file_base = 'test'
    signal_file_rest = ""
    duration = 100

    cause_limit = 1
    oc_limit = 0
    pc = 8
    return_type = stl_constants.__F_03_SCORE
    withoutS = True
    upto = False

    uk_domain = [1, 2, 3, 4]
    uk_count = 1

    violation_formula = ' ! ( x0 = 0 ) & ! ( x1 = 5 ) & ! ( x1 = 6 ) '  # violation formula of game_map2
    violation_formula2 = '! ( ( x0 < 2 ) & ( x1 < 4 ) ) & ! ( ( x0 > 3 ) & ( x1 > 3 ) )'  # violation formula of game_map

    viol_formula_prefix = STL.infix_to_prefix(violation_formula2)

    formula_list = []

    valuation_limit = 0.1
    operator_count_limit_heuristic = 100

    label_cnt = hf.label_count(folder_name=folder_name, label_file_base='test_', label_file_rest='_label',
                               trace_count=trace_count)
    print("label count before the controller: " + str(label_cnt))
    for i in range(0, n):
        if heuristic:
            cause_formula_prefix = heuristic_toy_example(pc=pc, folder_name=folder_name, valuation_limit=valuation_limit,
                                                         trace_count=trace_count, signal_file_base=signal_file_base,
                                                         operator_count_limit=operator_count_limit_heuristic,
                                                         return_type=return_type, withoutS=withoutS)  # returns prefix formula (string)

        else:
            best_formula = search_all_search_space_toy_example(cause_limit=cause_limit, pc=pc, return_type=return_type,
                                                               folder_name=folder_name, trace_count=trace_count,
                                                               signal_file_base=signal_file_base, upto=upto,
                                                               operator_count_limit=oc_limit, withoutS=withoutS)
            if best_formula == "":
                print("no formula with positive valuation")
                break
            cause_formula_prefix = STL.infix_to_prefix(best_formula)

        cma.cause_mining_main.print_detailed_result(prefix=1, formula=cause_formula_prefix, folder_name=folder_name,
                                                    signal_file_base=signal_file_base, signal_file_rest=signal_file_rest,
                                                    trace_count=trace_count)

        formula_list.append(cause_formula_prefix)
        cause_formula_prefix = cma.helper_funs.concat_with_or_prefix(formula_list)

        sg.controller(folder_name=folder_name, name='test', trace_count=trace_count, duration=duration,
                      viol_formula=viol_formula_prefix, cause_formula=cause_formula_prefix,
                      step_function=toy_example_step_function, xk_initialized=(3, 4), uk_domain=uk_domain,
                      uk_count=uk_count, num_to_let=False)

        label_cnt = hf.label_count(folder_name=folder_name, label_file_base='test_', label_file_rest='_label',
                                    trace_count=trace_count)
        print("label count after controller " + str(i) + " is: " + str(label_cnt))

        if label_cnt == 0:
            break

def show_trajectory():
    """

    Takes the trajectories from given files of toy example trajectories, adds them and prints a heat map that shows
    the exploration rate of the robot in the map.

    """
    # folder_name = 'test_data/toy_example_data/ex1_trajectory/'
    folder_name = 'test_data/toy_example_data/'
    trace_count = 20
    duration = 100
    row_cnt = 8
    coloumn_cnt = 7

    font_size_numbers = 20
    font_size_labels = 26
    font_size_colorbar = 20

    Matrix = numpy.zeros(shape=(row_cnt, coloumn_cnt), dtype=int)  # a boolean matrix where unpassable places are 1,

    chosen_index = 4
    tc = 0
    while tc < trace_count:
        f_signal_name = folder_name + "test_" + str(tc)
        f_s = open(f_signal_name, 'r')
        lines = f_s.readlines()

        time = 0
        while time <= duration:
            _, row, col, _ = lines[time].split()
            Matrix[int(row)][int(col)] += 1
            time += 1

        f_s.close()
        print("Toy Ex: Done with show trajectory, trace no" + str(tc))
        print(Matrix)
        if tc == chosen_index:
            chosen_Matrix = copy.deepcopy(Matrix)
        tc += 1

    sum_val = chosen_Matrix.sum()
    print("sum_val: " + str(sum_val))
    ratio_Matrix = numpy.zeros(shape=(row_cnt, coloumn_cnt), dtype=float)
    for i in range(row_cnt):
        for j in range(coloumn_cnt):
            if chosen_Matrix[i][j] == 0:
                ratio_Matrix[i][j] = 0
            else:
                ratio_Matrix[i][j] = float(chosen_Matrix[i][j])/float(sum_val)


    plt.figure(figsize=(5.9 , 5))

    plt.xticks(list(range(coloumn_cnt)), fontsize=font_size_numbers)
    plt.title('$x^1$', fontsize=font_size_labels)
    plt.yticks(list(range(row_cnt)), fontsize=font_size_numbers)
    plt.ylabel('$x^0$', fontsize=font_size_labels)

    ax = plt.gca()

    ax.set_xticks([x - 0.5 for x in range(1, coloumn_cnt)], minor=True)
    ax.set_yticks([y - 0.5 for y in range(1, row_cnt)], minor=True)
    plt.grid(which="minor", ls="-", lw=2)


    # plot a heatmap for the chosen Matrix
    plt.imshow(ratio_Matrix, cmap='hot_r', interpolation='nearest', vmin = 0, vmax = 0.1)

    cbar = plt.colorbar()
    cbar.ax.tick_params(labelsize=font_size_colorbar)

    plt.show()

    # plot game map
    #plt.imshow(Game_Matrix, cmap='Greys', interpolation='nearest', vmin = 0, vmax = 0.1, alpha= 0.5)

    #plt.show()

def find_best_formula(heuristic, controllable_formulas):
    folder_name = 'test_data/toy_example_data/'
    trace_count = 20
    signal_file_base = 'test'
    signal_file_rest = ""
    duration = 100

    if controllable_formulas:
        oc_limit_lhs = 1
        oc_limit_rhs = 0
        oc_limit = [oc_limit_lhs, oc_limit_rhs]
    else:
        oc_limit = 2
    cause_limit = 1
    pc = 8
    return_type = stl_constants.__F_03_SCORE
    withoutS = True
    upto = False

    valuation_limit = 0.0001
    operator_count_limit_heuristic = 100

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

    if heuristic:
        cause_formula_prefix = heuristic_toy_example(pc=pc, folder_name=folder_name,
                                                     valuation_limit=valuation_limit,
                                                     trace_count=trace_count, signal_file_base=signal_file_base,
                                                     operator_count_limit=operator_count_limit_heuristic,
                                                     return_type=return_type,
                                                     withoutS=withoutS, controllable_formulas=controllable_formulas)  # returns prefix formula (string)

    else:
        best_formula = search_all_search_space_toy_example(cause_limit=cause_limit, pc=pc, return_type=return_type,
                                                           folder_name=folder_name, trace_count=trace_count,
                                                           signal_file_base=signal_file_base, upto=upto,
                                                           operator_count_limit=oc_limit, withoutS=withoutS,
                                                           controllable_formulas=controllable_formulas)
        cause_formula_prefix = STL.infix_to_prefix(best_formula)

    cma.cause_mining_main.print_detailed_result(prefix=1, formula=cause_formula_prefix, folder_name=folder_name,
                                                signal_file_base=signal_file_base,
                                                signal_file_rest=signal_file_rest,
                                                trace_count=trace_count)

    return cause_formula_prefix


def toy_example_main():

    global Game_Matrix
    Game_Matrix = read_game_map()


    #show_trajectory()


    generate_random_traces()
    #controller_n_iterations(n=100, heuristic=False)
    p_formula = find_best_formula(heuristic=True, controllable_formulas = False)
    X_formula = scf.return_sc_form(p_formula, prefix=True)
    formula_with_atomic_props, dict = scf.turn_inequalities_to_atomic_propositions(X_formula)
    print(formula_with_atomic_props, dict)
