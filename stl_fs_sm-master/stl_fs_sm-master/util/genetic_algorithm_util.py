import random
from optimization import evaluator

import copy
from constants import genetic_algorithm_constants
from constants import stl_constants
from trace_checker import STL

from multiprocessing import Pool
from trace_checker import formula_generator
from functools import partial


# GENERATE SAMPLE SPACE
def generate_sample_space(metric_list, set_valued_metrics, operator_counts):
    template_formula_list = []
    for oc in operator_counts:
        template_formula_list += (generate_sample_space_helper(metric_list, set_valued_metrics, oc))
    sample_space = []
    for index in range(genetic_algorithm_constants.SAMPLE_SPACE_SIZE):
        sample_space.append(random.choice(template_formula_list))
    return sample_space


# GENERATES TEMPLATE FORMULA LIST WITH OPERATOR COUNT
# TO BEHAVE FAIR TO OPERATOR COUNTS ELIMINATES SOME IF THE SIZE IS BIGGER THAN MAX
def generate_sample_space_helper(metric_list, set_valued_metrics, oc):
    template_formula_list = formula_generator.generate_formula_tree_iterative(metric_list, oc,
                                                                              return_formula_string=True,
                                                                              set_valued_metrics=set_valued_metrics)
    if len(template_formula_list) > genetic_algorithm_constants.SAMPLE_SPACE_SIZE:
        sample_space = random.sample(template_formula_list, genetic_algorithm_constants.SAMPLE_SPACE_SIZE)
    else:
        sample_space = template_formula_list
    sample_space = [formula for formula in sample_space if formula.split().count('S') < 2]
    return sample_space


# INJECT PARAMETERS TO FORMULA AND CALCULATE FITNESS VALUE
def convert_and_evaluate(formula_list, parallel_process_count, parameter_domains, folder_name, signal_file_base,
                         return_type, trace_count, metric_list, set_valued_metrics):
    nodes_list = []
    for formula in formula_list:
        formula = inject_parameters(formula, parameter_domains, metric_list, set_valued_metrics)
        formula = STL.infix_to_prefix(formula)
        syntax_tree_node = STL.SyntaxTreeNode()
        syntax_tree_node.initialize_node(formula.split(), 0)
        nodes_list.append(syntax_tree_node)

    pool = Pool(processes=parallel_process_count)
    fitness_partial = partial(insert_fitness_value_to_individual, folder_name, signal_file_base, return_type,
                              trace_count)
    results = (pool.map(fitness_partial, nodes_list))
    pool.close()
    pool.join()

    return results


# CONVERT TEMPLATE TREE INTO TREE WITH PARAMETERS
def inject_parameters(formula, parameter_domains, metric_list, set_valued_metrics):
    tree, parameter_domains_in_formula = generate_formula_from_template(formula, parameter_domains)
    tree = insert_parameter_to_formula(tree, parameter_domains_in_formula, metric_list, set_valued_metrics)
    return tree


# GENERATES FORMULA TEMPLATE
def generate_formula_from_template(template_formula, parameter_domains):
    # first process the formula:
    formula_tokens = template_formula.split()
    # tokens that start with p and has 2 characters:
    parameters = [p for p in formula_tokens if p[0] == 'p' and len(p) == 2]
    parameters_set = list(set(parameters))  # make unique

    parameter_domains_in_formula = {}
    for p in parameters_set:
        for i in range(parameters.count(p)):
            p_new = p + str(i)
            for j in range(len(formula_tokens)):
                if formula_tokens[j] == p:
                    formula_tokens[j] = p_new
                    parameter_domains_in_formula[p_new] = parameter_domains[p]
                    break
    new_formula = " ".join(formula_tokens)
    return new_formula, parameter_domains_in_formula


# REPLACE CHARACTER P WITH REAL PARAMETERS
def insert_parameter_to_formula(formula, parameter_domains_for_formula, metric_list, set_valued_metrics):
    parameter_list = list(parameter_domains_for_formula.keys())
    tmp_formula = formula
    for p in parameter_list:
        temp_p = p
        if str(p[1]) in set_valued_metrics:
            tmp_formula = tmp_formula.replace(p, str(random.choice(parameter_domains_for_formula[p])))
        else:
            lower_bound = parameter_domains_for_formula[p][0]
            upper_bound = parameter_domains_for_formula[p][1]
            tmp_formula = tmp_formula.replace(p, str(random.randint(lower_bound, upper_bound)))
    return tmp_formula


# CALCULATE FITNESS VALUE BY RETURN TYPE COUNT AND PROPORTIONATE SELECT
def proportionate_select(generation, return_type):
    if return_type.category == stl_constants.CATEGORY_MAXIMIZATION:
        total_fitness = sum([float(pair[1]) for pair in generation])
    elif return_type.category == stl_constants.CATEGORY_MINIMIZATION:
        total_fitness = sum([1 / float(pair[1]) for pair in generation])
    population_to_reproduce = []
    for i in range(0, genetic_algorithm_constants.SAMPLE_SPACE_SIZE):
        random_number = random.uniform(0.0, total_fitness)
        p = 0.0
        for tuple in generation:
            if return_type.category == stl_constants.CATEGORY_MAXIMIZATION:
                p +=  float(tuple[1])
            elif return_type.category == stl_constants.CATEGORY_MINIMIZATION:
                p += 1 / float(tuple[1])
            if p >= random_number:
                population_to_reproduce.append(tuple)
                break
    return population_to_reproduce


# CROSSOVER OPERATION FOR WHOLE POPULATION
def mass_crossover(population_to_reproduce, maximum_operator_count):
    random.shuffle(population_to_reproduce)
    parents_list = list(zip(population_to_reproduce[0::2], population_to_reproduce[1::2]))
    next_generation = []
    for parents in parents_list:
        offsprings = (crossover(parents[0][0], parents[1][0], maximum_operator_count))
        next_generation.append(offsprings[0])
        next_generation.append(offsprings[1])

    return next_generation


def crossover(parent1, parent2, maximum_operator_count):
    flag = True

    while flag or temp_parent1.get_operator_count() > maximum_operator_count or temp_parent1.to_formula().split().count(
            'S') > 1 or temp_parent2.get_operator_count() > maximum_operator_count or temp_parent2.to_formula().split().count(
            'S') > 1:
        flag = False
        temp_parent1 = copy.deepcopy(parent1)
        temp_parent2 = copy.deepcopy(parent2)

        sub_tree1, route1 = copy.deepcopy(temp_parent1.random_node())
        sub_tree2, route2 = copy.deepcopy(temp_parent2.random_node())


        temp_parent1.cross_over(sub_tree2, route1)
        temp_parent2.cross_over(sub_tree1, route2)

    return temp_parent1, temp_parent2

# MUTATION OPERATION FOR WHOLE POPULATION
def mass_mutate(population, parameter_domains, metric_list, set_valued_metrics):
    for individual in population:
        if random.random() < genetic_algorithm_constants.PROBABILITY_OF_MUTATION_OPERATION:
            individual.mutate(parameter_domains, metric_list, set_valued_metrics)


def insert_fitness_value(population, folder_name, signal_file_base, return_type, trace_count):
    pool = Pool(processes=genetic_algorithm_constants.PARALLEL_PROCESS_COUNT)
    fitness_partial = partial(insert_fitness_value_to_individual, folder_name, signal_file_base, return_type,
                              trace_count)
    fitness_inserted_population = (pool.map(fitness_partial, population))
    pool.close()
    pool.join()
    return fitness_inserted_population


def insert_fitness_value_to_individual(folder_name, signal_file_base, return_type, trace_count, stn):
    return stn, float(evaluator.evaluate_signals('', folder_name, signal_file_base, trace_count, '', return_type,
                                                 stn))


def eliminate_tress(population):
    population = [formula for formula in population if formula.to_formula().split().count('S') < 2]
    return population


def get_parameter_domain_for_op(parameter_domains, param):
    return parameter_domains.get('p' + str(param))

