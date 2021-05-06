import mtl
import sys
from mtl import utils

print (sys.argv[1])
#( XX p0 & ( p1 & p2 ) ) {'x5=0.0': 'p0', 'x3>10.0': 'p1', 'x2<20.0': 'p2'}
# Assumes piece wise constant interpolation. (time, val)
#phi1 = mtl.parse('((a & b & c) | d | e)')
#phi2 = mtl.parse('(a -> b) & (~a -> c)')
#phi3 = mtl.parse('(a -> b -> c)')
#phi4 = mtl.parse('(a <-> b <-> c)')
#phi5 = mtl.parse('(x ^ y ^ z)')

# Eventually `x` will hold.
phi1 = mtl.parse('F x')

# `x & y` will always hold.
phi2 = mtl.parse('G(x & y)')

# `x` holds until `y` holds.
# Note that since `U` is binary, it requires parens.
phi3 = mtl.parse('(x U y)')

# Weak until (`y` never has to hold).
phi4 = mtl.parse('(x W y)')

# Whenever `x` holds, then `y` holds in the next two time units.
phi5 = mtl.parse('G(x -> F[0, 2] y)')

# We also support timed until.
phi6 = mtl.parse('(a U[0, 2] b)')

# Finally, if time is discretized, we also support the next operator.
# Thus, LTL can also be modeled.
# `a` holds in two time steps.
phi7 = mtl.parse('XX a')

# Assumes piece wise constant interpolation.
data = {
    'a': [(0, True), (1, False), (3, False)],
    'b': [(0, False), (0.2, True), (4, False)]
}
phiTest = mtl.parse('F(a | b)')
print(phiTest(data, quantitative=False))
# output: True

phiTest = mtl.parse('F(a | b)')
print(phiTest(data))
# output: True

# Note, quantitative parameter defaults to False

# Evaluate at t=3.
print(phiTest(data, time=3))
# output: False

# Compute sliding satisifaction.
print(phiTest(data, time=None))
# output: [(0, True), (0.2, True), (4, False)]

# Evaluate with discrete time
phiTest = mtl.parse('X b')
print(phiTest(data, dt=0.2))
# output: True

