
STLOperators = ['F', 'G', 'U', 'S', 'P', 'A']
# F : Eventually, future operator.
# G : Globally, future operator.
# U : Until, future operator.
# S : Since, past operator.
# P : Previously, past operator, a.k.a F-,
# A : Always in the past, past operator, a.k.a G-
STLPastOperators = ['S', 'P', 'A']
BooleanOperators = ['&', '|', '!']
MetricOperators = ['>', '<', '=']

# Precedence for parsing.
PREC = {'(': 0, 'F': 5, 'G': 5, 'U': 4, '&': 3, '|': 3, '!': 5, 'P': 5, 'A': 5, 'S': 3}

MAX_VAL = 10000000
MIN_VAL = -10000000


# Helper functions
def is_operand(x):
  if x not in STLOperators and x not in BooleanOperators and x not in [')', '(']:
    return True
  return False

def is_unary(x):
  if x in ['!','A','P','F','G']:
    return True
  return False
  
def is_binary(x):
  if x in ['U', '&', '|', 'S']:
    return True
  return False

def is_boolean(x):
  if x in BooleanOperators:
    return True
  return False
