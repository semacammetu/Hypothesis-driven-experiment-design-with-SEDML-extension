import os

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
folder_name = 'D:/CASE STUDY/ptSTL/stl_fs_sm-master/stl_fs_sm-master/test_data/traffic_data/traffic_data_l6/'
optimized_formula1 = '( P 1 1 ( ( v1 > 15 ) & ( v7 = 1 ) & ( v6 = 0 ) ) )'
optimized_formula2 = '( P 1 1 ( ( v1 > 25 ) & ( v7 = 1 ) ) )'
optimized_formula3 = '( P 1 1 ( ( v4 < 10 ) & ( v7 = 1 ) & ( v6 = 0 ) ) )'

if __name__ == '__main__':

    allData = []
    for file in os.listdir(folder_name):
        filepath = os.path.join(folder_name, file)
        data = []
        with open(filepath, 'r') as f:
            if not file.endswith('label') and not file.endswith('properties'):
                data = pd.read_csv(folder_name + '/' + file, sep=" ", header=None)
                data.columns = ["step", "v0", "v1", "v2", "v3", "v4", "v5", "v6", "v7"]
                allData.append(data)

    filename = folder_name + '/system_properties'
    with open(filename) as f:
        content = f.readlines()
    content = [x.strip() for x in content]

    mismatchFormula = content.__getitem__(3).replace('x1', 'next')
    if content.__getitem__(3).__contains__('>'):
        congestionFormula = content.__getitem__(3).replace('>', '<')

    if content.__getitem__(3).__contains__('<'):
        congestionFormula = content.__getitem__(3).replace('<', '>')

    optimized_formula1 = optimized_formula1.replace('=', '==').replace('P 1 1', '')
    optimized_formula2 = optimized_formula2.replace('=', '==').replace('P 1 1', '')
    optimized_formula3 = optimized_formula3.replace('=', '==').replace('P 1 1', '')

    fileIndex = 0
    hypothesisMatchingCount = 0
    totalCount = 0
    mismatchCount = 0
    congestedCount = 0
    resultMismatchAll= pd.DataFrame(columns=["step", "v0", "v1", "v2", "v3", "v4", "v5", "v6", "v7"])
    for data in allData:
        print('***************************** FILE: test_', fileIndex, '******************************')
        fileIndex = fileIndex + 1

        # add one more column for next x1
        # clean the data set (remove first 10 line and last line)
        data.loc[0, 'next'] = 0
        for i in range(1, len(data) - 1):
            data.loc[i, 'next'] = data.loc[i + 1, 'v1']

        data.loc[100, 'next'] = 0
        data = data.iloc[10:]
        data.drop(data.tail(1).index, inplace=True)
        totalCount = totalCount + len(data)

        #        fig = go.Figure()
        #  fig.add_trace(go.Scatter(x=data['step'], y=data['x0'], mode='lines+markers', name='x0'))
        #  fig.add_trace(go.Scatter(x=data['step'], y=data['x1'], mode='lines+markers', name='x1'))
        #  fig.add_trace(go.Scatter(x=data['step'], y=data['x2'], mode='lines+markers', name='x2'))
        #   fig.add_trace(go.Scatter(x=data['step'], y=data['x3'], mode='lines+markers', name='x3'))
        #   fig.add_trace(go.Scatter(x=data['step'], y=data['x4'], mode='lines+markers', name='x4'))
        #   fig.add_trace(go.Scatter(x=data['step'], y=data['x5'], mode='lines+markers', name='x5'))
        #   fig.add_trace(go.Scatter(x=data['step'], y=data['x6'], mode='lines+markers', name='x6'))
        #   fig.add_trace(go.Scatter(x=data['step'], y=data['x7'], mode='lines+markers', name='x7'))
        #  fig.show(renderer="browser")

        # find congested x1 and its count
        congested = data.query('v1>30')
        congestedCount = congestedCount + len(congested)

        # find the steps providing the formula
        result = data.query(optimized_formula1 + ' | ' + optimized_formula2 + ' | ' + optimized_formula3)

        # find the steps providing the hypothesis
        hypothesisResult = result.query('next>30')
        hypothesisMatchingCount = hypothesisMatchingCount + len(hypothesisResult)
        print(hypothesisResult)

        # find mismatching steps
        resultMismatch = result.query(mismatchFormula)
        mismatchCount = mismatchCount + len(resultMismatch)

        resultMismatchAll = resultMismatchAll.append(resultMismatch)


        plt.plot(resultMismatchAll["step"], resultMismatchAll["v0"], 'd', label="v0")
        plt.plot(resultMismatchAll["step"], resultMismatchAll["v1"], 's', label="v1")
        plt.plot(resultMismatchAll["step"], resultMismatchAll["v4"], 'g^', label="v4")
        plt.plot(resultMismatchAll["step"], resultMismatchAll["v6"], 'ro', label="s0")
        plt.plot(resultMismatchAll["step"], resultMismatchAll["v7"], 'o', label="s1")

        plt.xticks(np.arange(40, 70, 5))
        plt.title('Hypothesis refuting values for v0, v1, v4, s0 and s1')
        plt.xlabel('Time')
        plt.ylabel('Value of v')
        plt.xlim(40,71)
        plt.legend()
        plt.show()
    print('***************************************************************************\n')

    print('                  HYPOTHESIS PROVING STEP COUNT: ', hypothesisMatchingCount)
    print('                 HYPOTHESIS REFUTING STEP COUNT: ', mismatchCount)
    print(' (CONGESTED v1 - HYPOTHESIS PROVING) STEP COUNT: ', congestedCount - hypothesisMatchingCount)
    print('                            EXCLUDED STEP COUNT: ', totalCount - congestedCount - mismatchCount)
    print('                             OVERALL STEP COUNT: ', totalCount)
