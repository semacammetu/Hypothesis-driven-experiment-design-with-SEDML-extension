import matplotlib.pyplot as plt
from matplotlib import gridspec

from cause_mining_algo import cause_mining_heuristic
from trace_checker import STL
from . import traffic_example as te

#from . import SPA


def print_detailed_result(prefix, formula, folder_name, signal_file_base, signal_file_rest, trace_count):
    """

    Args:
        prefix: (bool) 1 if formula given is prefix, 0 if its infix
        formula: STL formula

    Returns: nothing

    """
    if prefix:
        infix_formula = STL.prefix_to_infix(formula)
    else:
        infix_formula = formula

    fp_fn_tp_tn = cause_mining_heuristic.cause_mining_print_detailed_result(infix_formula, folder_name, signal_file_base,
                                                                            trace_count, signal_file_rest)
    return fp_fn_tp_tn

def plot_func():
    """
    The plotting function for the paper
    """
    linewidth_labels = 12
    linewidth_states = 3
    font_size1 = 32
    font_size_legend = 23
    u0_place = 1.5 # u0_place and u1_place are arranged to arrange the distance between two marks in the second plot.
    u1_place = 0.8
    font_size_fig1_y_ax = 26
    font_size_fig1_x_ax = 26
    font_size_fig2_y_ax = 15
    font_size_fig2_x_ax = 15

    # It will show the data point between time = ll and time = ul
    ll = 0          # lower limit
    ul = 50          # upper limit

    signal_file_name = 'test_data/traffic_data/plot-folder/test_sabit_test_0'
    label_file_name = signal_file_name + '_label'
    formula_label_file_name = signal_file_name +'_cause_formula_label'
    x0 = []
    x1 = []
    x2 = []
    x3 = []
    x4 = []
    u0 = []
    u1 = []
    label = []
    formula_label1 = []
    formula_label = []

    with open(signal_file_name, 'r') as sf, open(label_file_name, 'r') as lf, open(formula_label_file_name, 'r') as clf:
            for ts, tl, tcl in zip(sf, lf, clf):
                s = ts.split()
                t = int(s[0])
                x0.append(float(s[1]))
                x1.append(float(s[2]))
                x2.append(float(s[3]))
                x3.append(float(s[4]))
                x4.append(float(s[5]))
                u0.append(float(s[6]))
                u1.append(float(s[7]))
                _, l = tl.split()
                _, cl = tcl.split()
                label.append(int(l))
                formula_label1.append(int(cl))
                #formula_label = [None if formula_label1[i]==0 else float(1.05) for i in xrange(ll,ul)]
                #if t <= 2:
                #    formula_label.append(None)
                #else:
                #    if ((int(u1[t-1]) == 0 and int(u1[t-2]) == 0 and int(u1[t]) == 0 and float(x4[t-1]) > 10) or
                #            (int(u0[t-1]) == 0 and int(u0[t-2]) == 0 and int(u0[t]) == 0 and float(x3[t-1]) > 10)):
                #        formula_label.append(float(1.05))
                #    else:
                #        formula_label.append(None)

    for i in range(ll, ul):
        if formula_label1[i] == 1:
            formula_label.append(float(1.05))
        else:
            formula_label.append(None)

    max_val = max(x0+x1+x2+x3+x4)*1.3

    t = [i for i in range(ll, ul, 1)]
    label = [None if label[i] == 0 else max_val for i in range(ll, ul)]
    neg_label = [None if not label[i] == None else max_val for i in range(ll, ul)]
    neg_formula_label = [None if not formula_label[i] == None else 1.1*max_val for i in range(ll, ul)]
    formula_label = [None if formula_label[i] == None else 1.1*max_val for i in range(ll, ul)]

    dashed_line_1 = [max_val for i in range(ll,ul)]
    dashed_line_2 = [max_val*1.1 for i in range(ll,ul)]




    #           PLOT

    fig = plt.figure(tight_layout=True,figsize=(18, 6.15))
    #fig.figure()

    gs = gridspec.GridSpec(15, 15)

    #      1st plot

    ax = fig.add_subplot(gs[0:11, :])
    ax.set_ylabel('$state$', fontsize=font_size1)
    ax.set_xlabel('$time (k)$', fontsize=font_size1)
    #ax1 = fig.gca()
    #ax1.xaxis.set_label_coords(0.5, 1.3)
    ax.set_yticklabels(['$0$', '$10$', '$20$', '$30$', '$40$'],fontsize=font_size_fig1_y_ax)
    ax.set_xticklabels(['$0$', '$10$', '$20$', '$30$', '$40$', '$50$'],fontsize=font_size_fig1_x_ax)
    ax.set_ylim(0, 63)

    ax.plot(t, label[ll:ul], '-',color='#4C9900', linewidth=linewidth_labels, label='$l = 1$')
    ax.plot(t, formula_label[ll:ul], '-', color='#33FF33', linewidth=linewidth_labels, label='$\Phi(v)^*$')

    ax.plot(t, x0[ll:ul], label='$x^0$', alpha=0.5, linewidth=linewidth_states)
    ax.plot(t, x1[ll:ul], label='$x^1$', alpha=0.5, linewidth=linewidth_states)
    ax.plot(t, x2[ll:ul], label='$x^2$', alpha=0.5, linewidth=linewidth_states)
    ax.plot(t, x3[ll:ul], label='$x^3$', alpha=0.5, linewidth=linewidth_states)
    ax.plot(t, x4[ll:ul], label='$x^4$', alpha=0.5, linewidth=linewidth_states)
    ax.plot(t, dashed_line_1, '--', alpha=0.3, color='#708090')
    ax.plot(t, dashed_line_2, '--', alpha=0.3, color='#708090')

    ax.legend(loc='center left', shadow=True, fontsize=font_size_legend)



    u0_original = u0
    u1_original = u1

    u0 = [None if u0[i] == 0 else u0_place for i in range(ll, ul)]
    neg_u0 = [None if not u0[i] == None else 0 for i in range(ll, ul)]
    u1 = [None if u1[i] == 0 else u1_place for i in range(ll, ul)]
    neg_u1 = [None if not u1[i] == None else 0 for i in range(ll, ul)]



    #   2nd plot
    ax = fig.add_subplot(gs[12:,: ])
    ax.set_ylabel('$control$', fontsize=font_size1)
    #ax.set_xlabel('$Time (k)$', fontsize=font_size1)
    ax.set_yticklabels([], fontsize=font_size_fig1_y_ax)
    ax.set_xticklabels([], fontsize=font_size_fig2_x_ax)

    plt.plot(t, u0[ll:ul], 'b-', linewidth=27.9,label='$u^0$', alpha=1)
    plt.plot(t, u1[ll:ul], 'r-',linewidth=27.9,label='$u^1$', alpha=1)

    plt.show()


def cause_mining_main():

    #ll.linked_list_main()
    te.traffic_example_main()
    #    bem.basic_example_main()
    #tem.toy_example_main()
    # SPA.SPA_main()
    #plot_func()
