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
    pylab.plt.plot(views, yp, color='grey')



    print 'done.'
