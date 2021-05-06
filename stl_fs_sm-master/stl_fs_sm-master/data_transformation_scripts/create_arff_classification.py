import sys
from collections import deque
import time

def main(argv):
    start_time = time.time()
    signal_file_names = ["sgt_"+str(n)+"_labeled" for n in range(400, 775)] #775

    window_size = int(argv[2])
    with open(argv[1], 'w') as arff_file:
        arff_file.write('@relation marine\n')
        for i in range(5 * window_size):
            arff_file.write('@attribute {0} REAL\n'.format(i+1))
        arff_file.write('@attribute alarm {0, 1}\n')
        arff_file.write('@data\n')

        for i, sfn in enumerate(signal_file_names):
            print("at file num = ", i)
            with open(sfn) as signal_file:
                signal_file.readline()
                signals1 = deque(maxlen=window_size)
                signals2 = deque(maxlen=window_size)
                signals3 = deque(maxlen=window_size)
                signals4 = deque(maxlen=window_size)
                signals5 = deque(maxlen=window_size)
                labels = deque(maxlen=window_size)

                for signal_line in signal_file:
                    pair = signal_line.split(',')
                    signals1.append(float(pair[0]))
                    signals2.append(float(pair[1]))
                    signals3.append(float(pair[2]))
                    signals4.append(int(pair[3]))
                    signals5.append(int(pair[4]))
                    labels.append(int(pair[5]))

                    if len(signals1) == window_size:
                        for elem in signals1:
                            arff_file.write('{0:.1f},'.format(elem))
                        for elem in signals2:
                            arff_file.write('{0:.5f},'.format(elem))
                        for elem in signals3:
                            arff_file.write('{0:.5f},'.format(elem))
                        for elem in signals4:
                            arff_file.write('{0},'.format(elem))
                        for elem in signals5:
                            arff_file.write('{0},'.format(elem))
                        arff_file.write('{0}\n'.format(int(pair[5])))
                        #if labels.count(1) > 0:
                        #    arff_file.write('1\n')
                        #else:
                        #    arff_file.write('0\n')
    # print running time
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main(sys.argv)
