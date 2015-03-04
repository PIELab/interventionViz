# -*- coding: utf-8 -*-

import pylab # for plotting commands & array
from scipy import stats
import warnings


def plot(data):
    # change plot font
#    font = {'family' : 'monospace',
#            'weight' : 'normal',
#            'size'   : 16}
#    pylab.plt.rc('font', **font)
    cmap = pylab.cm.get_cmap(name='spectral')
    pltName = 'PA vs interaction'
    print 'making plot "' + pltName + '"'
    pylab.figure(pltName)
    pylab.plt.ylabel('step count')
    pylab.plt.xlabel('(s active avatar exposure) - (s sedentary avatar exposure)')
    pylab.plt.draw()

    fitbits = list()
    views = list()

    pos_view = list()  # list of positively sloped avatar view points
    neg_view = list()
    pos_fb = list()  # fitbit
    neg_fb = list()
    pos_line = list()  # list of lines to accompany points
    neg_line = list()
    pNum = 0
    for sub in data:  # graph & fit individually
        pNum += 1

        fb_ts = sub.fitbit_data.get_day_ts(start=sub.meta_data.start, end=sub.meta_data.end)
        view_ts = sub.avatar_view_data.get_day_ts_score(start=sub.meta_data.start, end=sub.meta_data.end)

        for i in range(len(fb_ts)):  # for each data point (1 day)
            pylab.plt.scatter(view_ts[i], fb_ts[i], color=cmap(float(pNum) / float(len(data))))

        # fit a line to the data
        deg = 1  # degree of the polynomial
        m, b = pylab.polyfit(view_ts, fb_ts, deg)
        yp = pylab.polyval([m, b], view_ts)
        pylab.plt.plot(view_ts, yp, color=cmap(float(pNum) / float(len(data))))

        # make lists of postive & negative points and lines so they can be graphed separately:
        if m >= 0:
            pos_view.append(view_ts)
            pos_fb.append(fb_ts)
            pos_line.append(yp)
        else:
            neg_view.append(view_ts)
            neg_fb.append(fb_ts)
            neg_line.append(yp)

    ### Make plots with +/- separate ###
    pylab.figure('+ slope PA versus interaction')
    pylab.plt.ylabel('step count')
    pylab.plt.xlabel('(s active avatar exposure) - (s sedentary avatar exposure)')
    pylab.plt.draw()
    for p_num in range(len(pos_view)):
        # plot the points
        for i in range(len(pos_view[p_num])):  # for each data point (1 day)
            pylab.plt.scatter(pos_view[p_num][i], pos_fb[p_num][i], color=cmap(float(p_num) / float(len(data))))
        # plot the line
        pylab.plt.plot(pos_view[p_num], pos_line[p_num], color=cmap(float(p_num) / float(len(data))))

    n_pos = len(pos_line)  # count of positive participants already plotted (for shifting the color)
    pylab.figure('- slope PA versus interaction')
    pylab.plt.ylabel('step count')
    pylab.plt.xlabel('(s active avatar exposure) - (s sedentary avatar exposure)')
    pylab.plt.draw()
    for p_num in range(len(neg_view)):
        # plot the points
        for i in range(len(neg_view[p_num])):  # for each data point (1 day)
            pylab.plt.scatter(neg_view[p_num][i], neg_fb[p_num][i], color=cmap(float(p_num+n_pos) / float(len(data))))
        # plot the line
        pylab.plt.plot(neg_view[p_num], neg_line[p_num], color=cmap(float(p_num+n_pos) / float(len(data))))

    ### Make graph with one line fit to all:
    pylab.figure('PA versus interaction')
    pylab.plt.ylabel('step count')
    pylab.plt.xlabel('(s active avatar exposure) - (s sedentary avatar exposure)')
    pylab.plt.draw()

    pNum = 0
    for sub in data:  # graph & fit all together
        pNum += 1

        fb_ts = sub.fitbit_data.get_day_ts(start=sub.meta_data.start, end=sub.meta_data.end)
        view_ts = sub.avatar_view_data.get_day_ts_score(start=sub.meta_data.start, end=sub.meta_data.end)


        for i in range(len(fb_ts)):  # for each data point (1 day)
            pylab.plt.scatter(view_ts[i], fb_ts[i], color=cmap(float(pNum) / float(len(data))))
            # collect values for all participant analysis
            fitbits.append(fb_ts[i])
            views.append(view_ts[i])

    # fit a line to the data
    deg = 1  # degree of the polynomial
    m, b = pylab.polyfit(views, fitbits, deg)
    yp = pylab.polyval([m, b], views)
    slope, intercept, r_value, p_value, std_err = stats.linregress(views, fitbits)
    print 'linear fit | m:', slope, ' b:', intercept, ' r2:', r_value*r_value, ' p:', p_value, ' stdErr:', std_err
    pylab.plt.plot(views, yp, color='grey')



    print 'done.'
