import xml.etree.ElementTree as ET
from XmlOperations import indent


def generateSimulation(listOfSimulations):
    uniformTimeCourseAttr = {"initialTime": "0", "outputStartTime": "0", "outputEndTime": "100",
                             "numberOfPoints": "1000", "id": "simulation"}
    uniformTimeCourses = ET.SubElement(listOfSimulations, "uniformTimeCourse", attrib=uniformTimeCourseAttr)
    algorithmAttr = {"kisaoID": "KISAO:0000088", }
    ET.SubElement(uniformTimeCourses, "algorithm", attrib=algorithmAttr)


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


def generateSedML(systemVariables):
    sedmlAttr = {"xmlns:math": "http://www.w3.org/1998/Math/MathML",
                 "xmlns": "http://sed-ml.org/", "level": "1", "version": "1"}
    root = ET.Element("sedML", attrib=sedmlAttr)

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
    tree.write("D:/CASE STUDY/ptSTL/stl_fs_sm-master/stl_fs_sm-master/ltl_transformation/sedml.xml", encoding="utf-8",
               xml_declaration=True)
    with open("D:/CASE STUDY/ptSTL/stl_fs_sm-master/stl_fs_sm-master/ltl_transformation/sedml.xml", 'r') as fin:
        print(fin.read())
