
from collections import namedtuple
from . import formula_utilities as U

from constants import genetic_algorithm_constants
import random
import numpy as np
import copy


class STLError(Exception):
  pass


BINARY_MAX = 1000
DataPoint = namedtuple('DataPoint', ['time', 'value'])


class Interval():
  """This class is used to manage the intervals of the temporal operators."""
  def __init__(self, lb, ub):
    self.lb = lb
    self.ub = ub

  def __add__(self, other):
    n = Interval(0, 0)
    n.ub = self.ub + other.ub
    n.lb = self.lb + other.lb
    return n

  def __sub__(self, other):
    n = Interval(0, 0)
    n.ub = self.ub - other.lb
    n.lb = self.lb - other.ub
    return n

  def update_bounds(self, ub=None, lb=0):
    if self.lb < lb:
      self.lb = lb
    if ub and self.ub > ub:
      self.ub = ub

class SyntaxTreeNode():
  """This class represents the syntax tree of an STL formula. The quantitative valuation is performed in this class."""
  def __init__(self):
    self.left_node = []
    self.right_node = []

    self.op = []
    self.metric = [] # index of the metric, i for xi
    self.interval = []
    self.signal_length = 0  # The required length for the formula, e.g. G [0, 2] x > 3, signal_length is 2.
    self.set_valued = False # metric can take values from a set, In this case, only = is allowed (not > < )
                            # Common usage is for binary variables, takes value from {0, 1}.

    self.data_points = [] # It will be a sorted list of DataPoints according to the time.
                          # The points from this list will be removed when dp.time < time - interval.ub.
                          # Efficient online monitoring algorithms will be implemented, for this case, the list will
                          # be sorted according to the value as well (increasing/or decreasing).

    self.data_points_to_add = [] # Sorted list according to time. The points from this list will be added when
                                 # dp.time <= time - interval.lb (when they are in the operator window.)

    self.data_points_r = [] # For binary temporal operators S (since) and U (until), data points from the right tree
    self.data_points_to_add_r = [] # For binary temporal operators S (since) and U (until),
                                   # data points to add for the right tree.
    self.qv = 0  # Quantitative valuation.
    self.nt = 0 # Expiration time.

    # The operator parameter, T for x0 < T.
    self.param = 0 # for now 1 dimensional signal

  def initialize_node(self, tokens, index):
    """
    This function initializes the tree with the formula stored in the index. It recursively constructs the sub-strees.

    Args:
      tokens: An array of strings. This is the formula.
      index: The index of the tokens array for the current node.
    Returns:
      An integer for the next index in the tokens array.
    """
    op = tokens[index]
    # It is an operand, so leaf node.
    if U.is_operand(op):
      self.metric = int(tokens[index][1:len(tokens[index])])
      if op == '=':
        self.set_valued = True
      self.op = tokens[index + 1]
      self.param = float(tokens[index + 2])
      return index + 3  # The index to continue construction.
    else:
      index_shift = 1  # the operator
      self.op = op
      self_length = 0
      # If it is not an STL operator, then it is a Boolean opertor. No need for extra processing here.
      if op in U.STLOperators:
        self.interval = Interval(int(tokens[index+1]), int(tokens[index+2]))
        index_shift += 2  # interval vars
        self_length = self.interval.ub
      self.left_node = SyntaxTreeNode()
      post_index = self.left_node.initialize_node(tokens, index + index_shift)
      if U.is_binary(op):
        self.right_node = SyntaxTreeNode()
        post_index = self.right_node.initialize_node(tokens, post_index)
        self.signal_length = self_length + max(self.right_node.signal_length, self.left_node.signal_length)
      else:
        self.signal_length = self_length + self.left_node.signal_length
      return post_index

  def _get_until_interval(self, index, time_points, signal_length):

    if not time_points:
      new_interval_1 = Interval(0, self.interval.lb)
      new_interval_1 = self._get_interval(index, time_points, new_interval_1, False, signal_length)
      return new_interval_1, self._get_interval(index, time_points, self.interval, False, signal_length)

  def _get_since_interval(self, index, time_points, signal_length, t):

    if not time_points:
      new_interval_1 = Interval(0, self.interval.lb)
      new_interval_1 = self._get_interval(index, time_points, new_interval_1, True, signal_length)
      new_interval_2 = self._get_interval(index, time_points, self.interval, True, signal_length)
      return new_interval_1, new_interval_2

    i1 = Interval(0, self.interval.lb)
    r1 = self._get_interval(index, time_points, i1, True, signal_length, t)
    r2 = self._get_interval(index, time_points, self.interval, True, signal_length, t)
    return r1, r2


  def _get_interval(self, index, time_points, interval, is_past, signal_length=None, t=None):
    """Compute indices for the resulting interval. This function handles different cases.
     Case 1: time_points is None. In this case the interval is computed as interval +- index.

     Case 2: time_points array is given.
    """
    new_interval = Interval(index, index)
    if not time_points:
      if is_past:
        new_interval -= interval
      else:
        new_interval += interval
      new_interval.update_bounds(ub=signal_length-1)
      return new_interval

    # Return the indices according to the time points and current time t
    if not is_past:
      return None  # TODO implement for the future operators

    time_interval = Interval(t, t)
    time_interval -= interval
    index_interval = Interval(0, index)
    # now find the corresponding indices, start from i:

    # Loop for upper bound:
    for x in range(index, -1, -1):
      if time_points[x] <= time_interval.ub:
        index_interval.ub = x
        break
    # Loop for lower bound:
    for x in range(index_interval.ub - 1, -1, -1):
      if time_points[x] <= time_interval.lb:
        index_interval.lb = x
        break

    return index_interval

  def compute(self, signal, index, time_points=None, t=None):
    """
    The function computes the quantitative valuation at "index" along "signal". The "time_points" gives the time stamp
    for each signal value. If it is not given, it is assumed that the signal is produced at each time step (discrete).

    Args:
      signal:  T x N dimensional array. N is the number of different metrics (the signal dimension). T is the signal
               length.
      index: An integer. The index for the array signal for the current evaluation.
      time_points: T x 1 array. Time stamps for the "signal"
      t: The current time. (only used if time_points is given.)

    Returns:
      The quantitative valuation.
    """
    if self.op == '&':
      return min(self.left_node.compute(signal, index, time_points, t),
                 self.right_node.compute(signal, index, time_points, t))
    if self.op == '|':
      return max(self.left_node.compute(signal, index, time_points, t),
                 self.right_node.compute(signal, index, time_points, t))
    if self.op == '!':
      return -1*self.left_node.compute(signal, index, time_points, t)

    # Future operators:
    if self.op == 'F':
      val = U.MIN_VAL

      r = self._get_interval(index, time_points, self.interval, False, len(signal))
      for x in range(r.lb, r.ub + 1):
        vc = self.left_node.compute(signal, x, time_points)
        val = vc if vc > val else val
      return val

    if self.op == 'G':
      val = U.MAX_VAL
      r = self._get_interval(index, time_points, self.interval, False, len(signal))
      for x in range(r.lb, r.ub + 1):
        ts = time_points[x] if time_points else None
        vc = self.left_node.compute(signal, x, time_points, ts)
        val = vc if vc < val else val
      return val

    if self.op == 'U':
      val = U.MIN_VAL
      min_phi1_val = U.MAX_VAL
      r1, r2 = self._get_until_interval(index, time_points, len(signal))
      for x in range(r1.lb, r1.ub):
        ts = time_points[x] if time_points else None
        min_phi1_val = min(min_phi1_val, self.left_node.compute(signal, x, time_points, ts))

      for x in range(r2.lb, r2.ub + 1):
        ts = time_points[x] if time_points else None
        phi2_val = self.right_node.compute(signal, x, time_points, ts)
        val = max(val, min(min_phi1_val, phi2_val))
        phi1_val = self.left_node.compute(signal, x, time_points, ts)
        if phi1_val < val:
          return val # we can stop the iteration, after this point the new value will always be less than val
        min_phi1_val = min(min_phi1_val, phi1_val)
      return val

    if self.op == 'P':
      val = U.MIN_VAL
      r = self._get_interval(index, time_points, self.interval, True, len(signal), t)
      for x in range(r.lb, r.ub + 1):
        ts = time_points[x] if time_points else None
        vc = self.left_node.compute(signal, x, time_points, ts)
        val = vc if vc > val else val
      return val

    if self.op == 'A':
      val = U.MAX_VAL
      r = self._get_interval(index, time_points, self.interval, True, len(signal), t)
      for x in range(r.lb, r.ub + 1): #xrange(max(index - self.interval.ub, 0), max(0, index - self.interval.lb + 1)):
        ts = time_points[x] if time_points else None
        vc = self.left_node.compute(signal, x, time_points, ts)
        val = vc if vc < val else val
      return val

    if self.op == 'S':
      val = U.MIN_VAL
      min_left = U.MAX_VAL
      r1, r2 = self._get_since_interval(index, time_points, len(signal), t)
      for x in range(r1.ub, r1.lb, -1):
        ts = time_points[x] if time_points else None
        t_left = self.left_node.compute(signal, x, time_points, ts)
        min_left = t_left if t_left < min_left else min_left
      pre_val = U.MIN_VAL
      for x in range(r2.ub, r2.lb - 1, -1):
        ts = time_points[x] if time_points else None
        t_right = self.right_node.compute(signal, x, time_points, ts)
        t_left = self.left_node.compute(signal, x, time_points, ts)
        min_left = min(t_left, min_left)
        val = min(t_right, min_left) if min(t_right, min_left) > val else val
        if val < pre_val:
          return pre_val
        else:
          pre_val = val

      return val
    # Base case, lead computation
    return self._compute_base(signal[index][self.metric])


  def _compute_base(self, x):
    if self.op == '>':
      return x - self.param
    if self.op == '<':
      return self.param - x
    if self.op == '=':
      if x == self.param:
        return BINARY_MAX
      else:
        return -BINARY_MAX

  def _remove_condition(self):
    if len(self.data_points) > 0:
      # self.data_points_to_add[0].value is the new point to add
      if self.op == 'P':
        return self.data_points[-1].value < self.data_points_to_add[0].value
        # keep a descending list for Previous op
      elif self.op == 'A':
        return self.data_points[-1].value > self.data_points_to_add[0].value
        # keep an ascending list for Always in the past op
    else:
      return False

  def _process_ordered_list(self, list_to_process, new_point, decreasing):
    last_dropped_point = None
    while len(list_to_process) > 0:
      if decreasing:
        if list_to_process[-1].value < new_point.value:
          last_dropped_point = list_to_process.pop()
        else:
          break
      else:
        if list_to_process[-1].value > new_point.value:
          last_dropped_point = list_to_process.pop()
        else:
          break
    if len(list_to_process) == 0 or list_to_process[-1].value != new_point.value:
      if last_dropped_point and len(list_to_process) > 0:
        list_to_process.append(DataPoint(time=last_dropped_point.time, value=new_point.value))
      else:
        list_to_process.append(new_point)

    return last_dropped_point

  def compute_nt(self, data_points, data_points_to_add, dropped_point):
    """Compute the expiration time, e.g., when the qv might change even if a new point has not arrived."""

    nt = U.MAX_VAL  # if it is the only one, it will never expire
    if len(data_points) > 1:
      # if dropped_point:  # This should be used for the computation, change the second ones nt to this:
      # data_points[-1] = DataPoint(time=dropped_point.time, value=data_points[1].value)
      nt = data_points[1].time + self.interval.ub  # when this point will expire, or if there is a point to add:

    if len(self.data_points_to_add) > 0:
      nt = min(nt, data_points_to_add[0].time + self.interval.lb)

    return nt

  def compute_qv(self, new_data_point):
    """
      This function computes the quantitative valuation when the new point arrives and returns a time point T at
      which the quantitative valuation can change even if a new point is not received.
      The caller function is RESPONSIBLE for calling this with a new data point with time upper bounded by T. Otherwise
      this one will produce an error.

      This only supports PAST STL.

      new_data_point: A DataPoint instance
    """
    # Arithmetic operator:
    if self.op in U.MetricOperators:
      # self.qv = self.param - new_data_point.value[self.metric] if self.op == '<' else new_data_point.value[self.metric] - self.param
      self.qv = self._compute_base(new_data_point.value[self.metric])
      self.nt = U.MAX_VAL  # never expire
      return  self.nt

    # Boolean operator
    if U.is_boolean(self.op):
      if self.op == '&' or self.op == '|':
        tr = self.right_node.compute_qv(new_data_point)
        tl = self.left_node.compute_qv(new_data_point)
        self.nt = min(tr,tl)
        if self.op == '&':
          self.qv = min(self.left_node.qv, self.right_node.qv)
        else:
          self.qv = max(self.left_node.qv, self.right_node.qv)
      if self.op == '!':
        self.left_node.compute_qv(new_data_point)
        self.nt = self.left_node.nt
        self.qv = -1*self.left_node.qv

      return self.nt

    # Temporal operator
    if self.op == 'P' or self.op == 'A':
      if self.nt < new_data_point.time:
        raise Exception('The valuation is changed between the last time stamp and the current one')

      # First compute the quantitative valuation for the inner formula:
      self.left_node.compute_qv(new_data_point)
      new_data_point = DataPoint(time=new_data_point.time,value=self.left_node.qv)


      if len(self.data_points_to_add) == 0 or self.data_points_to_add[-1].value != new_data_point.value:
        self.data_points_to_add.append(new_data_point)


      last_dropped_point = None
      if self.data_points_to_add[0].time <= new_data_point.time - self.interval.lb:
        decreasing = self.op == 'P'
        last_dropped_point = self._process_ordered_list(self.data_points, self.data_points_to_add.pop(0), decreasing)

      # Remove an expired point
      if len(self.data_points) > 1 and self.data_points[1].time <= new_data_point.time - self.interval.ub:
        z = self.data_points.pop(0)

      self.qv = self.data_points[0].value if len(self.data_points) > 0 else U.MIN_VAL
      # Compute nt now:
      nt = self.compute_nt(self.data_points, self.data_points_to_add, last_dropped_point)
      self.nt = min(nt, self.left_node.nt)  # Pick the minimum of this one and the inner formula. If the valuation
                                                # of the inner formula changes, this one can also change.
      return self.nt

    elif self.op == 'S':
      if self.nt < new_data_point.time:
        raise Exception('The valuation is changed between the last time stamp and the current one')

      self.left_node.compute_qv(new_data_point)
      self.right_node.compute_qv(new_data_point)

      xn = DataPoint(time=new_data_point.time, value=self.left_node.qv)
      yn = DataPoint(time=new_data_point.time, value=self.right_node.qv)

      # Remove expired point:
      if len(self.data_points) > 1 and self.data_points[1].time <= new_data_point.time - self.interval.ub:
        self.data_points.pop(0)
      if len(self.data_points_r) > 1 and self.data_points_r[1].time <= new_data_point.time - self.interval.ub:
        self.data_points_r.pop(0)

      # Add them to the to_add lists:
      if len(self.data_points_to_add) == 0 or self.data_points_to_add[-1].value != xn.value:
        self.data_points_to_add.append(xn)
      if len(self.data_points_to_add_r) == 0 or self.data_points_to_add_r[-1].value != yn.value:
        self.data_points_to_add_r.append(yn)


      # If the point to add is within the range:
      if self.data_points_to_add[0].time <= new_data_point.time - self.interval.lb:
        process_y = False
        process_x = False
        xn = self.data_points_to_add.pop(0)
        yn = self.data_points_to_add_r.pop(0)
        # 3 cases to check, 3 values, 6 way to order, first 2: xn, yn, qv and yn,xn,qv
        if min(xn.value, yn.value) >= self.qv or (not self.data_points or not self.data_points_r):
          self.data_points = [xn] # forget the rest
          self.data_points_r = [yn] # forget the rest

          # self.qv = min(xn.value, yn.value)
        elif self.qv >= xn.value:
          self.data_points = [xn]
          if yn.value >= xn.value:
            # 2: qv,yn,xn and yn,qv,xn
            self.data_points_r = [yn]
          else:
            # 1: qv,xn,yn
            process_y = True
          # self.qv = xn.value
        elif xn.value > self.qv >= yn.value:
          # 1: xn,qv,yn
          process_y = True
          process_x = True
          # self.qv = min(self.data_points[0].value, self.data_points_r[0].value) # only changes when a point expires

        else:
          Exception('This should not be possible.')


        dropped_x = self._process_ordered_list(self.data_points, xn, decreasing=False) if process_x else None
        dropped_y = self._process_ordered_list(self.data_points_r, yn, decreasing=True) if process_y else None
        left_nt = min(self.compute_nt(self.data_points, self.data_points_to_add, dropped_x), self.left_node.nt)
        right_nt = min(self.compute_nt(self.data_points_r, self.data_points_to_add_r, dropped_y), self.right_node.nt)
        self.nt = min(left_nt, right_nt)
        self.qv = min(self.data_points[0].value, self.data_points_r[0].value)
        return self.nt

      return self.nt



  def clean(self):
    self.data_points = []
    self.data_points_r = []
    self.data_points_to_add = []
    self.data_points_to_add_r = []
    if U.is_operand(self.op):
      return
    self.left_node.clean()
    if U.is_binary(self.op):
      self.right_node.clean()



  def to_formula(self):
    if self.op in U.MetricOperators:
      return 'x' + str(self.metric) + ' ' + self.op + ' ' + str(self.param)

    ls = self.left_node.to_formula()
    op_str = self.op
    if not U.is_boolean(self.op):
      if self.interval:
        op_str = op_str + ' ' + str(self.interval.lb) + ' ' + str(self.interval.ub)
      else:
          op_str = op_str + ' p' + self.op + ' p' + self.op

    if U.is_binary(self.op):
      rs = self.right_node.to_formula()
      return '( '  + ls + ' ) ' + op_str +  ' ( '  + rs + ' )'
    else:
      return op_str + ' ( ' + ls + ' )'


  def compute_along_signal(self, signal, time_points=None):
    """Compute the quantitative valuation along the signal. The naive and expensive approach is to call the compute at
    every point.
    """
    # - self.signal_length  for the project
    result = [0 for _ in range(len(signal))]
    for i in range(len(result)):
      if time_points:
        result[i] = self.compute(signal, i, time_points, time_points[i])
      else:
        result[i] = self.compute(signal, i, time_points)
    return result

  #MUTATION OPERATION USED IN GENETIC ALGORTIHMS

  def mutate(self, parameter_domains, metric_list, set_valued_metrics):
      node_to_mutate = self.random_node()[0]
      if node_to_mutate.op in U.BooleanOperators or random.random() < genetic_algorithm_constants.PROBABILITY_OF_MUTATION_OPERATION:
        node_to_mutate.operation_mutate()
      else:
        node_to_mutate.parameter_mutate(parameter_domains, metric_list, set_valued_metrics)
      return

  # TO FIND A RANDOM NODE IN TREE
  def random_node(self):
      tree_order = traverse_pre_order(self)
      random_node_route = random.choice(tree_order)
      route = list(random_node_route)
      node_to_return = self
      for path in route:
        if path == 'b':
          return node_to_return, route
        elif path == 'l':
          node_to_return = node_to_return.left_node
        elif path == 'r':
          node_to_return = node_to_return.right_node
      return (node_to_return, route)

  #RETURNS THE OPERATOR COUNT IN STL FORMULA
  def get_operator_count(self):
      count = 0
      formula = self.to_formula().split()
      for operator in U.STLPastOperators:
          count += formula.count(operator)
      for operator in U.BooleanOperators:
          count += formula.count(operator)
      return count

  #PARAMETRIC MUTATION IN GENETIC ALGORITHMS
  def parameter_mutate(self, parameter_domains, metric_list, set_valued_metrics):
      if self.op in U.MetricOperators:
        #if the metric is in the valued metrics set then it should mutated into a value in metric list
        parameter_domains_for_operator = parameter_domains.get('p' + str(self.metric))
        if str(self.metric) in set_valued_metrics :
          temp_list = list(parameter_domains_for_operator)
          if int(self.param) in temp_list:
            temp_list.remove(int(self.param))
          self.param = float(random.choice(temp_list))
        else :
          self.param = np.random.triangular(parameter_domains_for_operator[0], self.param,
                                            parameter_domains_for_operator[1])
      elif (not U.is_boolean(self.op)) and self.interval:
          parameter_domains_for_operator = parameter_domains.get('p' + str(self.op))
          self.interval.ub = int(np.random.triangular(parameter_domains_for_operator[0], self.interval.ub,
                                                      parameter_domains_for_operator[1]))
  #OPERATIONAL MUTATION IN GENETIC ALGORTIHMS
  def operation_mutate(self):
      if self.op == 'P':
          self.op = 'A'
      elif self.op == 'A':
          self.op = 'P'
      elif self.op == '&':
          self.op = '|'
      elif self.op == '|':
          self.op = '&'
      elif self.op == '>':
          self.op = '<'
      elif self.op == '<':
          self.op = '>'
      elif self.op == 'S':
          if random.random > 0.50:
              self.op = 'A'
              self.right_node = None
          else:
              self.op = 'P'
              self.left_node = self.right_node
              self.right_node = None
      return self

  def cross_over(self, to_cross, route):

    if route[0] == 'b':
      self.copy(to_cross)
      return
    elif route[0] == 'l':
      route.pop(0)
      self.left_node.cross_over(to_cross, route)
    elif route[0] == 'r':
      route.pop(0)
      self.right_node.cross_over(to_cross, route)

  def copy(self, to_cross):
    self.left_node = to_cross.left_node
    self.right_node =  to_cross.right_node
    self.op = to_cross.op
    self.metric = to_cross.metric
    self.interval = to_cross.interval
    self.signal_length = to_cross.signal_length
    self.set_valued = to_cross.set_valued
    self.data_points = to_cross.data_points
    self.data_points_to_add = to_cross.data_points_to_add
    self.data_points_r = to_cross.data_points_r
    self.data_points_to_add_r = to_cross.data_points_to_add_r
    self.qv = to_cross.qv
    self.nt = to_cross.nt
    self.param = to_cross.param

def _to_operand_stack(op, operand_stack):
  operand2 = operand_stack.pop()
  if U.is_binary(op[0]):
    operand1 = operand_stack.pop()
    operand_stack.append(op + ' ' + operand1 + ' ' + operand2)
  else:
    operand_stack.append(op + ' ' + operand2)


def infix_to_prefix(formula):
  """

  Args:
      formula: infix formula

  Returns: prefix formula

  """

  op_list = formula.split()

  op_stack = []
  operand_stack = []

  op_stack.append('(')
  op_list.append(')')
  output = []

  i = 0
  while i < len(op_list):
    if U.is_operand(op_list[i]):
      # x <> real
      operand_stack.append(op_list[i] + " " + op_list[i + 1] + " " + op_list[i + 2])
      i += 3
    elif op_list[i] == '(':
      op_stack.append(op_list[i])
      i += 1
    elif op_list[i] == ')':
      top_token = op_stack.pop()
      while top_token != '(':
        _to_operand_stack(top_token, operand_stack)
        top_token = op_stack.pop()
      i += 1
    else:  # it is an operator
      op = op_list[i]
      if op in U.STLOperators:
        op = op + ' ' + op_list[i + 1] + ' ' + op_list[i + 2]  # concat its bound
        i += 2
      i += 1
      while op_stack and U.PREC[op[0]] < U.PREC[op_stack[-1][0]]:
        op2 = op_stack.pop()
        _to_operand_stack(op2, operand_stack)

      op_stack.append(op)

  while op_stack:
    op = op_stack.pop()
    _to_operand_stack(op, operand_stack)

  return operand_stack[0]

def prefix_to_infix(formula):
  """

  Args:
      formula: prefix formula

  Returns: infix formula

  """

  stn = SyntaxTreeNode()
  stn.initialize_node(formula.split(), 0)

  return stn.to_formula()

def traverse_pre_order(stn, path = ''):
    stack = []
    if stn:
        stack.append(path + 'b')
        stack = stack + traverse_pre_order(stn.left_node, path + 'l')
        stack = stack + traverse_pre_order(stn.right_node, path + 'r')
    return stack