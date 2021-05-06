def calculate_f1_score(detailed_result):

    return calculate_f_Beta_score(detailed_result, 1)

def calculate_fhalf_score(detailed_result):

    return calculate_f_Beta_score(detailed_result, 0.5)

def calculate_f_Beta_score(detailed_result, Beta):
    # detailed result is false_positive, false_negative, true_positive, true_negative
    precision = calculate_precision(detailed_result)
    recall = calculate_recall(detailed_result)

    if(precision == 0 or recall == 0):
        return 0
    else:
        return float ((1 + Beta * Beta) * precision * recall) / (Beta * Beta * precision + recall)

def calculate_precision(detailed_result):
    false_positive = detailed_result[0]
    true_positive = detailed_result[2]
    # HANDLE DIVISION BY ZERO
    if true_positive == 0 and false_positive == 0 :
        return 0
    else:
        return float(true_positive) / (true_positive + false_positive)


def calculate_recall(detailed_result):
    false_negative = detailed_result[1]
    true_positive = detailed_result[2]
    #HANDLE DIVISION BY ZERO
    if true_positive == 0 and false_negative == 0:
        return 0
    else:
        return float (true_positive) / (true_positive + false_negative)