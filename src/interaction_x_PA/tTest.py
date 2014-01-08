# -*- coding: utf-8 -*-

import pylab # for plotting commands & array
from scipy import stats

from src.PA.PAdata import PAdata
from src.interaction.timeSeries.multicolorBars import interactionData
from src.interaction.score import segmentInteractionIntoDays
from src.PA.score import segmentPAIntoDays,getPAscore_postiveOnly

from src.settings import InputError, HIGHEST_P_NUMBER

def plot(dataset='test',dataLoc = "./data/"):
	if dataset=='test':
		from src.settings import setupTestData as dataSetup
	elif dataset == 'USF':
		from src.settings import setupUSFData as dataSetup
	else:
		raise ValueError('dataset "'+str(dataset)+'" not recognized')


	pltName = 'All participants\' PA for sedentary & active avatar days'
	print 'making plot "'+pltName+'"'
	pylab.figure(pltName)
	activeBase = 0
	sedentBase = 0
	zeroBase   = 0
	cmap       = pylab.cm.get_cmap(name='jet')

	activePAs = list()
	sedentPAs = list()
	zeroPAs   = list()

	for pNum in range(HIGHEST_P_NUMBER+1): #cycle through all participants
		if pNum == 1 or pNum == 3 or pNum == 13 or pNum == 14: 
			# skip p1 & p3 b/c data is incomplete
			# skip p13 b/c data needs some massaging
			# skip p14 b/c data is incomplete
			continue
		activePAtotal = sedentPAtotal = zeroPAtotal = 0
		activePAcount = sedentPAcount = zeroPAcount = 0

		try :
			pid,interactFile,PAfile = dataSetup(pNum)

			interactFile = dataLoc+pid+'/'+interactFile;
			PAfile    = dataLoc+pid+'/'+PAfile;
			settings = dict(interactionFileLoc=interactFile,
					      PAfileLoc=PAfile)

			# load interaction data
			interact = interactionData(settings['interactionFileLoc'])
			interactScore,interactDate = segmentInteractionIntoDays(interact)

			# load PA data
			PA = PAdata(settings['PAfileLoc'])
			PAscore,PAdate = segmentPAIntoDays(PA,PAscoreFunction=getPAscore_postiveOnly)

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
						#	print '\nERR: unknown data mismatch!!!\n'
						#	print 'data dump:'
						#	print '===   PA   ==='
						#	print 'DATES='+str(PAdate)
						#	print 'VALUES='+str(PAscore)
						#	print '===interact==='
						#	print 'DATES='+str(interactDate) 
						#	print 'VALUES='+str(interactScore)
						#	return
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

					pylab.plt.bar(interactions[day], PAscore[day], bottom=activeBase, linewidth=1, color=cmap(float(pNum)/float(HIGHEST_P_NUMBER)) )
					activeBase += PAscore[day]
				elif interactions[day] < 0:
					sedentPAtotal+=PAscore[day]
					sedentPAcount+=1

					pylab.plt.bar(interactions[day], PAscore[day], bottom=sedentBase, linewidth=1, color=cmap(float(pNum)/float(HIGHEST_P_NUMBER)) )
					sedentBase += PAscore[day] 
				else: # interactions[day] == 0
					zeroPAtotal+=PAscore[day]
					zeroPAcount+=1

					pylab.plt.bar(interactions[day], PAscore[day], bottom=zeroBase,   linewidth=1, color=cmap(float(pNum)/float(HIGHEST_P_NUMBER)) )
					zeroBase   += PAscore[day]


			activePAs.append(activePAtotal/activePAcount)
			sedentPAs.append(sedentPAtotal/sedentPAcount)
			try:
				zeroPAs.append(zeroPAtotal/zeroPAcount)
			except ZeroDivisionError:
				zeroPAs.append(0)

		except InputError: 
			print 'participant '+str(pNum)+' not valid.'
		except IOError: 
			print 'participant '+str(pNum)+' not found.'
		except Warning as w:
			print w.message

	pylab.plt.ylabel('physical activity score')
	pylab.plt.xlabel('<-sedentary                   zero                   active->\navatar behavior')

	pylab.plt.draw()

	print activePAs
	print sedentPAs
	print zeroPAs

	paired_sample = stats.ttest_rel(sedentPAs, activePAs)
	print "The t-statistic is %.3f and the p-value is %.3f." % paired_sample

	print 'done.'
