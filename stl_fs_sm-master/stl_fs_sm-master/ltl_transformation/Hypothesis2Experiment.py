import ast
import sys

from GenerateSedML import generateSedML
from GenerateXperimenter import generateXperimenter

optimized_formula = sys.argv[1]

folder_name = 'D:/CASE STUDY/ptSTL/stl_fs_sm-master/stl_fs_sm-master/test_data/traffic_data/traffic_data_l6/'
filename = folder_name + '/system_properties'
with open(filename) as f:
    content = f.readlines()
content = [x.strip() for x in content]

variables = ast.literal_eval(content.__getitem__(0))
constraints = ast.literal_eval(content.__getitem__(2))

print('************************ SedML ****************************')
generateSedML(variables)

print('************************ Xperimenter ****************************')
generateXperimenter(variables, constraints)

