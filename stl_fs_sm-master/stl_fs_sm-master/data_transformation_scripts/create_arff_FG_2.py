import sys
import math
import time

def eventually(data, size):
    result = []
    number_of_results = len(data) // size
    for i in range(0, len(data), size):
        for j in range(i + size, len(data) + 1, size):
            result.append(max(data[i:j]))
        if number_of_results * size < len(data):
            result.append(max(data[i:]))
    return result

def globally(data, size):
    result = []
    number_of_results = len(data) // size
    for i in range(0, len(data), size):
        for j in range(i + size, len(data) + 1, size):
            result.append(min(data[i:j]))
        if number_of_results * size < len(data):
            result.append(min(data[i:]))
    return result

def main(argv):
    start_time = time.time()

    with open(argv[1]) as signal_file:
        with open(argv[2], 'w') as arff_file:
            dimension = int(argv[3])
            window_size = int(argv[4])

            for i in range(dimension + 3):
                dummy = signal_file.readline()

            arff_file.write('@relation cpu\n')
            n = math.ceil(int(dimension / 5) / window_size)
            for i in range(5 * n * (n + 1)):
                arff_file.write('@attribute {0} REAL\n'.format(i+1))
            arff_file.write('@attribute alarm {0, 1}\n')
            arff_file.write('@data\n')

            data_span = int(dimension / 5)
            for line in signal_file:
                raw_data = line.split(',')
                label = int(raw_data[-1])
                data1 = [float(x) for x in raw_data[0:data_span]]
                data1.reverse()
                data2 = [float(x) for x in raw_data[data_span:2*data_span]]
                data2.reverse()
                data3 = [float(x) for x in raw_data[2*data_span:3*data_span]]
                data3.reverse()
                data4 = [int(x) for x in raw_data[3*data_span:4*data_span]]
                data4.reverse()
                data5 = [int(x) for x in raw_data[4*data_span:5*data_span]]
                data5.reverse()

                result = globally(data1, window_size)
                for elem in result:
                    arff_file.write('{0:.1f},'.format(elem))

                result = eventually(data1, window_size)
                for elem in result:
                    arff_file.write('{0:.1f},'.format(elem))

                result = globally(data2, window_size)
                for elem in result:
                    arff_file.write('{0:.5f},'.format(elem))

                result = eventually(data2, window_size)
                for elem in result:
                    arff_file.write('{0:.5f},'.format(elem))

                result = globally(data3, window_size)
                for elem in result:
                    arff_file.write('{0:.5f},'.format(elem))

                result = eventually(data3, window_size)
                for elem in result:
                    arff_file.write('{0:.5f},'.format(elem))

                result = globally(data4, window_size)
                for elem in result:
                    arff_file.write('{0},'.format(elem))

                result = eventually(data4, window_size)
                for elem in result:
                    arff_file.write('{0},'.format(elem))

                result = globally(data5, window_size)
                for elem in result:
                    arff_file.write('{0},'.format(elem))

                result = eventually(data5, window_size)
                for elem in result:
                    arff_file.write('{0},'.format(elem))

                arff_file.write('{0}\n'.format(label))

    # print running time
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main(sys.argv)
