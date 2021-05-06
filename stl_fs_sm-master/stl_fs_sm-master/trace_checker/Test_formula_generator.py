import unittest
import formula_generator as fg
import formula_utilities as U


class MyTestCase(unittest.TestCase):

  def test_generate_formula_tree_op0(self):

    tree_list = fg.generate_formula_tree('0', 0, True)
    expected_formula_list = ['x0 < p0', 'x0 > p0']
    self.assertSetEqual(set(expected_formula_list), set(tree_list))


    tree_list = fg.generate_formula_tree(['0'], 0, True, ['0'])
    expected_formula_list = ['x0 = p0']
    self.assertSetEqual(set(expected_formula_list), set(tree_list))

    
  def test_generate_formula_tree_op1(self):
    tree_list = fg.generate_formula_tree([0], 1, True)
    expected_formula_list = ['! ( x0 < p0 )', '! ( x0 > p0 )',
                             '( x0 < p0 ) & ( x0 < p0 )', '( x0 < p0 ) & ( x0 > p0 )',
                             '( x0 > p0 ) & ( x0 < p0 )', '( x0 > p0 ) & ( x0 > p0 )',
                             '( x0 < p0 ) | ( x0 < p0 )', '( x0 < p0 ) | ( x0 > p0 )',
                             '( x0 > p0 ) | ( x0 < p0 )', '( x0 > p0 ) | ( x0 > p0 )',
                             'P pP pP ( x0 < p0 )', 'P pP pP ( x0 > p0 )',
                             'A pA pA ( x0 < p0 )', 'A pA pA ( x0 > p0 )',
                             '( x0 < p0 ) S pS pS ( x0 < p0 )', '( x0 < p0 ) S pS pS ( x0 > p0 )',
                             '( x0 > p0 ) S pS pS ( x0 < p0 )', '( x0 > p0 ) S pS pS ( x0 > p0 )']
    self.assertSetEqual(set(expected_formula_list), set(tree_list))


  def test_generate_formula_tree_op2(self):
    tree_list = fg.generate_formula_tree('0', 2, False)
    count_with_0_operator = 2
    count_with_1_operator = 18
    count_with_2_root_binary_operator = 3*2*count_with_0_operator*count_with_1_operator
    count_with_2_root_unary_operator = 3*count_with_1_operator

    expected_formula_count = count_with_2_root_binary_operator + count_with_2_root_unary_operator
    self.assertEqual(len(tree_list), expected_formula_count)

    # A few scheck:
    formulas = set([ "".join(tree.to_formula().split())  for tree in tree_list])

    self.assertIn("".join('A pA pA ( P pP pP (x0 < p0) )'.split()), formulas)


  def test_generate_formula_tree_iterative_op0(self):
    tree_list_recur = fg.generate_formula_tree([0], 0, True)
    tree_list_iter = fg.generate_formula_tree_iterative([0], 0, True,[],False)

    self.assertSetEqual(set(tree_list_recur), set(tree_list_iter))


  def test_generate_formula_tree_iterative_op1(self):
    tree_list_recur = fg.generate_formula_tree([0], 1, True)
    tree_list_iter = fg.generate_formula_tree_iterative([0], 1, True,[],False)

    self.assertSetEqual(set(tree_list_recur), set(tree_list_iter))


  def test_generate_formula_tree_iterative_op2(self):
    tree_list_recur = fg.generate_formula_tree([0], 2, True)
    tree_list_iter = fg.generate_formula_tree_iterative([0], 2, True,[],False)

    self.assertSetEqual(set(tree_list_recur), set(tree_list_iter))


  def test_generate_formula_tree_iterative_param2(self):
    tree_list_recur = fg.generate_formula_tree([0,1], 2, True)
    tree_list_iter = fg.generate_formula_tree_iterative([0,1], 2, True, [],False)

    self.assertSetEqual(set(tree_list_recur), set(tree_list_iter))


  def test_generate_formula_tree_iterative_setValued(self):
    tree_list_recur = fg.generate_formula_tree([0,1], 2, True, [0])
    tree_list_iter = fg.generate_formula_tree_iterative([0,1], 2, True,[0],False)

    self.assertSetEqual(set(tree_list_recur), set(tree_list_iter))


  def test_generate_formula_tree_strict_equal_formulas(self):
    test_formula1 = '( x0 < p0 ) & ( x0 < p0 )'
    formula_list_original = fg.generate_formula_tree_iterative([0],1,True,[],False) 
    formula_list_simplified = fg.generate_formula_tree_iterative([0], 1, True)
    
    self.assertIn(test_formula1, formula_list_original)
    self.assertNotIn(test_formula1, formula_list_simplified)

    formula_list_original = fg.generate_formula_tree_iterative([0],3,True,[],False) 
    formula_list_simplified = fg.generate_formula_tree_iterative([0], 3, True)
    test_formula2 = '( A pA pA ( x0 < p0 ) ) & ( A pA pA ( x0 < p0 ) )'

    self.assertIn(test_formula2, formula_list_original)
    self.assertNotIn(test_formula2, formula_list_simplified)


  def test_generate_formula_tree_associativity(self):
    test_formula1 = '( x0 > p0 ) & ( ( x0 > p0 ) & ( x0 < p0 ) )' # p & (p & q)
    formula_list_original = fg.generate_formula_tree_iterative([0],2,True,[],False) 
    formula_list_simplified = fg.generate_formula_tree_iterative([0], 2, True)

    self.assertIn(test_formula1, formula_list_original)
    self.assertNotIn(test_formula1, formula_list_simplified)

    formula_list_original = fg.generate_formula_tree_iterative([0],3,True,[],False) 
    formula_list_simplified = fg.generate_formula_tree_iterative([0], 3, True)
    test_formula2 = '( x0 < p0 ) | ( ( P pP pP ( x0 > p0 ) ) | ( x0 > p0 ) )'

    self.assertIn(test_formula2, formula_list_original)
    self.assertNotIn(test_formula2, formula_list_simplified)


  def test_generate_formula_tree_absorption(self):
    test_formula1 = '( x0 > p0 ) & ( ( x0 > p0 ) | ( x0 < p0 ) )' # p & (p | q)
    formula_list_original = fg.generate_formula_tree_iterative([0],2,True,[],False) 
    formula_list_simplified = fg.generate_formula_tree_iterative([0], 2, True)

    self.assertIn(test_formula1, formula_list_original)
    self.assertNotIn(test_formula1, formula_list_simplified)

    test_formula2 = '( x0 < p0 ) | ( ( x0 < p0 ) & ( P pP pP ( x0 > p0 ) ) )' # p | (p & q)
    formula_list_original = fg.generate_formula_tree_iterative([0],3,True,[],False) 
    formula_list_simplified = fg.generate_formula_tree_iterative([0], 3, True)

    self.assertIn(test_formula2, formula_list_original)
    self.assertNotIn(test_formula2, formula_list_simplified)


  def test_generate_formula_tree_distrubitivity(self):
    test_formula = '( ( x0 > p0 ) | ( x0 < p0 ) ) & ( ( P pP pP ( x0 > p0 ) ) | ( x0 > p0 ) )' # (p | q) & (r | p)
    formula_list_original = fg.generate_formula_tree_iterative([0],4,True,[],False) 
    formula_list_simplified = fg.generate_formula_tree_iterative([0], 4, True)

    self.assertIn(test_formula, formula_list_original)
    self.assertNotIn(test_formula, formula_list_simplified)


  def test_generate_formula_tree_negation_op(self):
    
    test_formula1 = '! ( x0 > p0 )' #roughly equivalent to  "x0 < p0" for our purposes
    formula_list_original = fg.generate_formula_tree_iterative([0],1,True,[],False) 
    formula_list_simplified = fg.generate_formula_tree_iterative([0], 1, True)

    self.assertIn(test_formula1, formula_list_original)
    self.assertNotIn(test_formula1, formula_list_simplified)

    test_formula2 = '! ( P pP pP ( x0 > p0 ) )' #roughly equivalent to  "A 0 pA(x0 < p0) "
    formula_list_original = fg.generate_formula_tree_iterative([0],2,True,[],False) 
    formula_list_simplified = fg.generate_formula_tree_iterative([0], 2, True)

    self.assertIn(test_formula2, formula_list_original)
    self.assertNotIn(test_formula2, formula_list_simplified)


  def test_generate_formula_tree_repeated_unary_operators(self):
    
    test_formula = 'P pP pP ( P pP pP ( x0 > p0 ) )'
    formula_list_original = fg.generate_formula_tree_iterative([0],2,True,[],False) 
    formula_list_simplified = fg.generate_formula_tree_iterative([0], 2, True)

    self.assertIn(test_formula, formula_list_original)
    self.assertNotIn(test_formula, formula_list_simplified)

if __name__ == '__main__':
  unittest.main()
