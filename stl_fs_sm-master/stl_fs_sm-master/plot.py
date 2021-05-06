
import numpy as np
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import sys


import scipy.io

if sys.platform == 'darwin':
  import matplotlib
  matplotlib.use("TkAgg")
  import matplotlib.pyplot as plt
else:
  import matplotlib.pyplot as plt


def show():
  plt.show()

def title(t):
  plt.title(t)

def save(file_name):
  fig = plt.gcf()
  if file_name:
    fig.savefig(file_name, dpi=400)

def plot_all(signal_files, label_files):
  if isinstance(signal_files, list):
    for i in range(len(signal_files)):
      plot(signal_files[i], label_files[i], i)
  else:
    plot(signal_files, label_files)

  plt.show()


def plot_with_evaluation(signal, label, ts = None, ind=1, evaluation=None, binary_evaluation=None, th_list=None):
  plt.rcParams["figure.figsize"] = (12, 3)

  plot_helper(signal, label, ts, tl=ts, ind=ind, binary_evaluation=binary_evaluation, evaluation=evaluation, th_list=th_list)
  #if evaluation:
  #  plt.plot(evaluation, lw=2)





def plot(signal_file_name, label_file_name, ind=1):

  ts, s = read_into_arrays(signal_file_name)
  tl, l = read_into_arrays(label_file_name)
  plot_helper(s, l, ts, tl, ind)

def plot_helper(signal, label, ts=None, tl=None, ind=1, binary_evaluation=None, evaluation=None, th_list=None):
  mx = max(max(signal))

  for i in range(len(label)):
    label[i] = label[i][0]*mx*1.2

  if binary_evaluation:
    for i in range(len(binary_evaluation)):
      binary_evaluation[i] = binary_evaluation[i] * (mx-1) * 1.2

  plt.figure(ind)
  signal_legend = ['signal']
  if ts:
    if len(signal[0]) == 1:
      # plt.plot(ts, signal)
      plt.step(ts, signal)
    else:
      transpose_signal = list(zip(*signal))
      metric_count = len(transpose_signal)
      signal_legend = []

      for x in range(metric_count):
        # plt.plot(ts, transpose_signal[x])
        # plt.step(ts, transpose_signal[x])
        # signal_legend.append(str("signal_" + str(x)))
        # Delete the following part:
        if x==0:
          plt.step(ts, [20*y for y in transpose_signal[x]])
          signal_legend.append('p (scaled)')
        else:
          plt.step(ts, transpose_signal[x])
          signal_legend.append('r')
  else:
    # plt.plot(signal)
    plt.step(signal)
  if tl:
    # plt.plot(tl, label, lw=2)
    plt.step(tl, label, lw=2)
  else:
    # plt.plot(label)
    plt.step(label)

  if binary_evaluation:
    if ts:
      # plt.plot(ts, binary_evaluation)
      plt.step(ts, binary_evaluation)
    else:
      # plt.plot(binary_evaluation)
      plt.step(binary_evaluation)

  if evaluation:
    if ts:
      # plt.plot(ts, evaluation)
      plt.step(ts, evaluation)
    else:
      # plt.plot(evaluation)
      plt.step(evaluation)

  xl = len(signal)
  if ts:
    xl=ts[-1]
  t = [0, xl]
  if th_list:
    for x in th_list:
      l = [x, x]
      plt.plot(t, l, '--')

  plt.xlim(t)
  plt.legend(signal_legend + [ "label", "qualitative", "quantitative"], loc='upper left', fontsize=16)
  plt.tick_params(axis='both', which='major', labelsize=16)


def read_into_arrays(file_name):
  f = open(file_name, 'r')
  t = []
  s = []
  for l in f:
    ls = l.split()
    t.append(int(ls[0]))
    s.append([float(x) for x  in ls[1:]])
  return t,s


def convert_save_results(params, param_lists, all_results, file_name, formula, time_passed, trace_count, thread_count,
                         opt_valuation, opt_params):

  s = list(map(len, param_lists))
  r = dict()
  for i in range(len(params)):
    r[params[i]] = np.reshape([t[1][i] for t in all_results], s)

  r['val'] = np.reshape([t[0] for t in all_results], s)
  r['parameter_list'] = params
  r['parameter_domain'] = param_lists
  r['formula'] = formula
  r['time_passed'] = time_passed
  r['trace_count'] = trace_count
  r['thread_count'] = thread_count
  r['opt_valuation'] = opt_valuation
  r['opt_params'] = opt_params


  if file_name:
    scipy.io.savemat(file_name, r)

  return r


def plot_converted_results(results, params):

  if len(params) == 2:
    MZ = np.max(results['val'])
    mZ = np.min(results['val'])

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    # Plot the surface.
    surf = ax.plot_surface(results[params[0]], results[params[1]], results['val'], cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)

    # Customize the z axis.
    ax.set_zlim(mZ * 0.9, MZ * 1.1)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    # Add a color bar which maps values to colors.
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.show()

def plot_sample_figure():
  fs = 24
  lw = 2

  fig_size = [10,3.2]
  folder_name="paper_plots/"
  ts = [0, 1,4,5, 7]
  x = [2,4,3,1, 1]

  ts = [0, 1,4,5]
  x = [2,4,3,3]


  plt.figure(0, figsize=fig_size)
  xline, = plt.plot(ts, x, drawstyle='steps-post', label='x', linewidth=lw)
  plt.plot(ts[0:len(ts)-1], x[0:len(ts)-1], 's')


  tsy = [0, 2,5]
  y = [3,2,2]


  plt.xlim([0,5])
  yline, = plt.plot(tsy, y, drawstyle='steps-post', label='y',linewidth=lw)
  plt.plot(tsy[0:len(tsy)-1], y[0:len(tsy)-1], 's')
  plt.legend(handles=[xline, yline], fontsize=fs)
  plt.tick_params(axis='both', which='major', labelsize=fs)

  fig = plt.gcf()
  fig.savefig(folder_name + "signal_file", dpi=400)


  le = len(ts)-1
  x1 = [3 - xx for xx in x ]
  x2 = [xx - 2 for xx in x ]


  plt.figure(1, figsize=fig_size)
  x1line, = plt.plot(ts, x1, drawstyle='steps-post', label='x < 3',linewidth=lw)
  # x2line, = plt.plot(ts, x2, drawstyle='steps-post', label='x > 2')
  # plt.plot(ts[0:le], zip(x1[0:le],x2[0:le]),'s')
  plt.xlim([0, 5])

  print(ts)
  print(x1)
  print(x2)

  # plt.figure(2, figsize=fig_size)
  Fx = [1,-1,0,2,2]
  Fxt = [0, 3,4,5,7]

  Fx = [1,-1,0,0]
  Fxt = [0, 3,4,5]
  fxline, = plt.plot(Fxt, Fx, drawstyle='steps-post', linestyle='--',label='F [0 2] x < 3',linewidth=lw)
  plt.legend(handles=[x1line,fxline],  fontsize=fs)
  plt.xlim([0,5])
  plt.tick_params(axis='both', which='major', labelsize=fs)

  fig = plt.gcf()
  fig.savefig(folder_name + "evaluation", dpi=400)


  EM = 0
  exp_time = [EM, EM, 3, 3,]
  exp_time_t = [0, 1, 1, 3, 5]
  exp_time = [EM, EM, 2, 0, 0]

  plt.figure(2, figsize=fig_size)
  plt.plot(exp_time_t, exp_time,linewidth=lw)
  plt.xlim([0,5])
  plt.ylim([0,3])
  plt.legend(['t - exp'], fontsize=fs)
  plt.tick_params(axis='both', which='major', labelsize=fs)

  fig = plt.gcf()
  fig.savefig(folder_name + "time", dpi=400)
  plt.show()
  # orx = [1,2,2,2, 1, 2, 2, 2]
  # or_ts = range(0,8)
  # orline, = plt.plot(or_ts, orx, drawstyle='steps-post', label='x > 2 or F [0 2] x < 3',linestyle='--')

  # plt.legend(handles=[fxline,orline])

  return

  tf = [0,1,3,4,5,5,7]
  xf = [1,1,1,-1,0,2,2]
  plt.plot(tf,xf, drawstyle='steps-post')
  plt.plot(tf[0:len(ts)-1], xf[1:len(ts)],  's')


  plt.xlim([0,7])
  plt.ylim([-2,5])
  plt.legend(['x < 5', 'x < 3'])
  fig = plt.gcf()
  #fig.savefig(folder_name + "signal_less_than", dpi=400)

  plt.show()
  return



def plot_results(param_lists, all_results):
  if len(param_lists) > 2:
    print('Plotting is not supported for more than 2 optimization parameters')

  if len(param_lists) == 2:
    return plot_results3D(len(param_lists[0]), len(param_lists[1]), all_results)

  if len(param_lists) == 1:
    return plot_results2D()


def plot_results3D(p1, p2, results):
  X = np.array(p1)
  Y = np.array(p2)
  X2, Y2 = np.meshgrid(X, Y)

  X = np.reshape([r[1][0] for r in results], (p1, p2) )
  Y = np.reshape([r[1][1] for r in results], (p1, p2) )
  Z = np.reshape([r[0] for r in results], (p1, p2) )

  MZ = np.max(Z)
  mZ = np.min(Z)

  fig = plt.figure()
  ax = fig.gca(projection='3d')
  # Plot the surface.
  surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                         linewidth=0, antialiased=False)

  # Customize the z axis.
  ax.set_zlim(mZ*0.9, MZ*1.1)
 # ax.zaxis.set_major_locator(LinearLocator(10))
 # ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

  # Add a color bar which maps values to colors.
  fig.colorbar(surf, shrink=0.5, aspect=5)

  plt.show()




def plot_results2D():
  print('what?')