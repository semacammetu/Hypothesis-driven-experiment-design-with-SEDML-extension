import unittest
import random
from trace_checker import STL
from trace_checker import formula_utilities as U
import syntactically_cosafe_form as scf


_data_points = [STL.DataPoint(0, [0]), STL.DataPoint(2, [1]), STL.DataPoint(4, [3]), STL.DataPoint(6, [8])]


class Test_syntactically_cosafe_form(unittest.TestCase):


  def test_scf(self):
      formula = 'P 1 1 ( x0 = 1 )'
      formula_X0, dict0 = 'X p0', {'x0=1.0': 'p0'}
      sc_formula = scf.return_sc_form(formula, prefix=False)
      formula_X, dict = scf.turn_inequalities_to_atomic_propositions(sc_formula)
      self.assertEqual(formula_X, formula_X0)
      self.assertEqual(dict, dict0)

      formula = 'P 1 2 ( x0 = 1 )'
      formula_X0, dict0 = '( X p0 | XX p0 )', {'x0=1.0': 'p0'}
      sc_formula = scf.return_sc_form(formula, prefix=False)
      formula_X, dict = scf.turn_inequalities_to_atomic_propositions(sc_formula)
      self.assertEqual(formula_X, formula_X0)
      self.assertEqual(dict, dict0)

      formula = 'A 1 1 ( x0 = 1 )'
      formula_X0, dict0 = 'X p0', {'x0=1.0': 'p0'}
      sc_formula = scf.return_sc_form(formula, prefix=False)
      formula_X, dict = scf.turn_inequalities_to_atomic_propositions(sc_formula)
      self.assertEqual(formula_X, formula_X0)
      self.assertEqual(dict, dict0)

      formula = 'A 1 2 ( x0 = 1 )'
      formula_X0, dict0 = '( X p0 & XX p0 )', {'x0=1.0': 'p0'}
      sc_formula = scf.return_sc_form(formula, prefix=False)
      formula_X, dict = scf.turn_inequalities_to_atomic_propositions(sc_formula)
      self.assertEqual(formula_X, formula_X0)
      self.assertEqual(dict, dict0)

      formula = 'P 0 0 ( x0 = 1 )'
      formula_X0, dict0 = 'p0', {'x0=1.0': 'p0'}
      sc_formula = scf.return_sc_form(formula, prefix=False)
      formula_X, dict = scf.turn_inequalities_to_atomic_propositions(sc_formula)
      self.assertEqual(formula_X, formula_X0)
      self.assertEqual(dict, dict0)

      formula = 'A 0 0 ( x0 = 1 )'
      formula_X0, dict0 = 'p0', {'x0=1.0': 'p0'}
      sc_formula = scf.return_sc_form(formula, prefix=False)
      formula_X, dict = scf.turn_inequalities_to_atomic_propositions(sc_formula)
      self.assertEqual(formula_X, formula_X0)
      self.assertEqual(dict, dict0)

      formula = '( P 1 2 ( ( ( A 1 1 ( ( x0 = 1 ) ) ) ) ) ) '
      formula_X0, dict0 = '( XX p0 | XXX p0 )', {'x0=1.0': 'p0'}
      sc_formula = scf.return_sc_form(formula, prefix=False)
      formula_X, dict = scf.turn_inequalities_to_atomic_propositions(sc_formula)
      self.assertEqual(formula_X, formula_X0)
      self.assertEqual(dict, dict0)

      formula = '( P 1 2 ( ( ( A 1 3 ( ( x0 = 1 ) ) ) ) ) ) '
      formula_X0, dict0 = '( X ( X p0 & XX p0 & XXX p0 ) | XX ( X p0 & XX p0 & XXX p0 ) )', {'x0=1.0': 'p0'}
      sc_formula = scf.return_sc_form(formula, prefix=False)
      formula_X, dict = scf.turn_inequalities_to_atomic_propositions(sc_formula)
      self.assertEqual(formula_X, formula_X0)
      self.assertEqual(dict, dict0)

      formula = '! ( x0 = 1.0 )'
      formula_X0, dict0 = '! p0', {'x0=1.0': 'p0'}
      sc_formula = scf.return_sc_form(formula, prefix=False)
      formula_X, dict = scf.turn_inequalities_to_atomic_propositions(sc_formula)
      self.assertEqual(formula_X, formula_X0)
      self.assertEqual(dict, dict0)

      formula = ' ( ( x0 = 1 ) )'
      formula_X0, dict0 = 'p0', {'x0=1.0': 'p0'}
      sc_formula = scf.return_sc_form(formula, prefix=False)
      formula_X, dict = scf.turn_inequalities_to_atomic_propositions(sc_formula)
      self.assertEqual(formula_X, formula_X0)
      self.assertEqual(dict, dict0)

      formula = '! ( P 1 1 ( x0 = 1 ) )'
      formula_X0, dict0 = '! X p0', {'x0=1.0': 'p0'}
      sc_formula = scf.return_sc_form(formula, prefix=False)
      formula_X, dict = scf.turn_inequalities_to_atomic_propositions(sc_formula)
      self.assertEqual(formula_X, formula_X0)
      self.assertEqual(dict, dict0)


      formula = 'P 1 1 ( x0 = 1 ) & A 1 2 ( x1 < 3 )'
      formula_X0, dict0 = '( X p0 & ( X p1 & XX p1 ) )', {'x0=1.0': 'p0', 'x1<3.0': 'p1'}
      sc_formula = scf.return_sc_form(formula, prefix=False)
      formula_X, dict = scf.turn_inequalities_to_atomic_propositions(sc_formula)
      self.assertEqual(formula_X, formula_X0)
      self.assertEqual(dict, dict0)

      formula = 'P 1 2 ( x0 = 1 ) & A 1 2 ( x1 < 3 )'
      formula_X0, dict0 = '( ( X p0 | XX p0 ) & ( X p1 & XX p1 ) )', {'x0=1.0': 'p0', 'x1<3.0': 'p1'}
      sc_formula = scf.return_sc_form(formula, prefix=False)
      formula_X, dict = scf.turn_inequalities_to_atomic_propositions(sc_formula)
      self.assertEqual(formula_X, formula_X0)
      self.assertEqual(dict, dict0)

      formula = ' ! ( ( ( ( P 1 2 ( x0 = 1 ) & A 1 2 ( ( x1 < 3 ) ) ) ) ) )'
      formula_X0, dict0 = '! ( ( X p0 | XX p0 ) & ( X p1 & XX p1 ) )', {'x0=1.0': 'p0', 'x1<3.0': 'p1'}
      sc_formula = scf.return_sc_form(formula, prefix=False)
      formula_X, dict = scf.turn_inequalities_to_atomic_propositions(sc_formula)
      self.assertEqual(formula_X, formula_X0)
      self.assertEqual(dict, dict0)

if __name__ == '__main__':
  unittest.main()