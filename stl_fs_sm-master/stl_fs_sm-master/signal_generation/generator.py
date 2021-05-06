
from . import sg
import os
from multiprocessing import Pool
import json
import math
from functools import partial
from trace_checker import STL



def generate_signals_push(folder_name, file_name, trace_count, pc=8):
  # ["duration", "violate", "min_v_dur", "max_v_dur", "v_dur", "min_step", "max_step"]
  options = sg.Options(duration=2000, violate=1, min_v_dur=50, v_dur=70, max_v_dur=100, min_step=1, max_step=5,
                       sleep=0, s_min=0, s_max=100, t=0)

  # Check if the directory exists, create if necessary:
  if not os.path.isdir(folder_name):
    os.mkdir(folder_name)

  # Store the options:
  j = json.dumps(options._asdict())
  with open(folder_name + "options.txt", 'w') as outfile:
    json.dump(j, outfile)

  partial_generator = partial(sg.signal_generator, folder_name=folder_name, name=file_name, s_type="PUSH",
                              options=options, additional_options=None)

  pool = Pool(processes=pc)
  pool.map(partial_generator, list(range(trace_count)))


  pool.close()
  pool.join()

def generate_signals(folder_name, file_name, trace_count, pc=8):
  # ["duration", "violate", "min_v_dur", "max_v_dur", "v_dur", "min_step", "max_step"]
  options = sg.Options(duration=500, violate=1, min_v_dur=30, v_dur=50, max_v_dur=100, min_step=1, max_step=5,
                       sleep=0, s_min=0, s_max=100, t=0)
  gauss_options = sg.GaussOptions(mean=15, deviation=6, v_diff=20)

  # Check if the directory exists, create if necessary:
  if not os.path.isdir(folder_name):
    os.mkdir(folder_name)

  # Store the options:
  j = json.dumps(options._asdict())
  with open(folder_name + "options.txt", 'w') as outfile:
    json.dump(j, outfile)

  j = json.dumps(gauss_options._asdict())
  with open(folder_name + "s_options.txt", 'w') as outfile:
    json.dump(j, outfile)

  partial_generator = partial(sg.signal_generator, folder_name=folder_name, name=file_name, s_type="GAUSS",
                              options=options, additional_options=gauss_options)

  pool = Pool(processes=pc)
  pool.map(partial_generator, list(range(trace_count)))


  pool.close()
  pool.join()


def generate_traffic_traces(folder_name, file_name, trace_count, viol_formula, traffic_file, duration, pc=8,
                            cause_formula=None):
  """

  Args:
    folder_name: The folder in which the signals will be stored.
    file_name: The base file name.
    trace_count: The number of traces to generate
    viol_formula: A string (STL formula for violating parts.)
    traffic_file: A file name. The file contains the traffic system properties.
    duration: A signal duration
    pc: The process count.
  """
  # Check if the directory exists, create if necessary:
  if not os.path.isdir(folder_name):
     os.mkdir(folder_name)

  if pc == 0:
    sg.traffic_signal_generator(0, folder_name, file_name, traffic_file, trace_count, viol_formula, duration)
  else:
    tc = int(math.ceil(float(trace_count)/pc)) # yukari yuvarla

    partial_generator = partial(sg.traffic_signal_generator, folder_name=folder_name, name=file_name,
                                traffic_file=traffic_file, trace_count=tc, viol_formula=viol_formula,
                                duration=duration)

    pool = Pool(processes=pc)
    pool.map(partial_generator, list(range(0, trace_count, tc)))
    #
    #
    pool.close()
    pool.join()

  metric_list, input_metrics, domains = sg.traffic_signal_generator(0, folder_name, file_name, traffic_file, 0, "", 0)

  system_properties = folder_name + "/system_properties"
  f = open(system_properties, "w")
  f.write(str(metric_list) + "\n")
  f.write(str(input_metrics)+ "\n")
  f.write(str(domains) + "\n")
  f.write(viol_formula)
  f.close()



