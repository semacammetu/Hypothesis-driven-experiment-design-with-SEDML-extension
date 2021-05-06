import sys

from trace_checker import STL
import evaluator
import stl_constants

#( XX p0 & ( p1 & p2 ) ) {'x5=0.0': 'p0', 'x3>10.0': 'p1', 'x2<20.0': 'p2'}
#( p0 & XX p1 ) {'x5=0.0': 'p0', 'x3>10.0': 'p1'}
#( P 1 1 ( ( x1 > 15 ) & ( x7 = 1 ) & ( x6 = 0 ) ) )  |  ( P 1 1 ( ( x1 > 25 ) & ( x7 = 1 ) ) )  |  ( P 1 1 ( ( x4 < 10 ) & ( x7 = 1 ) & ( x6 = 0 ) ) )

#print(sys.argv[1])
#optimized_formula=sys.argv[1]
optimized_formula='( P 1 1 ( ( v1 > 15 ) & ( v7 = 1 ) & ( v6 = 0 ) ) )  |  ( P 1 1 ( ( v1 > 25 ) & ( v7 = 1 ) ) )  |  ( P 1 1 ( ( v4 < 10 ) & ( v7 = 1 ) & ( v6 = 0 ) ) )'
folder_name = 'D:/CASE STUDY/ptSTL/stl_fs_sm-master/stl_fs_sm-master/test_data/traffic_data/traffic_data_l6/'
signal_file_base = 'test'

result = evaluator.evaluate_signals(STL.infix_to_prefix(optimized_formula), folder_name, signal_file_base, 20,
                                    '',
                                    stl_constants.__DETAILED, stn=None,
                                    past_results=[])
# print('for formula = ' + optimized_formula + ' result is: ' + str(result))

print(str(result))
#[22, 2, 454, 1322]