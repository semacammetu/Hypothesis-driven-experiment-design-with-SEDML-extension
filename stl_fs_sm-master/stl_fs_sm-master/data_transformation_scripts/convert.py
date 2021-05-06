import sys
import csv

def minute_counter(start, end):
    start_date, start_time = start.split(' ')
    start_day, start_mounth, start_year = [int(i) for i in start_date.split('-')]
    start_hour, start_minute = [int(i) for i in start_time.split(':')]
    end_date, end_time = end.split(' ')
    end_day, end_mounth, end_year = [int(i) for i in end_date.split('-')]
    end_hour, end_minute = [int(i) for i in end_time.split(':')]

    if end_mounth != start_mounth:
        if start_mounth in [1, 3, 5, 7, 8, 10, 12]:
            end_day += 31
        elif start_mounth in [4, 6, 9, 11]:
            end_day += 30
        else:
            end_day += 28 # in 2015
    if end_day != start_day:
        end_hour += (end_day - start_day) * 24
    if end_hour != start_hour:
        end_minute += (end_hour - start_hour) * 60

    diff = end_minute - start_minute
    if diff > 30:
        diff = 30
    return diff

def main(argv):
    with open('debs2018_training_fixed_5.csv', mode='r') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        trip_count = 0
        line_count = 0
        trip_id = ""
        for row in readCSV:
            if line_count == 0:
                print(', '.join(row))
            elif trip_id != row[10]:
                if trip_id != "":
                    f.write(last_row[2] + ', ' + last_row[4] + ', ' + last_row[3] + ', ' + last_row[5] + ', ' + last_row[6] + '\n')
                    f.close()
                f = open('sgt_' + str(trip_count), 'w')
                trip_count += 1
                trip_id = row[10]
                # 
                f.write(row[12] + ', ' + row[1] + ', ' + row[8] + ', ' + row[10] + ', ' + row[0] + '\n')
                time = row[7]
                last_row = row
            else:
                diff = minute_counter(time, row[7])
                for i in range(diff):
                    f.write(last_row[2] + ', ' + last_row[4] + ', ' + last_row[3] + ', ' + last_row[5] + ', ' + last_row[6] + '\n')
                time = row[7]
                last_row = row

            line_count += 1
        print(trip_count)

        
if __name__ == "__main__":
    main(sys.argv)
