def generateXperimenter(variables, constraints, description='"description"'):
    xperimenter = open('D:/CASE STUDY/xperimenter.xpr', "w")
    xperimenter.write('experiment experiment{')
    xperimenter.write('\n\t desc {0};'.format(description))
    xperimenter.write('\n\t objective COMPARATIVE;')
    xperimenter.write('\n\t design design;')
    xperimenter.write('\n\t simulation simulation;')
    xperimenter.write('\n\t analysis AnovaAnalysis;')
    xperimenter.write('\n\t visual DEFAULT;')
    xperimenter.write('\n\t target KEPLER;')
    xperimenter.write('\n}')
    varList = ''
    for variable in variables:
        variable = 'v' + str(variable)
        elem = constraints.get(variable)
        if elem is not None and 'a' in elem and 'b' in elem:
            xperimenter.write('\nvariable {0}: BOOLEAN group RESPONSE;'.format(variable))
        else:
            xperimenter.write(
                '\nvariable {0}: INTEGER group FACTOR {1};'.format(variable, str(constraints.get(variable))))
        varList = varList + variable + ' '

    xperimenter.write('\ndesign design{')
    xperimenter.write('\n\t method FULLFACTORIAL;')
    xperimenter.write('\n\t varlist %s;' % varList)
    xperimenter.write('\n}')

    xperimenter.write('\nsimulation simulation{')
    xperimenter.write('\n\t modelFile D:/CASE STUDY/ptSTL/stl_fs_sm-master/stl_fs_sm-master/test_data/traffic_data/traffic_data_l6/;')
    xperimenter.write('\n\t modelType DISCRETEEVENT;')
    for variable in variables:
        variable = 'x' + str(variable)
        xperimenter.write('\n\t inport {0}:  {0};'.format(variable))
    xperimenter.write('\n}')

    xperimenter.write('\nanalysis AnovaAnalysis{')
    xperimenter.write('\n\t file "http://ceng.metu.edu.tr/~e1564178/xperimenter/anova-service";')
    xperimenter.write('\n}')
    xperimenter.close()

    with open('D:/CASE STUDY/xperimenter.xpr', 'r') as fin:
        print(fin.read())
