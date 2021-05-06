"""
Signal generator.
"""

from collections import namedtuple
from trace_checker import STL
from cause_mining_algo import controller_helper_funs as hf
#from cause_mining_algo import linked_list
import random
import numpy as np
import sys

# 4 commented out lines below must be uncommented and the directories must be updated whenever traffic-network-code
#  will be used in the code. The lines must be uncommented to use traffic example related functions in
#  cause_mining_algo module such as traffic_example.py.
sys.path.insert(0, '/Users/ebru/PycharmProjects/stl_fs_sm_cpy/traffic-network-code/traffic_network/')
sys.path.insert(0, '/Users/ebru/PycharmProjects/stl_fs_sm_cpy/traffic-network-code')

#from traffic_network import network
#from traffic_network import read_input



#import network # why are they red but not give out an error?
#import read_input

import copy
import random
from itertools import product
# from cause_mining_algo import linked_list as ll



Options = namedtuple('Options', ["duration", "violate", "min_v_dur", "max_v_dur", "v_dur", "min_step", "max_step",
                                 "sleep", "s_min", "s_max", "t"])
# duration: signal duration  (floating point)
# violate: violation occurs or not (boolean)
# min_v_dur: minimum violation duration
# max_v_dur: maximum violation duration
# v_dur: min_v_dur <= v_dur <= max_v_dur, [ v_dur, max_v_dur] will be labeled as violating
# min_step
# max_step
# sleep

GaussOptions = namedtuple('GaussOptions', ["v_diff", "mean", "deviation"])


def signal_generator(index, folder_name, name, s_type, options, additional_options):
  """
  Generate the signal and store it in a file according to given options.

  index: index of the signal
  name: signal name, e.g. metric name
  type: type of the generator
  options: generator options an instance of Options
  additional_options: additional options for generator type
  """
  f_signal_name = folder_name + "/" + name + "_" + str(index) # + "_" + str(options.t)
  f_label_name = f_signal_name + "_label"
  f_s = open(f_signal_name, 'w')
  f_l = open(f_label_name, 'w')

  if s_type == "GAUSS":
    gauss_signal_generator(f_s, f_l, options, additional_options)
  elif s_type == "PUSH":
    push_signal_generator(f_s, f_l, options)
  else:
    print("Unknown signal type:" + s_type)

  f_s.close()
  f_l.close()
  print("Done %d" % index)


  return


def push_signal_generator(f_s, f_l, options):
  passed_time = 0

  s = [0, 0]
  if options.violate:
    v_dur = random.uniform(options.min_v_dur, options.max_v_dur/2 )
    v_start_time = random.uniform(0, options.duration - v_dur)
    v_end_time = v_start_time + v_dur

    if v_start_time > options.duration/2:
      push_start_time = random.uniform(0, options.duration/2)
    else:
      push_start_time = random.uniform(options.duration/2, options.duration - v_dur)
    push_end_time = push_start_time + random.uniform(options.min_v_dur, options.max_v_dur)

  viol_rate = random.uniform(15, 25)
  with_push = random.uniform(20, 30)

  while passed_time < options.duration:

    s[0] = 0 # no push
    s[1] = 0 # no restart
    l = 0# no violation
    if random.uniform(0, 1) < 0.04:
      s[1] = random.uniform(0, 10) # no violation
    if v_start_time <= passed_time <= v_end_time:
      s[1] = viol_rate
      s[0] = 0
      l = 1 # violation

    if push_start_time <= passed_time <= push_end_time:
      s[1] = with_push
      s[0] = 1
      l = 0 # no violation

    step = random.randint(options.min_step, options.max_step)

    t = options.t + passed_time
    f_s.write("%s %s %s\n" % (str(t), str(s[0]), str(s[1])))
    f_l.write("%s %s\n" % (str(t), str(l)))

    if options.sleep:
      sys.sleep(step)
    passed_time += step

def gauss_signal_generator(f_s, f_l, options, gauss_options):
  passed_time = 0
  v_start_time = options.duration + 1
  v_label_time = options.duration + 1
  v_end_time = v_start_time

  if options.violate:
    v_dur = random.uniform(options.min_v_dur, options.max_v_dur)
    v_start_time = random.uniform(0, options.duration - v_dur)
    if v_dur >= options.v_dur:
      v_label_time = v_start_time + options.v_dur
    v_end_time = v_start_time + v_dur

  while passed_time < options.duration:

    s = random.gauss(gauss_options.mean, gauss_options.deviation)
    t = options.t + passed_time
    if v_start_time <= passed_time <= v_end_time:
      # s += gauss_options.v_diff
      s = random.gauss(gauss_options.mean +  gauss_options.v_diff, gauss_options.deviation)
    # additional noise:
    if random.uniform(0, 1) < 0.02:
      s = random.gauss(gauss_options.mean*3, gauss_options.deviation)
    s = min(s, options.s_max)
    s = max(s, options.s_min)
    f_s.write("%s %s\n" % (str(t), str(s)))
    if  v_label_time <= passed_time <= v_end_time:
      f_l.write("%s 1\n" % str(t))
    else:
      f_l.write("%s 0\n" % str(t))

    step = random.randint(options.min_step, options.max_step)
    if options.sleep:
      sys.sleep(step)
    passed_time += step


def traffic_signal_generator(trace_start_index, folder_name, name, traffic_file, trace_count, viol_formula, duration):
  """

  Args:
    trace_start_index:
    folder_name:
    name:
    traffic_file:
    trace_count:
    viol_formula:
    duration:

  Returns tuple (metrics,inputs, parameter_domains)  where
    metrics: The list of metrics
    inputs: A list of controllable metrics (inputs is subset of metrics)
    parameter_domains: A dictionary containing the domains of parameters

    Sample return: ([0,1,2], [2], {'p0': [0, 10], 'p1': [0, 10], 'p2': ['a', 'b']}) Note that the domain for the input
    metrics is always set valued.
  """

  # First construct the traffic network.
  # In loop, generate trace. check it against the formula, produce the label. Save both
  link_dict, intersection_dict = read_input.load_from_annotated_file(traffic_file)
  tn = network.Network(link_dict, intersection_dict, scale=5)

  tc = 0
  while tc < trace_count:
    index = trace_start_index + tc
    f_signal_name = folder_name + "/" + name + "_" + str(index)
    f_label_name = f_signal_name + "_label"
    f_s = open(f_signal_name, 'w')
    f_l = open(f_label_name, 'w')

    time = 0
    # The states of the links
    xk = np.zeros(tn.get_link_count())
    sm = [_ for _ in range(tn.get_intersection_count())]

    tn.initialize_links(xk, 0.1)
    tn.set_random_signal_mode(sm)

    # Initialize the checker:
    stn_viol = STL.SyntaxTreeNode()
    stn_viol.initialize_node(viol_formula.split(), 0)
    sm_numbers = [0 if x == 'a' else 1 for x in sm]

    while time <= duration:
      # Store the values to the file:
      stn_viol.compute_qv(STL.DataPoint(value=xk.tolist() + sm_numbers, time=time))
      f_s.write("%s %s %s\n" % (str(time), " ".join([str(x) for x in xk]), " ".join([str(x) for x in sm_numbers])))
      qual = 0 if stn_viol.qv >= 0 else 1
      f_l.write("%s %s\n" % (str(time), str(qual)))
      xk, _ = tn.step(xk, sm)
      tn.set_random_signal_mode(sm)
      sm_numbers = [0 if x == 'a' else 1 for x in sm]

      time += 1



    f_s.close()
    f_l.close()
    print("Done %d" % index)
    tc += 1

  if trace_count == 0:
    # return the set of metrics
    link_count = tn.get_link_count()
    link_metrics = list(range(0, link_count))
    intersection_metrics = list(range(tn.get_intersection_count()))
    intersection_metrics = [x + tn.get_link_count() for x in intersection_metrics] # shift the indices
    c = tn.get_all_intersection_indices_and_modes()

    parameter_domains = {}
    for i in range(tn.get_intersection_count()):
      pi = 'p' + str(i + link_count)
      parameter_domains[pi] = next(list(x[1].keys()) for x in c if x[0] == i)

    capacities = tn.np_xcap
    for i in range(link_count):
      parameter_domains['p'+str(i)] = [0, capacities[i]]
    return link_metrics+intersection_metrics, intersection_metrics, parameter_domains  # All metrics, set valued metrics, domains for set valued metrics

def label_test_file(test_file_name, label_file_name, viol_formula, duration):
# THIS DOES NOT WORK. I WILL FIX IT LATER!
  f_s = open(test_file_name, 'r')
  lines = f_s.readlines()
  f_l = open(label_file_name, 'w')

  time = 0

  # Initialize the checker:
  stn_viol = STL.SyntaxTreeNode()
  stn_viol.initialize_node(viol_formula.split(), 0)

  while time <= duration:
    # Store the values to the file:
    kk = [float(f) for f in lines[time].split()[1:6]]+[int(i) for i in lines[time].split()[6:]]
    stn_viol.compute_qv(STL.DataPoint(value=[float(f) for f in lines[time].split()[1:6]]+[int(i) for i in lines[time].split()[6:]], time=time))
    qual = 1 if stn_viol.qv > 0 else 0
    f_l.write("%s %s\n" % (str(time), str(qual)))

    time += 1

  f_s.close()
  f_l.close()
  print("Done!")


def signal_generator_for_plot(trace_start_index, folder_name, name, traffic_file, trace_count, viol_formula, duration,
                              formula):
    """

    Args:
      trace_start_index:
      folder_name:
      name:
      traffic_file:
      trace_count:
      viol_formula:
      duration:
      cause_formula: (prefix) This is None if we are not constructing a controller, has a value otherwise.

    Returns tuple (metrics,inputs, parameter_domains)  where
      metrics: The list of metrics
      inputs: A list of controllable metrics (inputs is subset of metrics)
      parameter_domains: A dictionary containing the domains of parameters

      Sample return: ([0,1,2], [2], {'p0': [0, 10], 'p1': [0, 10], 'p2': ['a', 'b']}) Note that the domain for the input
      metrics is always set valued.
    """

    # First construct the traffic network.
    # In loop, generate trace. check it against the formula, produce the label. Save both
    link_dict, intersection_dict = read_input.load_from_annotated_file(traffic_file)
    tn = network.Network(link_dict, intersection_dict, scale=5)

    tc = 0
    while tc < trace_count:
      index = trace_start_index + tc
      f_signal_name = folder_name + "/" + name + "_" + str(index)
      f_label_name = f_signal_name + "_label"
      f_formula_label_name = f_signal_name + "_formula_label"
      f_s = open(f_signal_name, 'w')
      f_l = open(f_label_name, 'w')
      f_fl = open(f_formula_label_name, 'w')

      time = 0
      # The states of the links
      xk = np.zeros(tn.get_link_count())
      sm = [_ for _ in range(tn.get_intersection_count())]

      tn.initialize_links(xk, 0.1)
      tn.set_random_signal_mode(sm)


      # Initialize the checker:
      stn_viol = STL.SyntaxTreeNode()
      stn_viol.initialize_node(viol_formula.split(), 0)
      stn_cause = STL.SyntaxTreeNode()
      stn_cause.initialize_node(formula.split(), 0)
      sm_numbers = [0 if x == 'a' else 1 for x in sm]

      while time <= duration:
        # Store the values to the file:
        stn_viol.compute_qv(STL.DataPoint(value=xk.tolist() + sm_numbers, time=time))
        f_s.write("%s %s %s\n" % (str(time), " ".join([str(x) for x in xk]), " ".join([str(x) for x in sm_numbers])))
        qual1 = 0 if stn_viol.qv >= 0 else 1
        f_l.write("%s %s\n" % (str(time), str(qual1)))
        stn_cause.compute_qv(STL.DataPoint(value=xk.tolist() + sm_numbers, time=time))
        qual2 = 0 if stn_cause.qv >= 0 else 1
        f_fl.write("%s %s\n" % (str(time), str(qual2)))

        xk, _ = tn.step(xk, sm)
        tn.set_random_signal_mode(sm)
        sm_numbers = [0 if x == 'a' else 1 for x in sm]

        time += 1

      f_s.close()
      f_l.close()
      f_fl.close()
      print("Done %d" % index)
      tc += 1



def xk_tolist(xk):

  if not type(xk) == list:
    try:
      xk = xk.tolist()
    except:
      try:
        xk = list(xk)
      except:
        print("xk is not a list, numpy array or a tuple. We must convert it to a list somehow for the controller.")
  return xk


def controller(folder_name, name, trace_count,  duration, viol_formula, cause_formula, step_function, xk_initialized,
               uk_domain, uk_count, num_to_let=False):

  """
  IMPORTANT!:  We make the assumption that an input value (control or system) is ordered in the following way:
  The first xk_count numbers starting from 0 are for system inputs, the following uk_count ones, starting from xk_count
  are control inputs. For example, if xk_count = 3 and uk_count = 2, x0,x1 and x2 are system inputs and x3,x4 are control
  inputs. We also make the assumption that uk_domain is the same for each control input.
  Args:
    folder_name:
    name:
    trace_count:
    viol_formula:
    duration:
    cause_formula: (prefix) This is None if we are not constructing a controller, has a value otherwise.
    step_function: a function xk, _ = step(xk,uk) that takes old xk and uk values and returns the new xk value with
    another unimportant value.
    uk_domain: (list) of domain of uk values
    uk_count: the number of control inputs
    xk_initialized: (tuple, numpy array or list) initialized xk values
    num_to_let:(bool) if step_function takes xk's in the form of letters a and b instead of numbers 1 and 0, this value
    must be given as True. This variable is set specifically for traffic network's step function's needs.

  """
  npml = 0  # "no possible modes left" count
  #viol_cnt = 0
  xk_count = len(xk_initialized)
  iter_uk_crossproduct = product(uk_domain, repeat=uk_count)
  uk_crossproduct = []
  # set list of all possible uk combinations
  for prod in iter_uk_crossproduct:
      uk_crossproduct.append(prod)

  # First construct the traffic network.
  # In loop, generate trace. check it against the formula, produce the label. Save both

  tc = 0
  while tc < trace_count:
    f_signal_name = folder_name + "/" + name + "_" + str(tc)
    f_label_name = f_signal_name + "_label"
    f_s = open(f_signal_name, 'w')
    f_l = open(f_label_name, 'w')

    time = 0
    # initialize the states of system inputs
    xk = xk_initialized
    xk = xk_tolist(xk)

    # break the formula into its components
    formula_list = hf.break_formula(cause_formula)
    formula_components = hf.give_formula_components(formula_list)

    # Initialize the checker:
    stn_viol = STL.SyntaxTreeNode()
    stn_viol.initialize_node(viol_formula.split(), 0)

    # Initialize a number representing the last value where uk was not ck for each formula component's left side
    control_array = np.full((len(formula_list), 1), -1)

    while time <= duration:

        # new uk's free values are determined upon old xk and uk values
        uk_works = False
        free_control_values = copy.deepcopy(uk_crossproduct)
        while not uk_works:
            # set uk randomly from free_control_values
            rand_index = random.randint(0, len(free_control_values)-1)  # very weirdly, random.randint(a,b) can give out b
            uk = list(free_control_values[rand_index])

            j = 0
            while j in range(len(formula_list)):
                # check if left side is satisfied by checking if A 1, b-1 (u=c) is satisfied
                # and if u = c at this randomly generated uk.
                control_input = formula_components[j][0].left_node.metric - xk_count
                control_input_val = formula_components[j][0].left_node.param
                control_input_length = formula_components[j][0].interval.ub + 1  # orjinal formul A 1 1 ise length = 0
                if uk[control_input] == control_input_val and (control_input_length == 0 or time - control_array[j] > control_input_length):
                    # left side is satisfied for A 0 b-2 ( u = c ), check if right formula is satisfied
                    right_side_satisfied = False
                    if formula_components[j][1] == None:
                        right_side_satisfied = True
                    else:
                        copy_stn = copy.deepcopy(formula_components[j][1])
                        copy_stn.compute_qv(STL.DataPoint(value=xk + uk, time=time))
                        if copy_stn.qv > 0:
                            right_side_satisfied = True
                    if right_side_satisfied:
                        break
                j += 1

            if j == len(formula_list):
                uk_works = True
            else:
                free_control_values = hf.safe_remove(free_control_values, tuple(uk))
            if len(free_control_values) == 0:
                print("No possible free control combinations left")
                npml += 1
                rand_index = random.randint(0, len(uk_crossproduct)-1)
                uk = list(uk_crossproduct[rand_index])
                uk_works = True

        # we found a working uk for the corresponding xk
        # update all stns and linked_list values with this uk and xk values
        for i in range(len(formula_list)):
            if formula_components[i][1] is not None:
                formula_components[i][1].compute_qv(STL.DataPoint(value=xk + uk, time=time))
            control_input = formula_components[i][0].left_node.metric - xk_count
            control_input_val = formula_components[i][0].left_node.param
            if not uk[control_input] == control_input_val:
                control_array[i] = time  # en son bu time'da uk[control_input], control_input_val'dan degisikti

        # compute label, write new xk, uk and label to the file
        stn_viol.compute_qv(STL.DataPoint(value=xk + uk, time=time))
        f_s.write("%s %s\n" % (str(time), " ".join([str(x) for x in xk + uk])))
        qual = 0 if stn_viol.qv >= 0 else 1
        f_l.write("%s %s\n" % (str(time), str(qual)))

        # new xk is calculated from this loop's xk and uk values
        if num_to_let:
            uk_letters = ['a' if x == 0 else 'b' for x in uk]
            xk, _ = step_function(xk, uk_letters)
        else:
            xk, _ = step_function(xk, uk)

        xk = xk_tolist(xk)

        time += 1


    f_s.close()
    f_l.close()
    print("Done %d" % tc)
    tc += 1

  print("There were no possible modes left for a controller input for " + str(npml) + " times.")