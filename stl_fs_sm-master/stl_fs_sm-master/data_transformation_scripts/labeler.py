import sys
import csv

def main(argv):
    port = argv[1]
    percent = int(argv[2])
    signal_file_names = ["sgt_"+str(n) for n in range(775)]
    output_file_names = ["sgt_"+str(n)+"_labeled" for n in range(775)]
    for i, sfn in enumerate(signal_file_names):
        with open(sfn) as signal_file:
            for data_count, l in enumerate(signal_file):
                pass
        with open(sfn) as signal_file:
            with open(output_file_names[i], 'w') as output_file:
                line_count = 0
                signal_line = signal_file.readline() # read the first line of signal file
                meta = signal_line.split(',')
                destination = meta[0]
                if destination == port:
                    one_start = (data_count / 100) * percent
                else:
                    one_start = data_count + 1
                print(destination, port, one_start)
                output_file.write(signal_line)
                for signal_line in signal_file:
                    output_file.write(', '.join(signal_line.replace('\n','').split(', ')))
                    if line_count < one_start:
                        output_file.write(', 0\n')
                    else:
                        output_file.write(', 1\n')
                    line_count += 1


if __name__ == "__main__":
    main(sys.argv)
