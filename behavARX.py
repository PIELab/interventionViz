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

def loadSampleData():


    # print sm.datasets.sunspots.NOTE
    #
    # dta = sm.datasets.sunspots.load_pandas().data
    #
    # dta.index = pandas.Index(sm.tsa.datetools.dates_from_range('1700', '2008'))
    # del dta["YEAR"]

    data = knowMe.load_arx_model_data('./data/knowMeData.sav')
    # print data
    pid = 11
    print pid
    dat = data[pid]
    indices = pandas.date_range('1/1/2012', freq='Min', periods=len(dat['int_acc_cnts']))
    print dat
    print indices
    dta = pandas.DataFrame(
        data=dat['int_acc_cnts'],
        index=indices
    )
    interven = pandas.DataFrame(
        data=dat['sms_intervention'],
        index=indices
    )

    dta.plot(figsize=(12,8))

    plt.savefig(FIG_DIR+'dataView.png', bbox_inches='tight')
    # plt.show()

    return dta, interven

def seasonalDecompose(data, saveFigName=None):
    from statsmodels.tsa.seasonal import seasonal_decompose
    seasonLen = 60 #60*24 # expected season length [min]
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

def plot_ccf(x, y, ax=None, lags=None, alpha=.05, use_vlines=True, unbiased=True,
            fft=False, **kwargs):
    """
    Plot the cross-correlation function
    """
    from statsmodels.graphics import utils

    fig, ax = utils.create_mpl_ax(ax)

    if lags is None:
        lags = np.arange(len(x))
        nlags = len(lags) - 1
    else:
        nlags = lags
        lags = np.arange(lags + 1) # +1 for zero lag

    acf_x = sm.tsa.ccf(x, y, unbiased=unbiased)

    if use_vlines:
        ax.vlines(lags, [0], acf_x, **kwargs)
        ax.axhline(**kwargs)

    # center the confidence interval TODO: do in acf?
    # confint = confint - confint.mean(1)[:,None]
    kwargs.setdefault('marker', 'o')
    kwargs.setdefault('markersize', 5)
    kwargs.setdefault('linestyle', 'None')
    ax.margins(.05)
    ax.plot(lags, acf_x[:nlags+1], **kwargs)
    # ax.fill_between(lags, confint[:,0], confint[:,1], alpha=.25)
    ax.set_title("Cross-correlation")

    return fig

def plotCCF(dta, exog, saveFigName):
    fig = plt.figure(figsize=(12,8))
    ax1=fig.add_subplot(111)

    ax1.set_ylabel('CCF')
    ax1.set_xlabel('lag')
    print 'SIZES:',len(dta.values.squeeze()), ',', len(exog.values.squeeze())
    fig = plot_ccf(dta.values.squeeze(), exog.values.squeeze(), lags=20, ax=ax1)
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

    model30 = sm.tsa.ARMA(dta, (2,1,10), exog=interven)
    arma_mod30 = model30.fit()
    # print arma_mod20.aic, arma_mod20.bic, arma_mod20.hqic
    print '=== MODEL PARAMS ==='
    print arma_mod30.params

    print 'AIC, BIC, HQIC:'
    print arma_mod30.aic, arma_mod30.bic, arma_mod30.hqic

    return arma_mod30

def testModelFit(arma_mod30, dta):
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

    plt.savefig(FIG_DIR+'residualsVsTime.png', bbox_inches='tight')
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
    plt.savefig(FIG_DIR+'residualsNormality.png', bbox_inches='tight')

    # plot ACF/PACF for residuals
    plotACFAndPACF(residuals, 'residualsACFAndPACF.png')

    r,q,p = sm.tsa.acf(residuals.values.squeeze(), qstat=True)
    data = np.c_[range(1,41), r[1:], q, p]
    table = pandas.DataFrame(data, columns=['lag', "AC", "Q", "Prob(>Q)"])
    print table.set_index('lag')

    # sameple data indicates a lack of fit.


def testDynamicPrediction(arma_mod30, dta, interven):
    tf = len(dta)
    t0 = tf*2/3
    predict_sunspots = arma_mod30.predict(t0, tf, exog=interven, dynamic=True)
    print predict_sunspots

    ax = dta.ix['2012':].plot(figsize=(12,8))
    ax = predict_sunspots.plot(ax=ax, style='r--', label='Dynamic Prediction');
    ax.legend();
    # ax.axis((-20.0, 38.0, -4.0, 200.0));
    plt.savefig(FIG_DIR+'dynamicPrediction.png', bbox_inches='tight')

    def mean_forecast_err(y, yhat):
        return y.sub(yhat).mean()

    mf_err = mean_forecast_err(dta.SUNACTIVITY, predict_sunspots)

    print ('mean forcast err: ' + str(mf_err))

if __name__ == '__main__':
    [dta, interven] = loadSampleData()
    plotCCF(dta, interven, 'CCF.png')
    seasonalDecompose(dta, 'seasonalDecomposition.png')
    plotACFAndPACF(dta, 'acf_and_pacf.png')
    arma_mod30 = fitModel(dta, interven)
    testModelFit(arma_mod30, dta)
    testDynamicPrediction(arma_mod30, dta, interven)
    # more example methods @:
    # Simulated ARMA(4,1): Model Identification is Difficult
