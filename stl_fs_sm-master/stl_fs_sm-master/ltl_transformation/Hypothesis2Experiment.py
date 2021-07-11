import ast
import sys

from GenerateSedML import generateSedML
from GenerateXperimenter import generateXperimenter

optimized_formula = sys.argv[1]

folder_name = 'D:/CASE STUDY/ptSTL/stl_fs_sm-master/stl_fs_sm-master/test_data/traffic_data/traffic_data_l6/'
optimized_formula1 = '( P 1 1 ( ( v1 > 15 ) & ( v7 = 1 ) & ( v6 = 0 ) ) )'
optimized_formula2 = '( P 1 1 ( ( v1 > 25 ) & ( v7 = 1 ) ) )'
optimized_formula3 = '( P 1 1 ( ( v4 < 10 ) & ( v7 = 1 ) & ( v6 = 0 ) ) )'
filename = folder_name + '/system_properties'
with open(filename) as f:
    content = f.readlines()
content = [x.strip() for x in content]

variables = ast.literal_eval(content.__getitem__(0))
constraints = ast.literal_eval(content.__getitem__(2))

print('************************ SedML ****************************')
generateSedML(variables, optimized_formula1, optimized_formula2, optimized_formula3)

print('************************ Xperimenter ****************************')
generateXperimenter(variables, constraints)

