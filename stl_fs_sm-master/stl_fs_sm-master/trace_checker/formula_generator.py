
from . import formula_utilities as U
from . import STL


# See tests for the details of this class.


def check_idempotence(op, lf, rf, set_valued_metrics):
  #check for strict equality between two formulas
  if set_valued_metrics and op == '|': #(x = 3) | (x = 4) is valid
    return True

  if lf.to_formula() == rf.to_formula():
    return False

  return True

def check_associativity(op, lf, rf):
  #Left-associativity
  #If a new formula will be constructed with the latest used operator it is added to the front.
  #Allows formulas in the form of (p | q) | r but not p | (q | r)

  if rf.op == op:
    return False
  
  return True

def check_repeated_unary(op, lf):
  #if two unary operators are consecutively added it is redundant since there exists a formula with less operators
  # !!(x0 > p0) = (x0 > p0)
  # P 0 pP (P 0 pP (x0 > p0)) = P 0 pP (x0 > p0) it is also true for A 
  if lf.op == op:
    return False
  
  return True

def check_absorption(op, lf, rf):

  #Absorption law states : p | (p & q) = p and p & (p | q) = p
  #This function checks the law
  lf_formula = lf.to_formula()
  rf_formula = rf.to_formula()

  if U.is_binary(rf.op) and U.is_boolean(rf.op):
    if lf_formula == rf.left_node.to_formula() or lf_formula == rf.right_node.to_formula():
      return False

  if U.is_binary(lf.op) and U.is_boolean(lf.op):
    if rf_formula == lf.right_node.to_formula() or rf_formula == lf.left_node.to_formula():
      return False
  
  return True

def check_distributivity(op, lf, rf):

  #Checks for distrubitive law i.e. (p & q) | (p & r) = p & (q | r)

  if lf.op == rf.op and U.is_boolean(lf.op) and U.is_binary(lf.op):
    #check if it is in the form (p & q) | (r & t)
    left1 = lf.left_node.to_formula() #p
    left2 = lf.right_node.to_formula() #q
    right1 = rf.left_node.to_formula() #r
    right2 = rf.right_node.to_formula() #t

    #if any one of p or q is equal to any one of r or t it has a equivalent formula with less operators
    if left1 == right1 or left1 == right2 or left2 == right1 or left2 == right2:
      return False

  return True

def check_de_morgan(op, lf, rf):
  #controls if applying de Morgan's Rule simplifies the formula 

  #Checks !(p & !q) => !p | q
  #If the operator is !, previous operator is & or |, and if the sub_formulas start with !, then that formula has an equivalent with less operators
  if op == '!':
    if U.is_binary(lf.op) and U.is_boolean(lf.op):
      if lf.right_node.op == '!' or lf.left_node.op == '!':
        return False
  
  #Checks the other direction of the rule: !p & !q => !(p | q)
  elif U.is_binary(op) and U.is_boolean(op):
    if lf.op == rf.op and lf.op == '!':
      return False
  
  return True

def check_not_conditions(op, lf, set_valued_metrics):

  #If the negation is followed by a 0 operator formula without the operand '=', that formula is redundant
  # !(x0 > p0) is roughly equivalent to (x0 < p0) for our purposes 
  if U.is_operand(lf.op) and not set_valued_metrics: 
    return False

  #If the negation is followed by another unary operator then it is again redundant
  #!(P 0 pP (x0 > p0) = A 0 pA ( !(x0 > p0)) and similarly !(A 0 pA (x0 > p0) = P 0 pP ( !(x0 > p0))
  if U.is_unary(lf.op) :
    return False

  return True

def check_redundancy(op, lf, rf = None, set_valued_metrics = []):
   
    #returns true if it is valid to construct the larger formula with given sub-formulas and operator
    #if lf and rf are equivalent returns false

    if U.is_binary(op) and U.is_boolean(op): #and,or
        return (check_idempotence(op, lf, rf, set_valued_metrics) and #checks strict equality
                check_associativity(op, lf, rf) and #checks for associativity rule
                check_absorption(op, lf, rf) and #checks for absorption rule
                check_distributivity(op, lf, rf) and  #checks distrubitivity rule
                check_de_morgan(op, lf, rf) ) #checks one direction of de Morgan
    
    if U.is_unary(op):
        if U.is_boolean(op): #not
            return (check_not_conditions(op, lf, set_valued_metrics) and #checks the cases for operator !
                    check_de_morgan(op,lf,rf) ) #checks reverse direction of de Morgan 
        
        return check_repeated_unary(op, lf) #Checks the repeated unary case
    return True

def generate_formula_tree_iterative(metric_list, operator_count, return_formula_string, set_valued_metrics=[], simplify=True, withoutS=False):
  """
  :param withoutS: (bool) if True, the formulas are generates without Since.
  """


  return_list = []
  for m in set_valued_metrics: # only equality
    stn = STL.SyntaxTreeNode()
    stn.op = '='
    stn.param = 'p' + str(m)
    stn.metric = m
    return_list.append(stn)

  for m in metric_list:
    if not m in set_valued_metrics:
      for op in ['>', '<']:
        stn = STL.SyntaxTreeNode()
        stn.op = op
        stn.param = 'p' + str(m)
        stn.metric = m
        return_list.append(stn)

  if operator_count == 0:
    if return_formula_string:
      return [t.to_formula() for t in return_list]
    return return_list

  #all_trees[operator_count] will be the final list of formulas
  #now only includes formulas with oc = 0
  all_trees = {}
  all_trees[0] = return_list

  if withoutS:
    operator_list = ['A', 'P'] + U.BooleanOperators
  else:
    operator_list = U.STLPastOperators + U.BooleanOperators

  for oc in range(1, operator_count+1):
    all_trees[oc] = []

    for op in operator_list:
      if U.is_binary(op):
        lc_count = oc
        if U.is_boolean(op):
          lc_count = 1 + int(oc/2)
        
        for lc in range(lc_count):
          for li in range(len(all_trees[lc])): # for li in xrange(len(all_trees[lc]))
            for ri in range(len(all_trees[oc-lc-1])): #for ri in xrange(len(all_trees[lc]))
              if simplify == True and U.is_boolean(op) and lc == oc-lc-1 and li < ri:
                break  #covers the commutative case, i.e. (p & q) is allowed but (q & p) is not allowed

              if simplify != True or check_redundancy(op,all_trees[lc][li], all_trees[oc-lc-1][ri]) == True:
                stn = STL.SyntaxTreeNode()
                stn.op = op
                stn.left_node = all_trees[lc][li]
                stn.right_node = all_trees[oc-lc-1][ri]
                all_trees[oc].append(stn)

      else:
        for lf in all_trees[oc - 1]:
          if simplify != True or check_redundancy(op,lf) == True:
            stn = STL.SyntaxTreeNode()
            stn.op = op
            stn.left_node = lf
            all_trees[oc].append(stn)

  return_list = all_trees[operator_count]

  if return_formula_string:
    return [t.to_formula() for t in return_list]
  return return_list


def generate_formula_tree(metric_list, operator_count, return_formula_string, set_valued_metrics=[]):

  return_list = []
  if operator_count == 0:
    for m in set_valued_metrics: # only equality
      stn = STL.SyntaxTreeNode()
      stn.op = '='
      stn.param = 'p' + str(m)
      stn.metric = m
      return_list.append(stn)

    for m in metric_list:
      if not m in set_valued_metrics:
        for op in ['>', '<']:
          stn = STL.SyntaxTreeNode()
          stn.op = op
          stn.param = 'p' + str(m)
          stn.metric = m
          return_list.append(stn)

    # for op in U.MetricOperators:
    #   for m in metric_list:
    #     stn = STL.SyntaxTreeNode()
    #     stn.op = op
    #     stn.param = 'p' + str(m)
    #     stn.metric = m
    #     return_list.append(stn)

    if return_formula_string:
      return [t.to_formula() for t in return_list]
    return return_list

  # Compute all with less number of operators:
  all_trees = {}
  for oc in range(operator_count):
    all_trees[oc] = generate_formula_tree(metric_list, oc, False, set_valued_metrics)

  # now combine them
  for op in U.BooleanOperators + U.STLPastOperators:

    if U.is_binary(op):
      # For symmetric operators like and/or, only go through the half
      lc_count = operator_count
      if U.is_boolean(op):
        lc_count = 1 + int(operator_count/2)
      for lc in range(lc_count):
        for lf in all_trees[lc]:
          for rf in all_trees[operator_count - lc - 1]:
            stn = STL.SyntaxTreeNode()
            stn.op = op
            stn.left_node = lf
            stn.right_node = rf
            return_list.append(stn)

    else:
      for lf in all_trees[operator_count - 1]:
        stn = STL.SyntaxTreeNode()
        stn.op = op
        stn.left_node = lf
        return_list.append(stn)

  if return_formula_string:
    return [t.to_formula() for t in return_list]
  return return_list


def generate_formula_tree_for_cause_mining(metric_list, control_metrics, operator_count, set_valued_metrics, withoutS=False):
  """
  generate_formula_tree_for_cause_mining returns STL formulas in the form:
  A(formula with one metric, one op) & (any formula with given oc)
  the motivation is that in such a form the construction of a controller will be easier

  Args:
    metric_list: list of metrics that will appear in formulas
    control_metrics: the metrics that we can control. These are the metrics that will appear in the first part of
    the formula. For example: say c0 is a control metric, the resulting formula will be in the form
    ( A 1 7 c0 > 9 ) & (any formula with oc = oc)
    operator_count: how many operators will be in the resulting formula between metrics
    set_valued_metrics: metrics that take discrete values from a predefined set
    formula with given operator_count, in the form ( A 0 k c_t </>/= p_t ) & ( any formula with oc = operator_count)
    withoutS: (bool) if True, the formulas are generated without Since.
    * the formulas in the right part of & are generated by generate_formula_tree
  Returns:
      list of generated formulas
      Note: The lower bounds of A parameters on the left side in all formulasare fixed to be 0.

  A reminder for today's dummy scenario: In our dummy traffic system case(06.2018), all control metrics are set_valued,
  and they are for now called x5 and x6, so the formula is of the form:
  (formula with one op) is in the form x5 = {0,1} or x6 = {0,1}, i.e. it contains traffic light info
"""
  if type(operator_count)is int:
    operator_count_lhs, operator_count_rhs = [0, operator_count]
  else:
    operator_count_lhs, operator_count_rhs = operator_count

  return_list_A_added = []

  if operator_count == -1:
    formulas_inside = generate_formula_tree_iterative(metric_list=control_metrics, operator_count=operator_count_lhs,
                                                      return_formula_string=False, set_valued_metrics=set_valued_metrics,
                                                      withoutS=withoutS)
    for frml in formulas_inside:
      stn = STL.SyntaxTreeNode()
      stn.op = 'P'
      stn.interval = STL.Interval(1,1)
      stn.left_node = frml
      return_list_A_added.append(stn)

  else:
    formulas_left_side_inside = generate_formula_tree_iterative(metric_list=control_metrics, operator_count=operator_count_lhs,
                                                                return_formula_string=False,
                                                                set_valued_metrics=set_valued_metrics,withoutS=withoutS)
    formulas_right_side_inside = generate_formula_tree_iterative(metric_list=metric_list, operator_count=operator_count_rhs,
                                                                 return_formula_string=False,
                                                                 set_valued_metrics=set_valued_metrics,withoutS=withoutS)
    for frml_left_side_inside in formulas_left_side_inside:
      for frml_right_side_inside in formulas_right_side_inside:
        stn = STL.SyntaxTreeNode()
        stn.op = '&'
        stn_left_side = STL.SyntaxTreeNode()
        stn_left_side.op = 'P'
        stn_left_side.interval = STL.Interval(1, 1)
        stn_left_side.left_node = frml_left_side_inside
        stn.left_node = stn_left_side
        stn_right_side = STL.SyntaxTreeNode()
        stn_right_side.op = 'P'
        stn_right_side.interval = STL.Interval('pT', 'pT')
        stn_right_side.left_node = frml_right_side_inside
        stn.right_node = stn_right_side
        return_list_A_added.append(stn)

  # Fix the lower bounds of A's in the left-side to 0.
  return_list = []
  for f in return_list_A_added:
    formula = f.to_formula()
  #  index_first_pA = formula.find('pA')
  #  return_list.append(formula[:index_first_pA] + '1' + formula[index_first_pA+2:])
    return_list.append(formula)

  return return_list
