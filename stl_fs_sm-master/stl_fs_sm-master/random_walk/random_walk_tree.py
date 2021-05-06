from optimization import evaluator
from trace_checker import formula_utilities as U

class RandomWalkTree:

    total_number_of_evaluation = 0
    global_best = (None, None)
    def __init__(self):
        self.child_nodes = set()
        self.formula = ""
        self.score = 0
        self.parent = None

    def __str__(self, level=0):
        ret = "\t" * level + repr(self.formula + "------" + str(self.score)) + "\n"
        if self.child_nodes:
            for child in self.child_nodes:
                ret += child.__str__(level + 1)
        return ret

    def __repr__(self):
        return '<tree node representation>'

    def set_child_nodes(self, node_list):
        self.child_nodes = node_list

    def set_stl_formula(self, formula):
        self.formula = formula

    def init_random_walk_tree(self, formula="", score=0):
        self.child_nodes = set()
        self.formula = formula
        self.score = score
        if RandomWalkTree.global_best == (None, None):
            RandomWalkTree.global_best = (formula, score)

    def set_score(self, folder_name, sf_base, trace_count, return_type):
        self.score = evaluator.evaluate_signals(self.formula, folder_name, sf_base, trace_count, '',
                                                return_type,
                                                None)
        RandomWalkTree.total_number_of_evaluation += 1
        if self.score > RandomWalkTree.global_best[1]:
            RandomWalkTree.global_best = (self.formula, self.score)


    def add_child_node(self, child_node):
        # If it is not guaranteed that the score is increasing downwards
        # Then we should check for ancestor list 0f self whether contains child_node or not
        # In order to avoid infinite recursion
        self.child_nodes.add(child_node)
        child_node.parent = self

    def print_node_score(self):
        print(self.formula + "------" + str(self.score))
        if (self.child_nodes):
            for node in self.child_nodes:
                node.print_node_score()

    def walk(self, step_sizes, iteration=0, iteration_limit=0, folder_name='', sf_base='', trace_count=0,
             return_type=None, include_lower_bounds=False):

        """

            Args:
                step_sizes: parameter for step sizes of the parameter of the formula and upper and lower bounds
                iteration: in which iteration the algorithm is
                iteration_limit: maximum iteration for algorithm to run
                folder_name: the signal folder to evaluate generated formulas
                sf_base: signal file base for signals
                trace_count: number of signal files that involve in evaluation
                return_type: return type of the score

            Returns: VOID

        """
        if iteration > iteration_limit:
            return
        for key in list(step_sizes.keys()):
            tokenized_formula = self.formula.split()
            if key in tokenized_formula:
                indices = [i for i, x in enumerate(tokenized_formula) if x == key]
                # Any key may occur multiple times in a formula
                if key in U.STLPastOperators and include_lower_bounds:
                    a = []
                    for k in indices:
                        a.append(k - 1)
                    indices += a
                for index in indices :
                    # to find the parameter i.e. A 0 50
                    index_to_take_step = index + 2
                    #increment the parameter of the key by step size
                    tokenized_formula[index_to_take_step] = str(
                        int(tokenized_formula[index_to_take_step]) + step_sizes.get(key)[0])
                    #To check whether the new parameter is between the boundaries

                    if (step_sizes.get(key)[1][0] <= int(tokenized_formula[index_to_take_step]) <= step_sizes.get(key)[1][1]):
                        # Create the incremented version of the formula and push it as a child
                        # if it has a higher score
                        incremented_formula = ' '.join(str(e) for e in tokenized_formula)
                        incremented_child = RandomWalkTree()
                        incremented_child.init_random_walk_tree(formula=incremented_formula)
                        incremented_child.set_score(folder_name, sf_base, trace_count, return_type)
                        if (incremented_child.score > self.score):
                            self.add_child_node(incremented_child)
                            # recursive call
                            # TODO: Change it to iterative
                            incremented_child.walk(step_sizes, iteration + 1, iteration_limit, folder_name, sf_base,
                                                   trace_count,
                                                   return_type, include_lower_bounds)
                    # decrement the parameter of the key by 2 times step size
                    # because it is already incremented
                    tokenized_formula[index_to_take_step] = str(
                            int(tokenized_formula[index_to_take_step]) - step_sizes.get(key)[0])
                    tokenized_formula[index_to_take_step] = str(
                        int(tokenized_formula[index_to_take_step]) -   step_sizes.get(key)[0])
                    # to check whether the new parameter is between the boundaries
                    if (step_sizes.get(key)[1][0] <= int(tokenized_formula[index_to_take_step]) <= step_sizes.get(key)[1][
                        1]):
                        # Create the decremented version of the formula and push it as a child
                        # if it has a higher score
                        decremented_formula = ' '.join(str(e) for e in tokenized_formula)
                        decremented_child = RandomWalkTree()
                        decremented_child.init_random_walk_tree(formula=decremented_formula)
                        decremented_child.set_score(folder_name, sf_base, trace_count, return_type)
                        if (decremented_child.score > self.score):
                            self.add_child_node(decremented_child)
                            # recursive call
                            # TODO: Change it to iterative
                            decremented_child.walk(step_sizes, iteration + 1, iteration_limit, folder_name, sf_base,
                                                   trace_count,
                                                   return_type, include_lower_bounds)
                    tokenized_formula[index_to_take_step] = str(
                        int(tokenized_formula[index_to_take_step]) + step_sizes.get(key)[0])


    def generate_best_formula(self, step_sizes,  iteration_limit=0, folder_name='', sf_base='', trace_count=0,
             return_type=None, include_lower_bounds=False):
        self.reset()
        self.walk(step_sizes, 0, iteration_limit, folder_name, sf_base, trace_count, return_type, include_lower_bounds)
        return RandomWalkTree.global_best

    def reset(self):
        RandomWalkTree.global_best = (None, None)
        RandomWalkTree.total_number_of_evaluation = 0
