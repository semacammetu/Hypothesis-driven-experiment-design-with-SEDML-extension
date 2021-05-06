import unittest
import random
import STL
import formula_utilities as U


_data_points = [STL.DataPoint(0, [0]), STL.DataPoint(2, [1]), STL.DataPoint(4, [3]), STL.DataPoint(6, [8])]


class TestSTL(unittest.TestCase):

  def helper_get_stn(self, formula):
    stn = STL.SyntaxTreeNode()
    stn.initialize_node(formula.split(), 0)
    return stn


  def test_infix_to_prefix(self):

    self.assertEqual('F 0 10 x0 > 1', STL.infix_to_prefix('F 0 10 x0 > 1'))

    self.assertEqual(STL.infix_to_prefix('( F 0 10 x0 > 1 )'), 'F 0 10 x0 > 1')
    self.assertEqual(STL.infix_to_prefix('( F 0 10 ( x0 > 1 ) )'), 'F 0 10 x0 > 1')

    self.assertEqual(STL.infix_to_prefix('x0 > 1 U 0 12 x0 < 1'), 'U 0 12 x0 > 1 x0 < 1')

    self.assertEqual(STL.infix_to_prefix('x0 > 0 U 0 24 F 0 12 x0 < 12'), 'U 0 24 x0 > 0 F 0 12 x0 < 12')


  def test_to_formula(self):
    formula = 'F 0 10 x0 > 1.0'
    tokens = formula.split()
    stn = STL.SyntaxTreeNode()
    l = stn.initialize_node(tokens, 0)
    self.assertEqual(stn.to_formula(), 'F 0 10 ( x0 > 1.0 )')


  def test_syntax_tree_node_F(self):
    formula = 'F 0 10 x0 > 1'
    tokens = formula.split()
    stn = STL.SyntaxTreeNode()
    l = stn.initialize_node(tokens, 0)
    self.assertEqual(l, len(tokens))

    # root properties
    self.assertEqual(stn.op, 'F')
    self.assertEqual(stn.interval.ub, 10)
    self.assertEqual(stn.interval.lb, 0)

    # left tree properties:
    lt = stn.left_node
    self.assertEqual(lt.op, '>')
    self.assertEqual(lt.param, 1)


  def test_syntax_tree_node_U(self):
    formula = 'U 0 24 x0 > 0 F 0 12 x0 < 12'
    tokens = formula.split()
    stn = STL.SyntaxTreeNode()
    l = stn.initialize_node(tokens, 0)
    self.assertEqual(l, len(tokens))

    # root properties
    self.assertEqual(stn.op, 'U')
    self.assertEqual(stn.interval.ub, 24)
    self.assertEqual(stn.interval.lb, 0)

    # left tree properties:
    lt = stn.left_node
    self.assertEqual(lt.op, '>')
    self.assertEqual(lt.param, 0)

    rt = stn.right_node
    self.assertEqual(rt.op, 'F')
    self.assertEqual(rt.interval.ub, 12)
    self.assertEqual(rt.interval.lb, 0)
    lrt = rt.left_node
    self.assertEqual(lrt.op, '<')
    self.assertEqual(lrt.param, 12)


  def test_syntax_tree_node_Bool(self):
    formula = '& x0 > 11 F 0 12 x0 < 12'
    tokens = formula.split()
    stn = STL.SyntaxTreeNode()
    l = stn.initialize_node(tokens, 0)
    self.assertEqual(l, len(tokens))

    # root properties
    self.assertEqual(stn.op, '&')

    # left tree
    lt = stn.left_node
    self.assertEqual(lt.op, '>')
    self.assertEqual(lt.param, 11)

    # right tree
    rt = stn.right_node
    self.assertEqual(rt.op, 'F')
    self.assertEqual(rt.interval.ub, 12)
    self.assertEqual(rt.interval.lb, 0)
    lrt = rt.left_node
    self.assertEqual(lrt.op, '<')
    self.assertEqual(lrt.param, 12)


  def test_compute1(self):
    formula = 'x0 < 10'
    stn = self.helper_get_stn(formula)

    signal = [0]
    self.assertEqual(stn.compute([signal], 0), 10)

    signal = [12, 0]
    self.assertEqual(stn.compute([signal], 0), -2)

  def test_compute2(self):
    formula = 'F 0 2 x0 < 10'
    stn = self.helper_get_stn(formula)

    signal = [[3], [0], [9]]
    self.assertEqual(stn.compute(signal, 0), 10)

    signal = [[12], [1], [9], [2]]
    self.assertEqual(stn.compute(signal, 0), 9)


  def test_compute3(self):
    formula = 'G 0 2 x0 < 10'
    stn = self.helper_get_stn(formula)

    signal = [[3], [0], [9]]
    self.assertEqual(stn.compute(signal, 0), 1)

    signal = [[12], [1], [9], [2]]
    self.assertEqual(stn.compute(signal, 0), -2)


  def test_compute4(self):
    formula = '| G 0 2 x0 < 10 G 1 3 x0 > 3'
    stn = self.helper_get_stn(formula)

    signal = [[3], [0], [9], [5]]
    self.assertEqual(stn.compute(signal, 0), 1)

    signal = [[12], [8], [9], [2]]
    self.assertEqual(stn.compute(signal, 0), -1)

  def test_compute_length(self):
    formula = 'x0 < 10'
    stn = self.helper_get_stn(formula)

    self.assertEqual(0, stn.signal_length)

    formula = 'G 0 2 x0 < 10'
    stn = STL.SyntaxTreeNode()
    stn.initialize_node(formula.split(), 0)
    self.assertEqual(2, stn.signal_length)

    formula = '| G 0 2 x0 < 10 G 1 3 F 0 4 x0 > 3'
    stn = STL.SyntaxTreeNode()
    stn.initialize_node(formula.split(), 0)
    self.assertEqual(7, stn.signal_length)

  def test_compute_along_signal(self):
    formula = 'x0 < 10'
    stn = self.helper_get_stn(formula)

    self.assertEqual(stn.compute_along_signal([[0], [10], [12], [1]]), [10, 0, -2, 9])

  def test_compute_along_signal2(self):
    formula = 'F 0 2 x0 < 10'
    stn = self.helper_get_stn(formula)

    self.assertEqual(stn.compute_along_signal([[0], [10], [12], [1]]), [10, 9, 9, 9])


  def test_compute_along_signal3(self):
    formula = 'U 0 2 x0 > 5 x0 < 10'
    stn = self.helper_get_stn(formula)

    self.assertEqual(stn.compute_along_signal([[0], [10], [12], [1], [8]]), [10, 5, 7, 9, 2])


  def test_past_p(self):
    formula = 'P 0 2 x0 < 10'
    stn = self.helper_get_stn(formula)
    self.assertEqual(stn.compute([[9], [8], [7]], 2), 3)

    formula = 'P 1 2 x0 < 10'
    stn = self.helper_get_stn(formula)
    self.assertEqual(stn.compute([[9], [8], [7]], 2), 2)

    formula = 'P 2 2 x0 < 10'
    stn = self.helper_get_stn(formula)
    self.assertEqual(stn.compute([[9], [8], [7]], 2), 1)

    formula = 'P 3 4 x0 < 10'
    stn = self.helper_get_stn(formula)
    self.assertEqual(stn.compute([[9], [8], [7]], 2), U.MIN_VAL)


  def test_past_a(self):
    formula = 'A 0 2 x0 < 10'
    stn = self.helper_get_stn(formula)
    self.assertEqual(stn.compute([[9], [8], [7]], 2), 1)

    formula = 'A 0 1 x0 < 10'
    stn = self.helper_get_stn(formula)
    self.assertEqual(stn.compute([[9], [8], [7]], 2), 2)

    formula = 'A 0 0 x0 < 10'
    stn = self.helper_get_stn(formula)
    self.assertEqual(stn.compute([[9], [8], [7]], 2), 3)

    formula = 'A 3 4 x0 < 10'
    stn = self.helper_get_stn(formula)
    self.assertEqual(stn.compute([[9], [8], [7]], 2), U.MAX_VAL)

    formula = 'A 1 2 x0 < 10'
    stn = self.helper_get_stn(formula)
    self.assertEqual(stn.compute([[9], [8], [7], [6], [5]], 4), 3)

  def test_past_s(self):
    formula = 'S 0 2 x0 < 10 x0 > 5'
    stn = self.helper_get_stn(formula)
    self.assertEqual(stn.compute([[0], [0], [10]], 2), 0)


    formula = 'S 1 2 x0 < 10 x0 > 5'
    stn = self.helper_get_stn(formula)
    self.assertEqual(stn.compute([[0], [0], [10], [2]], 3), 0)

    formula = 'S 1 2 x0 < 10 x0 > 0'
    stn = self.helper_get_stn(formula)
    self.assertEqual(stn.compute([[5], [4], [3], [2]], 3), 4)


  # Tests for computation with time series:
  def test_past_p_time1(self):
    formula = 'P 0 4 x0 > 0'
    stn = self.helper_get_stn(formula)

    signal = [[12], [1], [-5], [0], [2]]
    time_points = [0, 2, 4, 6, 8]


    self.assertEqual(stn.compute(signal, 4, time_points, 8), 2)
    self.assertEqual(stn.compute(signal, 4, time_points, 7), 1)
    self.assertEqual(stn.compute(signal, 4, time_points, 6), 1)
    self.assertEqual(stn.compute(signal, 4, time_points, 5), 12)
    self.assertEqual(stn.compute(signal, 4, time_points, 3), 12)
    self.assertEqual(stn.compute(signal, 4, time_points, 9), 2)


  def test_past_a_time1(self):
    formula = 'A 0 4 x0 > 0'
    stn = self.helper_get_stn(formula)

    signal = [[-13], [-7], [-5], [0], [2]]
    time_points = [0, 2, 4, 6, 8]


    self.assertEqual(stn.compute(signal, 4, time_points, 8), -5)
    self.assertEqual(stn.compute(signal, 4, time_points, 7), -7)
    self.assertEqual(stn.compute(signal, 4, time_points, 6), -7)
    self.assertEqual(stn.compute(signal, 4, time_points, 5), -13)
    self.assertEqual(stn.compute(signal, 4, time_points, 3), -13)
    self.assertEqual(stn.compute(signal, 4, time_points, 9), -5)

  def test_past_s_time1(self):
    formula = 'S 0 4 x0 > 0 x0 < 10'
    stn = self.helper_get_stn(formula)

    signal = [[12], [2], [4], [11], [8]]
    time_points = [0, 2, 4, 6, 8]

    self.assertEqual(stn.compute(signal, 4, time_points, 8), 4)
    self.assertEqual(stn.compute(signal, 4, time_points, 7), 4)
    self.assertEqual(stn.compute(signal, 4, time_points, 6), 4)

    self.assertEqual(stn.compute(signal, 4, time_points, 5), 4)
    self.assertEqual(stn.compute(signal, 4, time_points, 4), 4)
    self.assertEqual(stn.compute(signal, 4, time_points, 3), 2)
    self.assertEqual(stn.compute(signal, 4, time_points, 1), -2)


  def test_past_s_time2(self):
    formula = '& P 0 3 x0 < 8 S 0 4 x0 > 0 x0 < 10'
    stn = self.helper_get_stn(formula)

    signal = [[12], [2], [4], [11], [8]]
    time_points = [0, 2, 4, 6, 8]

    self.assertEqual(stn.compute(signal, 4, time_points, 8), 4)
    self.assertEqual(stn.compute(signal, 4, time_points, 7), 4)
    self.assertEqual(stn.compute(signal, 4, time_points, 6), 4)

    self.assertEqual(stn.compute(signal, 4, time_points, 5), 4)
    self.assertEqual(stn.compute(signal, 4, time_points, 4), 4)
    self.assertEqual(stn.compute(signal, 4, time_points, 3), 2)
    self.assertEqual(stn.compute(signal, 4, time_points, 1), -4)

  def test_compute_qv_boolean_and(self):
    formula = '& x0 < 10 x0 > 3'
    stn = self.helper_get_stn(formula)

    results = [-3, -2, 0, 2]
    for i in range(4):
      self.assertEqual(stn.compute_qv(_data_points[i]), U.MAX_VAL)
      self.assertEqual(stn.qv, results[i])


  def test_compute_qv_boolean_or(self):
    formula = '| x0 < 10 x0 > 3'
    stn = self.helper_get_stn(formula)

    results = [10, 9, 7, 5]
    for i in range(4):
      self.assertEqual(stn.compute_qv(_data_points[i]), U.MAX_VAL)
      self.assertEqual(stn.qv, results[i])

  def test_compute_qv_boolean_not(self):
    formula = '! x0 < 10'
    stn = self.helper_get_stn(formula)

    results = [-10, -9, -7, -2]
    for i in range(4):
      self.assertEqual(stn.compute_qv(_data_points[i]), U.MAX_VAL)
      self.assertEqual(stn.qv, results[i])

  def test_compute_qv_previous(self):
    formula = 'P 0 3 x0 > 0'
    stn = self.helper_get_stn(formula)

    dp = STL.DataPoint(0, [2])
    dp_NL = STL.DataPoint(0, 2)
    self.assertEqual(stn.compute_qv(dp), U.MAX_VAL)
    self.assertEqual(stn.qv, 2)
    self.assertEqual(len(stn.data_points), 1)
    self.assertEqual(stn.data_points[0], dp_NL)
    self.assertEqual(stn.data_points_to_add, [])

    dp1 = STL.DataPoint(2, [4])
    dp1_NL = STL.DataPoint(2, 4)
    self.assertEqual(stn.compute_qv(dp1), U.MAX_VAL)
    self.assertEqual(stn.qv, 4)
    self.assertEqual(len(stn.data_points), 1)
    self.assertEqual(stn.data_points[0], dp1_NL)
    self.assertEqual(stn.data_points_to_add, [])

    dp2 = STL.DataPoint(4, [3])
    dp2_NL = STL.DataPoint(4, 3)
    self.assertEqual(stn.compute_qv(dp2), 7)
    self.assertEqual(stn.qv, 4)
    self.assertEqual(len(stn.data_points), 2)
    self.assertEqual(stn.data_points[0], dp1_NL)
    self.assertEqual(stn.data_points[1], dp2_NL)
    self.assertEqual(stn.data_points_to_add, [])

    dp3 = STL.DataPoint(5, [3])
    self.assertEqual(stn.compute_qv(dp3), 7)
    self.assertEqual(stn.qv, 4)
    self.assertEqual(len(stn.data_points), 2)
    self.assertEqual(stn.data_points[0], dp1_NL)
    self.assertEqual(stn.data_points[1], dp2_NL)
    self.assertEqual(stn.data_points_to_add, [])

    dp4 = STL.DataPoint(7, [3]) # artificial point
    self.assertEqual(stn.compute_qv(dp4), U.MAX_VAL)
    self.assertEqual(stn.qv, 3)
    self.assertEqual(len(stn.data_points), 1)
    self.assertEqual(stn.data_points[0], dp2_NL)
    self.assertEqual(stn.data_points_to_add, [])

    dp5 = STL.DataPoint(8, [2])
    dp5_NL = STL.DataPoint(8, 2)
    self.assertEqual(stn.compute_qv(dp5), 11)
    self.assertEqual(stn.qv, 3)
    self.assertEqual(len(stn.data_points), 2)
    self.assertEqual(stn.data_points[0], dp2_NL)
    self.assertEqual(stn.data_points[1], dp5_NL)
    self.assertEqual(stn.data_points_to_add, [])

    dp6 = STL.DataPoint(9, [1])
    dp6_NL = STL.DataPoint(9, 1)
    self.assertEqual(stn.compute_qv(dp6), 11)
    self.assertEqual(stn.qv, 3)
    self.assertEqual(len(stn.data_points), 3)
    self.assertEqual(stn.data_points[0], dp2_NL)
    self.assertEqual(stn.data_points[1], dp5_NL)
    self.assertEqual(stn.data_points[2], dp6_NL)
    self.assertEqual(stn.data_points_to_add, [])

    dp7 = STL.DataPoint(10, [0])
    dp7_NL = STL.DataPoint(10, 0)
    self.assertEqual(stn.compute_qv(dp7), 11)
    self.assertEqual(stn.qv, 3)
    self.assertEqual(len(stn.data_points), 4)
    self.assertEqual(stn.data_points[0], dp2_NL)
    self.assertEqual(stn.data_points[1], dp5_NL)
    self.assertEqual(stn.data_points[2], dp6_NL)
    self.assertEqual(stn.data_points[3], dp7_NL)

    dp8 = STL.DataPoint(11, [0])
    self.assertEqual(stn.compute_qv(dp8), 12)
    self.assertEqual(stn.qv, 2)
    self.assertEqual(len(stn.data_points), 3)
    self.assertEqual(stn.data_points[0], dp5_NL)
    self.assertEqual(stn.data_points[1], dp6_NL)
    self.assertEqual(stn.data_points[2], dp7_NL)

    dp9 = STL.DataPoint(12, [0])
    self.assertEqual(stn.compute_qv(dp9), 13)
    self.assertEqual(stn.qv, 1)
    self.assertEqual(len(stn.data_points), 2)
    self.assertEqual(stn.data_points[0], dp6_NL)
    self.assertEqual(stn.data_points[1], dp7_NL)

    dp10 = STL.DataPoint(13, [0])
    self.assertEqual(stn.compute_qv(dp10), U.MAX_VAL)
    self.assertEqual(stn.qv, 0)
    self.assertEqual(len(stn.data_points), 1)
    self.assertEqual(stn.data_points[0], dp7_NL)
    self.assertEqual(stn.data_points_to_add, [])

  def test_compute_qv_previous_with_lb(self):
    formula = 'P 1 3 x0 > 0'
    self._compute_qv_previous_with_lb(formula)

    formula = '! A 1 3 ! x0 > 0'
    self._compute_qv_previous_with_lb(formula, True)

  def _compute_qv_previous_with_lb(self, formula, first_boolean=False):
    # formula = 'P 1 3 p > 0'
    stn = self.helper_get_stn(formula)

    dp = STL.DataPoint(0, [2])
    dp_nl = STL.DataPoint(0, 2)
    self.assertEqual(stn.compute_qv(dp), 1)

    if not first_boolean:
      self.assertEqual(stn.qv, U.MIN_VAL)
      self.assertEqual(len(stn.data_points), 0)
      self.assertEqual(len(stn.data_points_to_add), 1)
      self.assertEqual(stn.data_points_to_add[0], dp_nl)

    dp_a = STL.DataPoint(1, [2])
    self.assertEqual(stn.compute_qv(dp_a), U.MAX_VAL)
    self.assertEqual(stn.qv, 2)
    if not first_boolean:
      self.assertEqual(len(stn.data_points), 1)
      self.assertEqual(stn.data_points[0], dp_nl)
      self.assertEqual(stn.data_points_to_add, [])

    dp1 = STL.DataPoint(2, [4])
    dp1_nl = STL.DataPoint(2, 4)
    self.assertEqual(stn.compute_qv(dp1), 3)
    self.assertEqual(stn.qv, 2)
    if not first_boolean:
      self.assertEqual(len(stn.data_points), 1)
      self.assertEqual(stn.data_points[0], dp_nl)
      self.assertEqual(len(stn.data_points_to_add), 1)
      self.assertEqual(stn.data_points_to_add[0], dp1_nl)

    # MOVE FROM TO_ADD to DATA_POINTS
    dp1_a = STL.DataPoint(3, [4])
    self.assertEqual(stn.compute_qv(dp1_a), U.MAX_VAL)
    self.assertEqual(stn.qv, 4)
    if not first_boolean:
      self.assertEqual(len(stn.data_points), 1)
      self.assertEqual(stn.data_points[0], dp1_nl)
      self.assertEqual(stn.data_points_to_add, [])


    dp2 = STL.DataPoint(4, [3])
    dp2_nl = STL.DataPoint(4, 3)
    self.assertEqual(stn.compute_qv(dp2), 5)
    self.assertEqual(stn.qv, 4)
    if not first_boolean:
      self.assertEqual(len(stn.data_points), 1)
      self.assertEqual(stn.data_points[0], dp1_nl)
      self.assertEqual(len(stn.data_points_to_add), 1)
      self.assertEqual(stn.data_points_to_add[0], dp2_nl)

    # MOVE FROM TO_ADD to DATA_POINTS
    dp2_a = STL.DataPoint(5, [3])
    self.assertEqual(stn.compute_qv(dp2_a), 7)
    self.assertEqual(stn.qv, 4)
    if not first_boolean:
      self.assertEqual(len(stn.data_points), 2)
      self.assertEqual(stn.data_points[0], dp1_nl)
      self.assertEqual(stn.data_points[1], dp2_nl)
      self.assertEqual(stn.data_points_to_add, [])

    dp4 = STL.DataPoint(7, [3]) # artificial point
    dp4_nl = STL.DataPoint(7, 3)
    self.assertEqual(stn.compute_qv(dp4), 8)
    self.assertEqual(stn.qv, 3)
    if not first_boolean:
      self.assertEqual(len(stn.data_points), 1)
      self.assertEqual(stn.data_points[0], dp2_nl)
      self.assertEqual(len(stn.data_points_to_add), 1)
      self.assertEqual(stn.data_points_to_add[0], dp4_nl)

    dp5 = STL.DataPoint(8, [2])
    dp5_nl = STL.DataPoint(8, 2)
    self.assertEqual(stn.compute_qv(dp5), 9)
    self.assertEqual(stn.qv, 3)
    if not first_boolean:
      self.assertEqual(len(stn.data_points), 1)
      self.assertEqual(stn.data_points[0], dp2_nl)
      self.assertEqual(len(stn.data_points_to_add), 1)
      self.assertEqual(stn.data_points_to_add[0], dp5_nl)


    dp6 = STL.DataPoint(9, [1])
    dp6_nl = STL.DataPoint(9, 1)
    self.assertEqual(stn.compute_qv(dp6), 10)
    self.assertEqual(stn.qv, 3)
    if not first_boolean:
      self.assertEqual(len(stn.data_points), 2)
      self.assertEqual(stn.data_points[0], dp2_nl)
      self.assertEqual(stn.data_points[1], dp5_nl)
      self.assertEqual(len(stn.data_points_to_add), 1)
      self.assertEqual(stn.data_points_to_add[0], dp6_nl)

    dp7 = STL.DataPoint(10, [0])
    dp7_nl = STL.DataPoint(10, 0)
    self.assertEqual(stn.compute_qv(dp7), 11)
    self.assertEqual(stn.qv, 3)
    if not first_boolean:
      self.assertEqual(len(stn.data_points), 3)
      self.assertEqual(stn.data_points[0], dp2_nl)
      self.assertEqual(stn.data_points[1], dp5_nl)
      self.assertEqual(stn.data_points[2], dp6_nl)
      self.assertEqual(len(stn.data_points_to_add), 1)
      self.assertEqual(stn.data_points_to_add[0], dp7_nl)

    dp8 = STL.DataPoint(11, [0])
    self.assertEqual(stn.compute_qv(dp8), 12)
    self.assertEqual(stn.qv, 2)
    if not first_boolean:
      self.assertEqual(len(stn.data_points), 3)
      self.assertEqual(stn.data_points[0], dp5_nl)
      self.assertEqual(stn.data_points[1], dp6_nl)
      self.assertEqual(stn.data_points[2], dp7_nl)
      self.assertEqual(len(stn.data_points_to_add), 0)

    dp9 = STL.DataPoint(12, [0])
    self.assertEqual(stn.compute_qv(dp9), 13)
    self.assertEqual(stn.qv, 1)
    if not first_boolean:
      self.assertEqual(len(stn.data_points), 2)
      self.assertEqual(stn.data_points[0], dp6_nl)
      self.assertEqual(stn.data_points[1], dp7_nl)
      self.assertEqual(len(stn.data_points_to_add), 1)

    dp10 = STL.DataPoint(13, [0])
    self.assertEqual(stn.compute_qv(dp10), U.MAX_VAL)
    self.assertEqual(stn.qv, 0)
    if not first_boolean:
      self.assertEqual(len(stn.data_points), 1)
      self.assertEqual(stn.data_points[0], dp7_nl)
      self.assertEqual(stn.data_points_to_add, [])


  def test_compute_qv_always(self):
    formula = 'A 0 3 x0 > 0'
    self._compute_qv_always_A_0_3(formula)

    formula_with_P = '! P 0 3 ! x0 > 0'
    self._compute_qv_always_A_0_3(formula_with_P, True)

  def _compute_qv_always_A_0_3(self, formula, first_boolean=False):
    # formula = 'A 0 3 p > 0'
    stn = self.helper_get_stn(formula)

    dp = STL.DataPoint(0, [2])
    dp_NL = STL.DataPoint(0, 2)
    self.assertEqual(stn.compute_qv(dp), U.MAX_VAL)
    self.assertEqual(stn.qv, 2)
    if not first_boolean: # remember nothing if the root is boolean
      self.assertEqual(len(stn.data_points), 1)
      self.assertEqual(stn.data_points[0], dp_NL) # in STN data points, the values are 1 dimensional
    self.assertEqual(stn.data_points_to_add, [])

    dp1 = STL.DataPoint(2, [4])
    dp1_NL = STL.DataPoint(2, 4)
    self.assertEqual(stn.compute_qv(dp1), 5)
    self.assertEqual(stn.qv, 2)
    if not first_boolean:
      self.assertEqual(len(stn.data_points), 2)
      self.assertEqual(stn.data_points[0], dp_NL)
      self.assertEqual(stn.data_points[1], dp1_NL)
    self.assertEqual(stn.data_points_to_add, [])


    dp2 = STL.DataPoint(4, [3])
    self.assertEqual(stn.compute_qv(dp2), 5)
    self.assertEqual(stn.qv, 2)
    if not first_boolean:
      self.assertEqual(len(stn.data_points), 2)
      self.assertEqual(stn.data_points[0], dp_NL)
      self.assertEqual(stn.data_points[1], STL.DataPoint(2, 3))
    self.assertEqual(stn.data_points_to_add, [])

    dp3 = STL.DataPoint(5, [3])
    self.assertEqual(stn.compute_qv(dp3), U.MAX_VAL)
    self.assertEqual(stn.qv, 3)
    if not first_boolean:
      self.assertEqual(len(stn.data_points), 1)
      self.assertEqual(stn.data_points[0], STL.DataPoint(2, 3))
    self.assertEqual(stn.data_points_to_add, [])

    dp5 = STL.DataPoint(8, [2])
    dp5_NL = STL.DataPoint(8, 2)
    self.assertEqual(stn.compute_qv(dp5), U.MAX_VAL)
    self.assertEqual(stn.qv, 2)
    if not first_boolean:
      self.assertEqual(len(stn.data_points), 1)
      self.assertEqual(stn.data_points[0], dp5_NL)
    self.assertEqual(stn.data_points_to_add, [])
    #
    dp6 = STL.DataPoint(9, [1])
    dp6_NL = STL.DataPoint(9, 1)
    self.assertEqual(stn.compute_qv(dp6), U.MAX_VAL)
    self.assertEqual(stn.qv, 1)
    if not first_boolean:
      self.assertEqual(len(stn.data_points), 1)
      self.assertEqual(stn.data_points[0], dp6_NL)
    self.assertEqual(stn.data_points_to_add, [])
    #
    dp7 = STL.DataPoint(10, [0])
    dp7_NL = STL.DataPoint(10, 0)
    self.assertEqual(stn.compute_qv(dp7), U.MAX_VAL)
    self.assertEqual(stn.qv, 0)
    if not first_boolean:
      self.assertEqual(len(stn.data_points), 1)
      self.assertEqual(stn.data_points[0], dp7_NL)

    dp8 = STL.DataPoint(11, [1])
    dp8_NL = STL.DataPoint(11, 1)
    self.assertEqual(stn.compute_qv(dp8), 14)
    self.assertEqual(stn.qv, 0)
    if not first_boolean:
      self.assertEqual(len(stn.data_points),2)
      self.assertEqual(stn.data_points[0], dp7_NL)
      self.assertEqual(stn.data_points[1], dp8_NL)

    dp9 = STL.DataPoint(12, [2])
    dp9_NL = STL.DataPoint(12, 2)
    self.assertEqual(stn.compute_qv(dp9), 14)
    self.assertEqual(stn.qv, 0)
    if not first_boolean:
      self.assertEqual(len(stn.data_points),3)
      self.assertEqual(stn.data_points[0], dp7_NL)
      self.assertEqual(stn.data_points[1], dp8_NL)
      self.assertEqual(stn.data_points[2], dp9_NL)


    dp10 = STL.DataPoint(13, [3])
    dp10_NL = STL.DataPoint(13, 3)
    self.assertEqual(stn.compute_qv(dp10), 14)
    self.assertEqual(stn.qv, 0)
    if not first_boolean:
      self.assertEqual(len(stn.data_points),4)
      self.assertEqual(stn.data_points[0], dp7_NL)
      self.assertEqual(stn.data_points[1], dp8_NL)
      self.assertEqual(stn.data_points[2], dp9_NL)
      self.assertEqual(stn.data_points[3], dp10_NL)

    dp11 = STL.DataPoint(14, [3])
    self.assertEqual(stn.compute_qv(dp11), 15)
    self.assertEqual(stn.qv, 1)
    if not first_boolean:
      self.assertEqual(len(stn.data_points), 3)
      self.assertEqual(stn.data_points[0], dp8_NL)
      self.assertEqual(stn.data_points[1], dp9_NL)
      self.assertEqual(stn.data_points[2], dp10_NL)

    dp12 = STL.DataPoint(15, [3])
    self.assertEqual(stn.compute_qv(dp12), 16)
    self.assertEqual(stn.qv, 2)
    if not first_boolean:
      self.assertEqual(len(stn.data_points), 2)
      self.assertEqual(stn.data_points[0], dp9_NL)
      self.assertEqual(stn.data_points[1], dp10_NL)

    dp13 = STL.DataPoint(16, [3])
    self.assertEqual(stn.compute_qv(dp13), U.MAX_VAL)
    self.assertEqual(stn.qv, 3)
    if not first_boolean:
      self.assertEqual(len(stn.data_points), 1)
      self.assertEqual(stn.data_points[0], dp10_NL)


  def test_compute_qv_since_0_3(self):
    formula = 'S 0 3 x0 > 0 x0 < 10'
    stn = self.helper_get_stn(formula)

    dp1 = STL.DataPoint(0, [12])
    self.assertEqual(stn.compute_qv(dp1), U.MAX_VAL)
    self.assertEqual(stn.qv, -2) # CASE 1

    dp2 = STL.DataPoint(2, [8]) # CASE 1 again, xn=8, yn= 2, qv=-2
    dp2_nl = STL.DataPoint(2, 8)
    self.assertEqual(stn.compute_qv(dp2), U.MAX_VAL)
    self.assertEqual(stn.qv, 2)
    self.assertListEqual(stn.data_points, [dp2_nl])
    self.assertListEqual(stn.data_points_r, [STL.DataPoint(time=2, value=2)])

    dp3 = STL.DataPoint(4, [1]) # CASE 2, xn=1, yn=9, qv=2  --> yn > qv > xn (II-6)
    dp3_nl = STL.DataPoint(4, 1)
    self.assertEqual(stn.compute_qv(dp3), U.MAX_VAL)
    self.assertEqual(stn.qv, 1)
    self.assertListEqual(stn.data_points, [dp3_nl])
    self.assertListEqual(stn.data_points_r, [STL.DataPoint(time=4, value=9)])

    dp4 = STL.DataPoint(6, [10]) # CASE 3, xn=10, yn=0, qv=1 --> xn > qv > yn
    dp4_nl = STL.DataPoint(6, 10)
    self.assertEqual(stn.compute_qv(dp4), 9) # dp3 will expire at 9
    self.assertEqual(stn.qv, 1)
    self.assertListEqual(stn.data_points, [dp3_nl, dp4_nl])
    self.assertListEqual(stn.data_points_r, [STL.DataPoint(time=4, value=9),
                                             STL.DataPoint(time=6, value=0)])

    # dp3 will expire now:
    dp5 = STL.DataPoint(9, [10])
    self.assertEqual(stn.compute_qv(dp5), U.MAX_VAL)
    self.assertEqual(stn.qv, 0)
    self.assertListEqual(stn.data_points, [dp4_nl])
    self.assertListEqual(stn.data_points_r, [STL.DataPoint(time=6, value=0)])

  def test_binary_1(self):
    formula = 'b0 = 10'
    stn = self.helper_get_stn(formula)
    dp1 = STL.DataPoint(0, [12])
    self.assertEqual(stn.compute_qv(dp1), U.MAX_VAL)
    self.assertEqual(stn.qv, -STL.BINARY_MAX)

    dp2 = STL.DataPoint(0, [10])
    self.assertEqual(stn.compute_qv(dp2), U.MAX_VAL)
    self.assertEqual(stn.qv, STL.BINARY_MAX)

  def test_randomized_p(self):
    formula = 'P 0 3 x0 > 7'
    file_name = 'tmp_test'
    self.randomized_t(formula, file_name, read=False, trace_length=160)

  def test_randomized_p_b(self):
    formula = 'P 2 4 x0 > 8'
    file_name = 'tmp_test'
    self.randomized_t(formula, file_name, read=False, trace_length=100)

  def test_randomized_since(self):
    formula = 'S 0 6 x0 > 6 x0 < 3'
    file_name = 'tmp_test'
    self.randomized_t(formula, file_name, read=False, trace_length=100)


  def test_randomized_nested1(self):
    formula = 'P 0 4 x0 < 5 S 0 3 A 1 2 x0 > 2'
    formula = STL.infix_to_prefix(formula)
    self.randomized_t(formula, 'tmp_test', read=False, trace_length=100)


  def test_randomized_always(self):
    formula = 'A 2 4 x0 > 0'
    self.randomized_t(formula, 'tmp_test', read=False, trace_length=100)

  def test_always(self):

    formula = 'A 1 2 x0 > 2'
    self.randomized_t(formula, 'tmp_test', read=False, trace_length=100)

    formula = 'A 1 1 x0 > 2'
    self.randomized_t(formula, 'tmp_test', read=False, trace_length=100)


  def test_p(self):
    formula = 'P 0 4 x0 < 5'
    self.randomized_t(formula, 'tmp_test', read=False, trace_length=100)


  def test_nested(self):
    formula = '! x0 > 6 | ( P 0 6 A 0 4 x0 < 4 )'
    formula = STL.infix_to_prefix(formula)
    self.randomized_t(formula, 'tmp_test', read=False, trace_length=100)



  def randomized_t(self, formula, file_name, read=False, trace_length=20):

    # return
    # Either read from a file or generate randomly, always length 100, within range 0-10
    time_values = list(range(trace_length))
    data_values = []
    # Read the traces from a file
    if read:
      f = open(file_name, 'r')
      for line in f:
        data_values.append(int(line))
      f.close()
    else:
      # Store them
      f = open(file_name, 'w')
      for _ in range(trace_length):
        x = random.randint(0,10)
        data_values.append(x)
        f.write(str(x) + '\n')
      f.close()



    # Generate the STN
    stn = self.helper_get_stn(formula)
    # Call compute
    result = stn.compute_along_signal([data_values], time_values)

    # efficient computation and result:
    e_result = []
    for t, v in zip(time_values, data_values):
      dp = STL.DataPoint(t, [v])
      stn.compute_qv(dp)
      e_result.append(stn.qv)

    if read:
      print(formula)
      print(result)
      print(e_result)
    self.assertListEqual(result[stn.signal_length:], e_result[stn.signal_length:len(result)])


  def test_traversal(self):
    formula = '& x5 = 0 A 0 1 x3 > 15'
    stn = STL.SyntaxTreeNode()
    stn.initialize_node(formula.split(), 0)
    result = STL.traverse_pre_order(stn)
    expected = ['b', 'rb', 'lb',  'rlb']
    self.assertListEqual(sorted(result), sorted(expected))

if __name__ == '__main__':
  unittest.main()

