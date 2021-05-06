import collections
import sys
from collections import namedtuple

# MIN-MAX CONSTANTS
MAX_EVAL = sys.maxsize
MIN_EVAL = 0

#CATEGORY CONSTANTS
CATEGORY_MAXIMIZATION = 0
CATEGORY_MINIMIZATION = 1

#TYPE CONSTANTS
TYPE_RATIO = 0
TYPE_MISMATCH = 1
TYPE_FALSE_POSITIVE_FALSE_NEGATIVE = 2
TYPE_F1_SCORE = 3
TYPE_FHALF_SCORE = 4
TYPE_PRECISION = 5
TYPE_RECALL = 6
TYPE_F_015_SCORE = 7
TYPE_F_02_SCORE = 8
TYPE_F_03_SCORE = 9
TYPE_F_04_SCORE = 10

#Name of the named tuple must be the same with name attribute(ReturnType)
ReturnType = collections.namedtuple('ReturnType', 'name, category, type')

FormulaValuation = namedtuple('FormulaValuation', ['formula', 'valuation'])


__MISMATCH = ReturnType(name='mismatch', category=CATEGORY_MINIMIZATION, type =TYPE_MISMATCH)
__RATIO = ReturnType(name='ratio', category=CATEGORY_MINIMIZATION, type=TYPE_RATIO)
__DETAILED = ReturnType(name='detailed', category=CATEGORY_MINIMIZATION, type=TYPE_FALSE_POSITIVE_FALSE_NEGATIVE)
__F1_SCORE = ReturnType(name='f1_score', category=CATEGORY_MAXIMIZATION, type=TYPE_F1_SCORE)
__F_015_SCORE = ReturnType(name='f015_score', category=CATEGORY_MAXIMIZATION, type=TYPE_F_015_SCORE)
__F_02_SCORE = ReturnType(name='f02_score', category=CATEGORY_MAXIMIZATION, type=TYPE_F_02_SCORE)
__F_03_SCORE = ReturnType(name='f03_score', category=CATEGORY_MAXIMIZATION, type=TYPE_F_03_SCORE)
__F_04_SCORE = ReturnType(name='f04_score', category=CATEGORY_MAXIMIZATION, type=TYPE_F_04_SCORE)
__FHALF_SCORE = ReturnType(name='fhalf_score', category=CATEGORY_MAXIMIZATION, type=TYPE_FHALF_SCORE)
__PRECISION = ReturnType(name='precision', category=CATEGORY_MAXIMIZATION, type=TYPE_PRECISION)
__RECALL = ReturnType(name='recall', category=CATEGORY_MAXIMIZATION, type=TYPE_RECALL)



