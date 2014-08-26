# -*- coding: utf-8 -*-

import pylab # for plotting commands & array
from scipy import stats

from src.dep.PA.PAdata import PAdata, DEFAULT_METHOD
from src.dep.interaction.timeSeries.multicolorBars import interactionData
from src.dep.interaction.score import segmentInteractionIntoDays
from src.dep.PA.score import segmentPAIntoDays,getPAscore_postiveOnly
from src.settings import InputError, HIGHEST_P_NUMBER, setup


def plot(dataset='test',dataLoc = "./data/", paMethod=DEFAULT_METHOD, bypass_data_check=False):
    # change plot font
#    font = {'family' : 'monospace',
#            'weight' : 'normal',
#            'size'   : 16}
#    pylab.plt.rc('font', **font)

    pltName = 'participants\' avg PA for sedentary & active avatar days'
    print 'making plot "'+pltName+'"'
    pylab.figure(pltName)
    cmap       = pylab.cm.get_cmap(name='terrain')

    activePAs = list()
    sedentPAs = list()
    zeroPAs   = list()

    dataCounter = 0 # a count of how many datapoints are used so far (for colormapping and debug)

    for pNum in range(HIGHEST_P_NUMBER+1): #cycle through all participants
        print '===p:'+str(pNum)+'==='
        
        if pNum==1 or pNum==3: 
            print 'skipping p1 & p3 b/c data is incomplete.\n'
            continue
        elif pNum==13:
            print 'skip p13 b/c data needs some massaging.\n'
            continue
        elif pNum==14:
            print 'skip p14 b/c data is incomplete.\n'
            continue
        else:
                
            activePAtotal = sedentPAtotal = zeroPAtotal = 0
            activePAcount = sedentPAcount = zeroPAcount = 0

            try :
                settings = setup(dataset=dataset, dataLoc=dataLoc, subjectN=pNum)

                # load interaction data
                interact = interactionData(settings.getFileName('viewLog'))
                interactScore,interactDate = segmentInteractionIntoDays(interact)

                # load PA data
                PA = PAdata(PAfile=settings.getFileName(paMethod), method=paMethod, timeScale='daily')
                if paMethod == 'mMonitor':
                    PAscore, PAdate = segmentPAIntoDays(PA,PAscoreFunction=getPAscore_postiveOnly)
                elif paMethod == 'fitbit':
                    PAscore = PA.steps
                    PAdate  = PA.time
                else : 
                    raise ValueError('unknown PA method "'+str(paMethod)+'"')

                if not bypass_data_check:
                    trim_data(interactDate, PAdate, interactScore, PAscore)

                interactions = list()
                for iScore in interactScore:
                    if iScore > 0:
                        interactions.append(1)#'active')
                    elif iScore < 0:
                        interactions.append(-1)#'sedentary')
                    else: # iScore = 0
                        interactions.append(0)#'0')


                for day in range(len(PAscore)):
                    #print 'day     ='+str(day)
                    #print 'interact='+str(interactions[day])
                    #print 'PAscore ='+str(PAscore[day])
                    if interactions[day] > 0:
                        activePAtotal+=PAscore[day]
                        activePAcount+=1
                    elif interactions[day] < 0:
                        sedentPAtotal+=PAscore[day]
                        sedentPAcount+=1
                    else: # interactions[day] == 0
                        zeroPAtotal+=PAscore[day]
                        zeroPAcount+=1

                activePAs.append(activePAtotal/activePAcount)
                sedentPAs.append(sedentPAtotal/sedentPAcount)
                try:
                    zeroPAs.append(zeroPAtotal/zeroPAcount)
                except ZeroDivisionError:
                    zeroPAs.append(0)

                # no exceptions means this data was good, increment counter
                dataCounter += 1
                print str(pNum)+' loaded.\n'

            except InputError as e: 
                print e.message
                print 'participant '+str(pNum)+' not valid.\n'
            except IOError as e:
                print e.message
                print 'participant '+str(pNum)+' not found.\n'
            except Warning as w:
                print w.message
                print 'some issues loading participant '+str(pNum)+'; continuing anyway.\n'

    if paMethod == 'mMonitor':
        pylab.plt.ylabel('physical activity score')
    elif paMethod == 'fitbit':
        pylab.plt.ylabel('average step counts')
        
    pylab.plt.xlabel('<-sedentary                                      active->\navatar behavior')
    
    pylab.plt.gca().axes.get_xaxis().set_ticks([])

    pylab.plt.draw()

    print activePAs
    print sedentPAs
    print zeroPAs

    # TODO: colormapping should use dataCounter and actual number of data available (instead of pNum and HIGHEST_P_NUM, respectively)
    base = 0
    for PA in activePAs:
        pylab.plt.bar(1, PA, bottom=base,   linewidth=1, width=1.7) #, color=cmap(float(pNum)/float(HIGHEST_P_NUMBER)) )
        base += PA
    base = 0
    for PA in sedentPAs:
        pylab.plt.bar(-1, PA, bottom=base,   linewidth=1, width=1.7) #, color=cmap(float(pNum)/float(HIGHEST_P_NUMBER)) )
        base += PA
    base = 0
    for PA in zeroPAs:
        pylab.plt.bar(0, PA, bottom=base,   linewidth=1, width=1.7) #, color=cmap(float(pNum)/float(HIGHEST_P_NUMBER)) )
        base += PA

    paired_sample = stats.ttest_rel(sedentPAs, activePAs)
    print "================================================"
    print str(dataCounter) + " subjects analyzed using " + paMethod + " data."
    print "The t-statistic is %.3f and the p-value is %.3f." % paired_sample
    print "================================================"
    
    print 'done.'

def trim_data(interactDate, PAdate, interactScore, PAscore):
    while (interactDate[0].date() != PAdate[0].date()) or (interactDate[-1].date() != PAdate[-1].date()) or (len(interactScore) != len(PAscore)):
        print 'day mismatch: '
        #print 'data is ' + str(len(PAscore)) + 'x' + str(len(interactScore))
        print '\t NAME   \tSTART \t\t\tEND \t\t\tLEN'
        print '\t interact\t'+str(interactDate[0])+'\t'+str(interactDate[-1])+'\t'+str(len(interactScore))

        print '\t PA     \t'+str(PAdate[0])+      '\t'+str(PAdate[-1])      +'\t'+str(len(PAscore))+'\n'
        if(PAdate[0].date() < interactDate[0].date()):#if pa starts before interact
            print 'pa data removed from start'
            PAdate.pop(0)
            PAscore.pop(0)
        elif PAdate[0].date() > interactDate[0].date():#if pa starts after interact
            print 'interact data removed from start'
            interactDate.pop(0)
            interactScore.pop(0)
        elif PAdate[-1].date() < interactDate[-1].date() :#if pa ends before interact
            print 'pa data removed from end'
            interactDate.pop()
            interactScore.pop()
        elif PAdate[-1].date() > interactDate[-1].date() :#if pa ends after interact
            print 'interact data removed from end'
            PAscore.pop()
            PAdate.pop()
        else: # uneven values must be from missing days in middle of one dataset
            longer = list()
            shorter = list()
            ldate = list()
            sdate = list()
            shortName = ''
            if len(PAscore) > len(interactScore):
                shortName = 'interaction'
                longName  = 'PA'
                longer = PAscore
                shorter= interactScore
                ldate  = PAdate
                sdate  = interactDate
            else:
                shortName = 'PA'
                longName  = 'interaction'
                longer = interactScore
                shorter= PAscore
                ldate  = interactDate
                sdate  = PAdate
            for i in range(len(longer)):
                #if i >= len(shorter): #check for end of shortlist reached
                #    print '\nERR: unknown data mismatch!!!\n'
                #    print 'data dump:'
                #    print '===   PA   ==='
                #    print 'DATES='+str(PAdate)
                #    print 'VALUES='+str(PAscore)
                #    print '===interact==='
                #    print 'DATES='+str(interactDate)
                #    print 'VALUES='+str(interactScore)
                #    return
                if i>=len(shorter) or sdate[i].date() != ldate[i].date():#remove extra dates not in shortlist
                    print 'value removed from '+longName+' at '+str(ldate[i])
                    longer.pop(i)
                    ldate.pop(i)
                    #shorter.insert(i,0)
                    #sdate.insert(i,ldate[i])
                    #print 'zero value inserted into '+shortName+' at '+str(sdate[i])
                    break
        if len(PAscore)<=0 or len(interactScore)<=0:
            raise Warning('data has no overlap!')

    # modify interaction score to just separate (+) and (-) values