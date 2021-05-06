import ast
import os
import pandas as pd
from statemachine import StateMachine, State


class Signal(State):
    def on_event(self, event):
        if event == 'pin_entered':
            return Link()
        return self


class Link(State):
    def on_event(self, event):
        if event == 'pin_entered':
            return Link()
        return self


def countList(states, param):
    counter = 0
    for state in states:
        if str(state.name).__contains__(param):
            counter = counter + 1
    return counter


def getSignal(states, signal):
    i = 0
    for state in states:
        if str(state.name).__contains__('s') and str(state.name).__contains__(str(signal)):
            return state
        i = i + 1


if __name__ == '__main__':
    folder_name = 'D:/CASE STUDY/ptSTL/stl_fs_sm-master/stl_fs_sm-master/test_data/traffic_data/traffic_data_l6/'
    filename = folder_name + '/system_properties'
    with open(filename) as f:
        content = f.readlines()
    content = [x.strip() for x in content]

    variables = ast.literal_eval(content.__getitem__(0))
    constraints = ast.literal_eval(content.__getitem__(2))

    states = []
    signal = 0
    for variable in variables:
        variable = 'x' + str(variable)
        elem = constraints.get(variable)
        if 'a' in elem and 'b' in elem:
            elem = [0, 1]
            variable = 's' + str(signal)
            signal = signal + 1
            states.append(Signal(variable, value=elem))

        if variable == 'x0':
            states.append(Link(variable, initial=True, value=elem))
        if variable.__contains__('x'):
            states.append(Link(variable, value=elem))
    for state in states:
        print(state)

    transitions = []
    signalCount = countList(states, 's');
    i = 0
    linkCount = (states.__len__() - signalCount)

    k = 0
    while k < signalCount and (k + 1) < linkCount:
        fromState = states.__getitem__(k)
        toSignal = getSignal(states, k)
        signalToState = states.__getitem__(k + 1)
        transitions.append(fromState.to(toSignal))
        transitions.append(toSignal.to(signalToState))
        k = k + 1

    z = 0
    while z < signalCount and z < linkCount:
        fromState = states.__getitem__(z + signalCount + 1)
        toSignal = getSignal(states, z)
        transitions.append(fromState.to(toSignal))
        z = z + 1

    v = 0
    while v < signalCount and (v + 2 * signalCount + 1) < linkCount:
        fromSignal = getSignal(states, v)
        toState = states.__getitem__(v + 2 * signalCount + 1)
        transitions.append(fromSignal.to(toState))
        v = v + 1

    for transition in transitions:
        print(transition)

    allData = []
    for file in os.listdir(folder_name):
        filepath = os.path.join(folder_name, file)
        data = []
        with open(filepath, 'r') as f:
            if not file.endswith('label') and not file.endswith('properties'):
                data = pd.read_csv(folder_name + '/' + file, sep=" ", header=None)
                data.columns = ["step", "x0", "x1", "x2", "x3", "x4", "x5", "s0", "s1"]
                allData.append(data)
    # print(allData)

    count = 0
    totalCount = 0
    rule1 = 0
    rule2 = 0
    rule3 = 0
    totalData = 0
    mismatch = 0
    for data in allData:
        print('**************************FILE: test_', count, '**************************')
        count = count + 1
        step = 0
        data=data.iloc[11:]
        for index, row in data.iterrows():
            totalData = totalData + 1
            if step + 1 == row['step']:
                print(row)
                step = 0
                if(row['x1']>30):
                    totalCount = totalCount + 1
                if row['x1']<30:
                    mismatch=mismatch+1

            if row['s0'] == 0 and row['s1'] == 1 and row['x1'] > 15 :
                rule1 = rule1 + 1
                step = row['step']

            if row['s1'] == 1 and row['x1'] > 25 :
                rule2 = rule2 + 1
                step = row['step']

            if row['s0'] == 0 and row['s1'] == 1 and row['x4'] < 10:
                rule3 = rule3 + 1
                step = row['step']

    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^TOTAL CASE FOUND: ', totalCount, '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^MISMATCH COUNT: ', mismatch, '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^TOTAL DATA: ', totalData, '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
