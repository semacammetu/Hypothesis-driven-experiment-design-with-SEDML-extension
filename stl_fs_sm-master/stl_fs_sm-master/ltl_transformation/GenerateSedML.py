import xml.etree.ElementTree as ET
from XmlOperations import indent


def generateSimulation(listOfSimulations):
    uniformTimeCourseAttr = {"initialTime": "0", "outputStartTime": "0", "outputEndTime": "100",
                             "numberOfPoints": "1000", "id": "simulation"}
    uniformTimeCourses = ET.SubElement(listOfSimulations, "uniformTimeCourse", attrib=uniformTimeCourseAttr)
    algorithmAttr = {"kisaoID": "KISAO:0000088", }
    ET.SubElement(uniformTimeCourses, "algorithm", attrib=algorithmAttr)


def generateHypothesis(listOfHypothesis, optimized_formula1, optimized_formula2, optimized_formula3):
    hypothesis1 = ET.SubElement(listOfHypothesis, "hypothesis")
    hypothesis2 = ET.SubElement(listOfHypothesis, "hypothesis")
    temporalOp1 = optimized_formula1.split(0, 5)
    exprOp1 = optimized_formula1.split(5, 20)
    conditionAttr1 = {"metaid": "C1", "expr": exprOp1, "temporal operator": temporalOp1}
    temporalOp2 = optimized_formula2.split(0, 5)
    exprOp2 = optimized_formula2.split(5, 20)
    conditionAttr2 = {"metaid": "C2", "expr": exprOp2, "temporal operator": temporalOp2}
    temporalOp3 = optimized_formula3.split(0, 5)
    exprOp3 = optimized_formula3.split(5, 20)
    conditionAttr3 = {"metaid": "C3", "expr": exprOp3, "temporal operator": temporalOp3}

    listOfConditions = ET.SubElement(hypothesis1, "listOfConditions")
    ET.SubElement(listOfConditions, "condition", attrib=conditionAttr1)
    ET.SubElement(listOfConditions, "condition", attrib=conditionAttr2)
    ET.SubElement(listOfConditions, "condition", attrib=conditionAttr3)

    listOfExpressions = ET.SubElement(hypothesis1, "listOfExpressions")
    expressionAttr1 = {"expr": exprOp1, "temporal operator": temporalOp1}
    ET.SubElement(listOfExpressions, "expression", attrib=expressionAttr1)

    listOfRelations = ET.SubElement(listOfHypothesis, "listOfRelations")
    relationAttr1 = {"relation": "CONTRADICT", "hyp": hypothesis1, "hyp": hypothesis2}
    ET.SubElement(listOfRelations, "relation", attrib=relationAttr1)

def generateModel(listOfModels):
    modelAttribute = {"id": "model", "language": "urn:sedml:language:sbml",
                      "source": "urn:miriam:biomodels.db:BIOMD0000000021"}
    model = ET.SubElement(listOfModels, "model", attrib=modelAttribute)


def generateTask(listOfTasks):
    taskAttr = {"simulationReference": "simulation",
                "modelReference": "model", "id": "task"}
    task = ET.SubElement(listOfTasks, "task", attrib=taskAttr)


def generateDataGenerators(listOfDataGenerators, systemVariables):
    variableTime = 'time'
    datageneratorAttr = {"id": variableTime + 'DG', "name": variableTime + 'DG'}
    datagenerator = ET.SubElement(listOfDataGenerators, "dataGenerator", attrib=datageneratorAttr)

    listOfVariables = ET.SubElement(datagenerator, "listOfVariables")
    timevariablesAttr = {"id": variableTime, "name": variableTime, "taskReference": "task"}
    ET.SubElement(listOfVariables, "variable", attrib=timevariablesAttr)

    mathAttr = {"xmlns": "http://www.w3.org/1998/Math/MathML"}
    math = ET.SubElement(datagenerator, "math:math", attrib=mathAttr)
    ET.SubElement(math, "math:ci").text = variableTime

    for variable in systemVariables:
        variable = 'x' + str(variable)
        datageneratorAttr = {"id": variable + "DG", "name": variable + "DG"}
        datagenerator = ET.SubElement(listOfDataGenerators, "dataGenerator", attrib=datageneratorAttr)

        listOfVariables = ET.SubElement(datagenerator, "listOfVariables")
        variablesAttr = {"id": variable, "name": variable, "taskReference": "task"}
        # , "target":"/sbml:sbml/sbml:model/sbml:listOfSpecies/sbml:species[@id='PX']"
        ET.SubElement(listOfVariables, "variable", attrib=variablesAttr)

        mathAttr = {"xmlns": "http://www.w3.org/1998/Math/MathML"}
        math = ET.SubElement(datagenerator, "math:math", attrib=mathAttr)
        ET.SubElement(math, "math:ci").text = variable


def generateListOfOutputs(listOfOutputs, systemVariables):
    plot2DAttr = {"id": "plot1_Basic"}
    plot2D = ET.SubElement(listOfOutputs, "plot2D", attrib=plot2DAttr)
    listOfCurves = ET.SubElement(plot2D, "listOfCurves")
    for variable in systemVariables:
        variableOut = 'x' + str(variable) + "DG"
        curveAttr = {"id": variableOut, "logX": "false", "logY": "false", "xDataReference": "timeDG",
                     "yDataReference": variableOut}
        ET.SubElement(listOfCurves, "curve", attrib=curveAttr)


def generateSedML(systemVariables, optimized_formula1, optimized_formula2, optimized_formula3):
    sedmlAttr = {"xmlns:math": "http://www.w3.org/1998/Math/MathML",
                 "xmlns": "http://sed-ml.org/", "level": "1", "version": "1"}
    root = ET.Element("sedML", attrib=sedmlAttr)

    listOfHypothesis = ET.SubElement(root, "listOfHypothesis")
    generateHypothesis(listOfHypothesis, optimized_formula1, optimized_formula2, optimized_formula3)

    listOfSimulations = ET.SubElement(root, "listOfSimulations")
    generateSimulation(listOfSimulations)

    listOfModels = ET.SubElement(root, "listOfModels")
    generateModel(listOfModels)

    listOfTasks = ET.SubElement(root, "listOfTasks")
    generateTask(listOfTasks)

    listOfDataGenerators = ET.SubElement(root, "listOfDataGenerators")
    generateDataGenerators(listOfDataGenerators, systemVariables)

    listOfOutputs = ET.SubElement(root, "listOfOutputs")
    generateListOfOutputs(listOfOutputs, systemVariables)

    tree = ET.ElementTree(root)
    indent(root)

    # writing xml
    tree.write("D:/CASE STUDY/ptSTL/stl_fs_sm-master/stl_fs_sm-master/ltl_transformation/SEDML_with_hypothesis.xml",
               encoding="utf-8",
               xml_declaration=True)
    with open("/ltl_transformation/SEDML_with_hypothesis.xml", 'r') as fin:
        print(fin.read())
