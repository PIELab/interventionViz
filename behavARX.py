import pylab
import warnings
import numpy as np
from scipy import stats
import pandas
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.graphics.api import qqplot

from src.settings import setup, QUALITY_LEVEL, DATA_TYPES

import src.day_step_compare as day_step_compare
from src.post_view_event_steps_bars import plot_minutes, PLOT_TYPES, plot_difference

import knowMe

#knowMe.makePlots(type=PLOT_TYPES.bars, show=True, pre_win=10, post_win=40)
#knowMe.makePlots(type=PLOT_TYPES.bars, show=True)

# knowMe.makePlot(type=PLOT_TYPES.bars)
# pylab.show()

# # plot participant averages & global average response (lines)
# # knowMe
# print 'knowMe lines...'
# knowMe.makePlot(type=PLOT_TYPES.lines, selected_data='int_acc_cnts', smooth=7)
# pylab.show()
#
# # plot stackGraphs of event response
# # knowMe
# print 'knowMe stackPlot...'
# knowMe.makePlot(type=PLOT_TYPES.bars)
# pylab.show()


# re-creation of
#   http://statsmodels.sourceforge.net/devel/examples/notebooks/generated/tsa_arma.html

FIG_DIR = 'sampleOutputs/behavARX/'

def loadSampleData(pid, filterOutliers=False):
    # print sm.datasets.sunspots.NOTE
    #
    # dta = sm.datasets.sunspots.load_pandas().data
    #
    # dta.index = pandas.Index(sm.tsa.datetools.dates_from_range('1700', '2008'))
    # del dta["YEAR"]

    OUTPUT_INDEX = 16 # 27=HeartRate 16=Accelerometry
    data = knowMe.load_arx_model_data('./data/knowMeData.sav', OUTPUT_INDEX)
    from knowMe import columnHeader as dataColumns
    INPUT_INDEX = 28
    OUTPUT_KEY = dataColumns[OUTPUT_INDEX]
    INPUT_KEY = dataColumns[INPUT_INDEX]
    # print data
    dat = data[pid]
    indices = pandas.DatetimeIndex(dat['datetime'])#pandas.date_range('1/1/2012', freq='Min', periods=len(dat[OUTPUT_KEY]))
    # print dat
    # print indices
    dta = pandas.DataFrame(
        data=dat[OUTPUT_KEY],
        columns=[OUTPUT_KEY],
        index=indices
    )
    interven = pandas.DataFrame(
        data=dat[INPUT_KEY],
        columns=[OUTPUT_KEY],
        index=indices
    )

    if filterOutliers:
        # filter outliers:
        # print dta
        dataFrame = dta.copy()
        statBefore = pandas.DataFrame({
            'q1': dataFrame[OUTPUT_KEY].quantile(.25),
            'median': dataFrame[OUTPUT_KEY].median(),
            'q3' : dataFrame[OUTPUT_KEY].quantile(.75),
            'temp' : [0]
        })

        def is_outlier(row):
            iq_range = statBefore['q3'] - statBefore['q1']
            median = statBefore['median']
            # print str((row[OUTPUT_KEY] > (median + (1.5* iq_range)))[0]) + '\r'
            if (row[OUTPUT_KEY] > (median + (1.5* iq_range)))[0] \
            or (row[OUTPUT_KEY] < (median - (1.5* iq_range)))[0]:
                return True
            else:
                return False

        #apply the function to the original df:
        dataFrame.loc[:, 'outlier'] = dataFrame.apply(is_outlier, axis = 1)
        #filter to only non-outliers:
        dta_no_outliers = dta[~(dataFrame.outlier)]
        interven_no_outliers = interven[~(dataFrame.outlier)]
    else:
        dta_no_outliers = dta
        interven_no_outliers = interven



    plt.subplot(211)
    # dta.plot(figsize=(12,8))
    plt.plot(dta_no_outliers, label='out ('+str(OUTPUT_KEY)+')')
    plt.subplot(212)
    plt.plot(interven_no_outliers, label='in1 ('+str(INPUT_KEY)+')')
    plt.savefig(FIG_DIR+'dataView'+str(pid)+'.png', bbox_inches='tight')
    # plt.show()

    return dta_no_outliers, interven_no_outliers

def seasonalDecompose(data, saveFigName=None):
    from statsmodels.tsa.seasonal import seasonal_decompose
    seasonLen = 60*24 # expected season length [min]
    dataResolution = 1 # [min]
    decompfreq = seasonLen/dataResolution
    decomposition = seasonal_decompose(data.values, freq=decompfreq)

    trend = decomposition.trend
    seasonal = decomposition.seasonal
    residual = decomposition.resid

    plt.subplot(411)
    plt.plot(data, label='Original')
    plt.legend(loc='best')
    plt.subplot(412)
    plt.plot(trend, label='Trend')
    plt.legend(loc='best')
    plt.subplot(413)
    plt.plot(seasonal,label='Seasonality')
    plt.legend(loc='best')
    plt.subplot(414)
    plt.plot(residual, label='Residuals')
    plt.legend(loc='best')
    plt.tight_layout()
    if (saveFigName == None):
        plt.show()
    else:
        plt.savefig(FIG_DIR+str(saveFigName))

def plotCCF(dta, exog, saveFigName, **kwargs):
    zoomLagView = 120   # max lag of interest (for zoomed view)

    kwargs.setdefault('marker', 'o')
    kwargs.setdefault('markersize', 5)
    kwargs.setdefault('linestyle', 'None')

    fig = plt.figure(figsize=(12,8))
    ax1=fig.add_subplot(211)

    ax1.set_ylabel('CCF')
    ax1.set_xlabel('lag?')
    # print dta

    print 'SIZES:',len(dta.values.squeeze()), ',', len(exog.values.squeeze())

    ccf_x = sm.tsa.ccf(dta.values.squeeze(), exog.values.squeeze())
    ax1.plot(range(1,len(ccf_x)+1), ccf_x, **kwargs)

    ax2=fig.add_subplot(212)
    ax2.plot(range(1,zoomLagView+1), ccf_x[:zoomLagView], **kwargs)

    if (saveFigName==None):
        plt.show()
    else:
        plt.savefig(FIG_DIR+str(saveFigName), bbox_inches='tight')

def plotACFAndPACF(dta, saveFigName=None):
    fig = plt.figure(figsize=(12,8))
    ax1 = fig.add_subplot(211)
    # squeeze = Remove single-dimensional entries from the shape of an array.
    # Plots lags on the horizontal and the correlations on vertical axis
    ax1.set_ylabel('correlation')
    ax1.set_xlabel('lag')
    fig = sm.graphics.tsa.plot_acf(dta.values.squeeze(), lags=40, ax=ax1)

    # partial act
    # Plots lags on the horizontal and the correlations on vertical axis
    ax2 = fig.add_subplot(212)
    ax1.set_ylabel('correlation')
    ax1.set_xlabel('lag')
    fig = sm.graphics.tsa.plot_pacf(dta, lags=40, ax=ax2)

    if (saveFigName==None):
        plt.show()
    else:
        plt.savefig(FIG_DIR+str(saveFigName), bbox_inches='tight')

def fitModel(dta, interven):
    # NOTE: can set exog=[] to set exogeneous variables
    # model20 = sm.tsa.ARMA(dta, (2,0), exog=interven)
    # arma_mod20 = model20.fit()
    # print arma_mod20.params

    model30 = sm.tsa.ARMA(dta, (1,0,0), exog=interven)
    arma_mod30 = model30.fit()
    # print arma_mod20.aic, arma_mod20.bic, arma_mod20.hqic
    print '=== MODEL PARAMS ==='
    print arma_mod30.params

    print 'AIC, BIC, HQIC:'
    print arma_mod30.aic, arma_mod30.bic, arma_mod30.hqic

    return arma_mod30

def testModelFit(arma_mod30, dta, pid):
    # does our model fit the theory?
    residuals = arma_mod30.resid
    sm.stats.durbin_watson(residuals.values)
    # NOTE: Durbin Watson Test Statistic approximately equal to 2*(1-r)
    #       where r is the sample autocorrelation of the residuals.
    #       Thus, for r == 0, indicating no serial correlation,
    #       the test statistic equals 2. This statistic will always be
    #       between 0 and 4. The closer to 0 the statistic, the more evidence
    #       for positive serial correlation. The closer to 4, the more evidence
    #       for negative serial correlation.

    # plot the residuals so we can see if there are any areas in time which
    # are poorly explained.
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111)
    ax = arma_mod30.resid.plot(ax=ax);

    plt.savefig(FIG_DIR+'residualsVsTime'+str(pid)+'.png', bbox_inches='tight')
#    plt.show()

    # tests if samples are different from normal dist.
    k2, p = stats.normaltest(residuals)
    print ("residuals skew (k2):" + str(k2) +
           " fit w/ normal dist (p-value): " + str(p))

    # plot residuals
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(211)
    fig = qqplot(residuals, line='q', ax=ax, fit=True)

    ax2 = fig.add_subplot(212)
    # resid_dev = residuals.resid_deviance.copy()
    # resid_std = (resid_dev - resid_dev.mean()) / resid_dev.std()
    plt.hist(residuals, bins=25);
    plt.title('Histogram of standardized deviance residuals');
    plt.savefig(FIG_DIR+'residualsNormality'+str(pid)+'.png', bbox_inches='tight')

    # plot ACF/PACF for residuals
    plotACFAndPACF(residuals, 'residualsACFAndPACF'+str(pid)+'.png')

    r,q,p = sm.tsa.acf(residuals.values.squeeze(), qstat=True)
    data = np.c_[range(1,41), r[1:], q, p]
    table = pandas.DataFrame(data, columns=['lag', "AC", "Q", "Prob(>Q)"])
    # print table.set_index('lag')

    # sample data indicates a lack of fit.


def testDynamicPrediction(arma_mod30, dta, interven, pid):
    tf = len(dta)
    t0 = tf*2/3
    predict_sunspots = arma_mod30.predict(t0, tf, exog=interven, dynamic=True)
    # print predict_sunspots

    ax = dta.ix['2012':].plot(figsize=(12,8))
    ax = predict_sunspots.plot(ax=ax, style='r--', label='Dynamic Prediction');
    ax.legend();
    # ax.axis((-20.0, 38.0, -4.0, 200.0));
    plt.savefig(FIG_DIR+'dynamicPrediction'+str(pid)+'.png', bbox_inches='tight')

    def mean_forecast_err(y, yhat):
        return y.sub(yhat).mean()

    # mf_err = mean_forecast_err(dta.SUNACTIVITY, predict_sunspots)

    # print ('mean forcast err: ' + str(mf_err))

def behavARX(pid):
    print '\n\n=== PID # ' + str(pid) + ' ==='
    [dta, interven] = loadSampleData(pid)
    plotCCF(dta, interven, 'CCF'+str(pid)+'.png')
    seasonalDecompose(dta, 'seasonalDecomposition'+str(pid)+'.png')
    plotACFAndPACF(dta, 'acf_and_pacf'+str(pid)+'.png')
    arma_mod30 = fitModel(dta, interven)
    testModelFit(arma_mod30, dta, pid)
    testDynamicPrediction(arma_mod30, dta, interven, pid)
    # more example methods @:


if __name__ == '__main__':
    for pid in [9, 10, 11, 13, 19, 22, 23, 32, 35]:  # 21 exlcuded
        behavARX(pid)
    # more example methods @:
    # Simulated ARMA(4,1): Model Identification is Difficult
