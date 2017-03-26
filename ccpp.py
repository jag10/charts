# -*- coding: utf-8 -*-
# python 2.7, python3.5
import matplotlib.pyplot as plt
import numpy as np

def draw_v_line(plt, x_point, y1, y2, min_value, max_value):
    plt.plot([x_point, x_point], [y1, y2], 'k-', lw = 2)
    plt.text(x_point, y1, min_value, fontsize=15)
    plt.text(x_point, y2, max_value, fontsize=15)

def normalize_data(data):
    # NORMALIZATION
    max_value = list(map(max,np.transpose(data)))
    min_value = list(map(min,np.transpose(data)))
    for row in data:
        i = 0
        for v in row:
            normalized_val = 100 * (v - min_value[i]) / (max_value[i] - min_value[i])
            row[i] = normalized_val
            i = i + 1
    return data

def ccpp(plt, data, ticks, labels, names):
    # plot normalized data
    max_value = list(map(max,np.transpose(data)))
    min_value = list(map(min,np.transpose(data)))
    data = normalize_data(data)
    i = 0
    for row in data:
        plt.plot(ticks, row, linewidth=2, label = names[i])
        i = i + 1


    ax = plt.gca()
    ax.axes.get_xaxis().set_ticklabels(labels)
    ax.axes.get_yaxis().set_ticklabels([])
    y1 = ax.get_ylim()[0]
    y2 = ax.get_ylim()[1]
    # draw vertical axes
    j = 0
    for value in ticks:
        draw_v_line(plt, value, y1, y2, min_value[j], max_value[j])
        j += 1

    # Shrink current axis's height by 10% on the bottom
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.2,
                 box.width, box.height * 0.8])

    # Put a legend below current axis, 2 columns
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=2)

    plt.show()

############################ MAIN CODE #########################

ccpp_attributes = 100*np.round(np.random.rand(7,7), 2);

names = ['example1', 'example2','example3','example4','example5','example6','example7']

# print ccpp_attributes
ticklabels=['none','attr1', u'attr2', u'attr3', u'attr4', u'attr5', u'attr6', u'attr7']
ticks=[0,2,4,6,8,10, 12]
ccpp(plt, ccpp_attributes, ticks, ticklabels, names)
