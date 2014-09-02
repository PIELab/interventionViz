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
    cmap       = pylab.cm.get_cmap(name='brg')
    pltName = 'participants\' PA for all sedentary & active avatar days'
    print 'making plot "' + pltName + '"'
    pylab.figure(pltName)
    pylab.plt.ylabel('step counts')
    pylab.plt.xlabel('<-sedentary                                      active->\navatar behavior')
    pylab.plt.gca().axes.get_xaxis().set_ticks([])
    pylab.plt.draw()

    activePAs = list()
    sedentPAs = list()
    zeroPAs = list()
    pNum = 0
    base = [0, 0, 0]  # base of graph indexed by view_ts values [0, 1, -1]... like base[0], base[1], base[-1]... get it?
    for sub in data:
        active = sed = zer = 0
        a_count = s_count = z_count = 0

        fb_ts = sub.fitbit_data.get_day_ts(start=sub.meta_data.start, end=sub.meta_data.end)
        view_ts = sub.avatar_view_data.get_day_type_ts(start=sub.meta_data.start, end=sub.meta_data.end)

        for i in range(len(fb_ts)):
            pylab.plt.bar(view_ts[i], fb_ts[i], bottom=base[view_ts[i]], linewidth=1, width=.9,
                          color=cmap(float(pNum) / float(len(data))))
            base[view_ts[i]] += fb_ts[i]

            if view_ts[i] > 0:
                active += fb_ts[i]
                a_count += 1
            elif view_ts[i] < 0:
                sed += fb_ts[i]
                s_count += 1
            else:
                zer += fb_ts[i]
                z_count += 1

        if a_count != 0:
            activePAs.append(active / a_count)
        else:
            assert active == 0
            activePAs.append(0)
        if s_count != 0:
            sedentPAs.append(sed / s_count)
        else:
            assert sed == 0
            sedentPAs.append(0)
        if z_count != 0:
            zeroPAs.append(zer / z_count)
        else:
            assert zer == 0
            zeroPAs.append(0)

        if a_count + s_count + z_count == 0:
            warnings.warn('subject has no active, passive, or zero days!')
        elif a_count + s_count == 0:
            warnings.warn('subject contains only zero days!')
        pNum += 1

    pltName = 'participants\' avg PA for sedentary & active avatar days'
    print 'making plot "' + pltName + '"'
    pylab.figure(pltName)
    pylab.plt.ylabel('average step counts')
    pylab.plt.xlabel('<-sedentary                                      active->\navatar behavior')
    pylab.plt.gca().axes.get_xaxis().set_ticks([])
    pylab.plt.draw()
    base = count = 0
    for PA in activePAs:
        pylab.plt.bar(1, PA, bottom=base, linewidth=1, width=.9, color=cmap(float(count)/float(len(data))))
        base += PA
        count += 1
    base = count = 0
    for PA in sedentPAs:
        pylab.plt.bar(-1, PA, bottom=base, linewidth=1, width=.9, color=cmap(float(count)/float(len(data))))
        base += PA
        count += 1
    base = count = 0
    for PA in zeroPAs:
        pylab.plt.bar(0, PA, bottom=base, linewidth=1, width=.9, color=cmap(float(count)/float(len(data))))
        base += PA
        count += 1

    paired_sample = stats.ttest_rel(sedentPAs, activePAs)
    print "================================================"
    print str(len(data)) + " subjects analyzed using fitbit data."
    print "The t-statistic is %.3f and the p-value is %.3f." % paired_sample
    print "================================================"
    
    print 'done.'
