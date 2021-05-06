

from signal_generation import generator
from util import genetic_algorithm_util
from operator import itemgetter

from constants import genetic_algorithm_constants
from constants import stl_constants


def formula_search(metric_list, set_valued_metrics, operator_counts, folder_name, trace_count,
                   generate_signals, signal_file_base, process_count, save, return_type, maximum_operator_count,
                   parameter_domains):
    # If needed, generate signals.
    if generate_signals == "GAUS":
        generator.generate_signals(folder_name, signal_file_base, trace_count, process_count)
    elif generate_signals == "PUSH":
        generator.generate_signals_push(folder_name, signal_file_base, trace_count, process_count)

    sample_space = genetic_algorithm_util.generate_sample_space(metric_list, set_valued_metrics, operator_counts)

    generation = genetic_algorithm_util.convert_and_evaluate(sample_space, process_count, parameter_domains,
                                                             folder_name, signal_file_base, return_type,
                                                             trace_count, metric_list, set_valued_metrics)

    # ORDERING AND BEST SELECTION IS CHANGING REGARDING TO RETURN TYPE
    if return_type.category == stl_constants.CATEGORY_MINIMIZATION:
        best_tuple = min(generation, key=itemgetter(1))
        reverse = False
    else:
        best_tuple = max(generation, key=itemgetter(1))
        reverse = True

    best_result = best_tuple[1]
    best_formula = best_tuple[0].to_formula()

    # A COUNTER TO HOLD NO CHANGE DATA BETWEEN GENERATIONS
    no_change_counter = 0
    best_results_to_draw = []
    best_results_to_draw.append(best_result)
    iteration = 0
    while True:
        print('iteration ' + str(iteration))
        iteration += 1
        if (return_type.category == stl_constants.CATEGORY_MAXIMIZATION and best_result == 1) or (
                return_type.category == stl_constants.CATEGORY_MINIMIZATION and best_result == 0) or (
                no_change_counter > 100):
            break
        # SELECT INDIVIDUALS TO CREATE OFFSPRING
        selected_individuals_ro_reproduce = genetic_algorithm_util.proportionate_select(generation, return_type)
        new_generation = genetic_algorithm_util.mass_crossover(selected_individuals_ro_reproduce,
                                                               maximum_operator_count)
        genetic_algorithm_util.mass_mutate(new_generation, parameter_domains, metric_list, set_valued_metrics)
        new_generation = genetic_algorithm_util.insert_fitness_value(new_generation, folder_name, signal_file_base,
                                                                     return_type, trace_count)
        generation = sorted(generation, key=lambda t: t[1], reverse=reverse)[
                     :genetic_algorithm_constants.BEST_TO_CARRY_ON] + new_generation
        generation.sort(key=lambda t: t[1], reverse=reverse)

        if return_type.category == stl_constants.CATEGORY_MINIMIZATION:
            best_tuple = min(generation, key=itemgetter(1))
            if best_result <= best_tuple[1]:
                no_change_counter += 1
            else:
                best_result = best_tuple[1]
                best_formula = best_tuple[0].to_formula()
                no_change_counter = 0
        else:
            best_tuple = max(generation, key=itemgetter(1))
            if best_result >= best_tuple[1]:
                no_change_counter += 1
            else:
                best_result = best_tuple[1]
                best_formula = best_tuple[0].to_formula()
                no_change_counter = 0
        if best_result <= best_tuple[1]:
            no_change_counter += 1
        else:
            best_result = best_tuple[1]
            best_formula = best_tuple[0].to_formula()
            no_change_counter = 0
        best_results_to_draw.append(best_result)
        iteration_file = open('results/iteration' + str(iteration) + '.txt', 'w+')
        for item in generation:
            iteration_file.write("%s %s\n" % (str(item[1]), str(item[0].to_formula())))
        iteration_file.close()
        total_file = open('results/total.txt', 'a+')
        total_file.write("%s %s\n" % (str(best_result), str(best_formula)))

        print("Best Result: " + str(best_result))
        print("Best Formula: " + str(best_formula))

    if save:
        print("Best Result: " + str(best_result))
        print("Best Formula: " + str(best_formula))
        print("SAVING")

    return best_result, best_formula
