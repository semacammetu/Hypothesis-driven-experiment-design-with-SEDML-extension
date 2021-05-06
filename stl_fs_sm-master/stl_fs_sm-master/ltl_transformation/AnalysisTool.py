import os
import sys

import easygui as eg
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import stats
from sklearn import linear_model
from statsmodels.formula.api import ols

folder_name = 'D:/CASE STUDY/ptSTL/stl_fs_sm-master/stl_fs_sm-master/test_data/hospital_bed_data/'


def query(queryString, allData):
    fileIndex = 0
    hypothesisMatchingCount = 0
    totalCount = 0
    for data in allData:
        result = data.query(queryString)
        totalCount = totalCount + len(data)
        hypothesisMatchingCount = hypothesisMatchingCount + len(result)
        plt.plot(result["step"], result["v0"], label="v0")
        plt.plot(result["step"], result["v1"], label="v1")
        plt.plot(result["step"], result["v2"], label="v2")
        plt.plot(result["step"], result["v3"], label="v3")
        plt.plot(result["step"], result["v4"], label="v4")
        plt.plot(result["step"], result["v5"], label="v5")
        plt.plot(result["step"], result["v6"], label="v6")
        plt.plot(result["step"], result["v7"], label="v7")
        plt.title('Dataset ' + str(fileIndex) + ' for query: ' + queryString)
        fileIndex = fileIndex + 1
        plt.legend()
        plt.show()
    print('                   QUERY MISMATCHING STEP COUNT: ', totalCount - hypothesisMatchingCount)
    print('                      QUERY MATCHING STEP COUNT: ', hypothesisMatchingCount)
    print('                               TOTAL STEP COUNT: ', totalCount)


def doHistogram(allData):
    fileIndex = 0
    for data in allData:
        print('***************************** FILE: test_', fileIndex, '******************************')
        plt.hist(data["v0"].sort_index(), color='blue', edgecolor='black', bins=int(180 / 15), label="v0")
        plt.xlabel('Value')
        plt.ylabel('Count')

        plt.hist(data["v1"].sort_index(), color='green', edgecolor='black', bins=int(180 / 15), label="v1")
        plt.xlabel('Value')
        plt.ylabel('Count')

        plt.hist(data["v2"].sort_index(), color='black', edgecolor='black', bins=int(180 / 15), label="v2")
        plt.xlabel('Value')
        plt.ylabel('Count')

        plt.hist(data["v3"].sort_index(), color='yellow', edgecolor='black', bins=int(180 / 15), label="v3")
        plt.xlabel('Value')
        plt.ylabel('Count')

        plt.hist(data["v4"].sort_index(), color='orange', edgecolor='black', bins=int(180 / 15), label="v4")
        plt.xlabel('Value')
        plt.ylabel('Count')

        plt.hist(data["v5"].sort_index(), color='white', edgecolor='black', bins=int(180 / 15), label="v5")
        plt.xlabel('Value')
        plt.ylabel('Count')

        plt.hist(data["v6"].sort_index(), color='brown', edgecolor='black', bins=int(180 / 15), label="v6")
        plt.xlabel('Value')
        plt.ylabel('Count')

        plt.hist(data["v7"].sort_index(), color='purple', edgecolor='black', bins=int(180 / 15), label="v7")
        plt.xlabel('Value')
        plt.ylabel('Count')
        plt.title("Histogram for dataset " + str(fileIndex))
        plt.legend()
        plt.show()
        fileIndex = fileIndex + 1


def doLinearRegression(allData):
    fileIndex = 0
    for data in allData:
        print('***************************** FILE: test_', fileIndex, '******************************')
        regr = linear_model.LinearRegression()

        datav0 = np.array(data["v0"].values.tolist())
        datav1 = np.array(data["v1"].values.tolist())

        regr.fit(datav0.reshape(1, -1), datav1.reshape(1, -1))
        plt.scatter(datav0, datav1, color='black')
        plt.plot(datav0, datav1, color='blue', linewidth=3, label="v0 vs v1")

        datav2 = np.array(data["v2"].values.tolist())
        regr.fit(datav1.reshape(1, -1), datav2.reshape(1, -1))
        plt.scatter(datav1, datav2, color='black')
        plt.plot(datav1, datav2, color='orange', linewidth=3, label="v1 vs v2")

        datav3 = np.array(data["v3"].values.tolist())
        regr.fit(datav2.reshape(1, -1), datav3.reshape(1, -1))
        plt.scatter(datav2, datav3, color='black')
        plt.plot(datav2, datav3, color='orange', linewidth=3, label="v2 vs v3")

        datav4 = np.array(data["v4"].values.tolist())
        regr.fit(datav3.reshape(1, -1), datav4.reshape(1, -1))
        plt.scatter(datav3, datav4, color='black')
        plt.plot(datav3, datav4, color='red', linewidth=3, label="v3 vs v4")

        datav5 = np.array(data["v5"].values.tolist())
        regr.fit(datav4.reshape(1, -1), datav5.reshape(1, -1))
        plt.scatter(datav4, datav5, color='black')
        plt.plot(datav4, datav5, color='yellow', linewidth=3, label="v4 vs v5")

        datav6 = np.array(data["v6"].values.tolist())
        regr.fit(datav5.reshape(1, -1), datav6.reshape(1, -1))
        plt.scatter(datav5, datav6, color='black')
        plt.plot(datav5, datav6, color='green', linewidth=3, label="v5 vs v6")

        datav7 = np.array(data["v7"].values.tolist())
        regr.fit(datav6.reshape(1, -1), datav7.reshape(1, -1))
        plt.scatter(datav6, datav7, color='black')
        plt.plot(datav6, datav7, color='brown', linewidth=3, label="v6 vs v7")

        plt.title("Linear regression for dataset " + str(fileIndex))
        plt.legend()
        plt.show()

        fileIndex = fileIndex + 1


def doStudentT(allData):
    fileIndex = 0
    for data in allData:
        print('***************************** FILE: test_', fileIndex, '******************************')
        resultv0 = stats.ttest_1samp(data['v0'], 0)
        resultv1 = stats.ttest_1samp(data['v1'], 0)
        resultv2 = stats.ttest_1samp(data['v2'], 0)
        resultv3 = stats.ttest_1samp(data['v3'], 0)
        resultv4 = stats.ttest_1samp(data['v4'], 0)
        resultv5 = stats.ttest_1samp(data['v5'], 0)
        resultv6 = stats.ttest_1samp(data['v6'], 0)
        resultv7 = stats.ttest_1samp(data['v7'], 0)
        plt.plot(resultv0, label="v0")
        plt.plot(resultv1, label="v1")
        plt.plot(resultv2, label="v2")
        plt.plot(resultv3, label="v3")
        plt.plot(resultv4, label="v4")
        plt.plot(resultv5, label="v5")
        plt.plot(resultv6, label="v6")
        plt.plot(resultv7, label="v7")
        plt.xlabel('P value')
        plt.ylabel('T statistic')
        plt.title("Histogram for dataset " + str(fileIndex))
        plt.legend()
        plt.show()

        fileIndex = fileIndex + 1


def doStudentZ(allData):
    fileIndex = 0
    for data in allData:
        print('***************************** FILE: test_', fileIndex, '******************************')
        fileIndex = fileIndex + 1


def doAnovaTest(allData):
    fileIndex = 0
    for data in allData:
        print('***************************** FILE: test_', fileIndex, '******************************')
        # One - Way ANOVA
        fvalue, pvalue = stats.f_oneway(data['v0'], data['v1'], data['v2'], data['v3'], data['v4'], data['v5'], data['v6'], data['v7'])
        resultOneWay="One way ANOVA: fvalue: " + str(fvalue), " pvalue: "+str(pvalue)
        print (resultOneWay)

        #Two - Way ANOVA
        for variable in data.columns:
            model = ols('{} ~ v0'.format(variable), data=data).fit()
            anova_table = sm.stats.anova_lm(model, typ=2)
            print(anova_table)


def doStatisticsSummary(allData):
    fileIndex = 0
    for data in allData:
        print('***************************** FILE: test_', fileIndex, '******************************')
        resultv0 = str(data['v0'].describe())
        resultv1 = str(data['v1'].describe())
        resultv2 = str(data['v2'].describe())
        resultv3 = str(data['v3'].describe())
        resultv4 = str(data['v4'].describe())
        resultv5 = str(data['v5'].describe())
        resultv6 = str(data['v6'].describe())
        resultv7 = str(data['v7'].describe())
        result = resultv0 + "/n" + resultv1 + resultv2 + "/n" + resultv3 + "/n" + resultv4 + "/n" + resultv5 + "/n" + resultv6 + "/n" + resultv7
        eg.textbox(result, "Summary statistics of dataset " + str(fileIndex))

        fileIndex = fileIndex + 1


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

    while True:
        try:
            listOfOptions = ["query", "statistical analysis", "exit"]
            question = "Select an analysis option"
            title = "Analysis Tool for Experiment"
            choice = eg.choicebox(question, title, listOfOptions)
            if choice.__contains__("query"):
                queryString = eg.textbox("Enter a query: ")
                query(queryString, allData)
            elif choice == "statistical analysis":
                listOfStatisticalOptions = ["Histogram of datasets", "Statistics summary", "Linear regression",
                                            "Student T test", "Student Z test", "Analysis of Variance (ANOVA) test"]
                statQuestion = "Select an statistical analysis option"
                statTitle = "Analysis Tool for Experiment"
                statisticalChoice = eg.multchoicebox(statQuestion, statTitle, listOfStatisticalOptions)
                if statisticalChoice.__contains__("Histogram of datasets"):
                    doHistogram(allData)
                if statisticalChoice.__contains__("Student T test"):
                    doStudentT(allData)
                if statisticalChoice.__contains__("Student Z test"):
                    doStudentZ(allData)
                if statisticalChoice.__contains__("Analysis of Variance (ANOVA) test"):
                    doAnovaTest(allData)
                if statisticalChoice.__contains__("Linear regression"):
                    doLinearRegression(allData)
                if statisticalChoice.__contains__("Statistics summary"):
                    doStatisticsSummary(allData)
            elif statisticalChoice == "exit":
                    sys.exit(0)
        except Exception:
            sys.exit(0)