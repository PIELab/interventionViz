# -*- coding: utf-8 -*-

import pylab # for plotting commands & array

from src.dep.PA.PAdata import PAdata
from src.dep.interaction.timeSeries.multicolorBars import interactionData
from src.dep.interaction.score import segmentInteractionIntoDays
from src.dep.PA.score import segmentPAIntoDays,getPAscore_postiveOnly


def plot(settings):
	# load interaction data
	interact = interactionData(settings['interactionFileLoc'])
	interactScore,interactDate = segmentInteractionIntoDays(interact)

	# load PA data
	PA = PAdata(settings['PAfileLoc'])
	PAscore,PAdate = segmentPAIntoDays(PA,PAscoreFunction=getPAscore_postiveOnly)

	# data check
	print 'data is ' + str(len(PAscore)) + 'x' + str(len(interactScore))

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
			print '\n ERR: data has no overlap!\n'
			return

	print '\t NAME   \tSTART \t\t\tEND \t\t\tLEN'
	print '\t interact\t'+str(interactDate[0])+'\t'+str(interactDate[-1])+'\t'+str(len(interactScore))
	print '\t PA     \t'+str(PAdate[0])+      '\t'+str(PAdate[-1])      +'\t'+str(len(PAscore))+'\n'

	# modify interaction score to just separate (+) and (-) values
	interactions = list()
	for iScore in interactScore:
		if iScore > 0:
			interactions.append(1)#'active')
		elif iScore < 0:
			interactions.append(-1)#'sedentary')
		else: # iScore = 0
			interactions.append(0)#'0')

	pltName = 'user PA for sedentary & active avatar days'
	print 'making plot "'+pltName+'"'
	pylab.figure(pltName)
	activeBase = 0
	sedentBase = 0
	zeroBase   = 0
	for day in range(len(PAscore)):
		#print 'day     ='+str(day)
		#print 'interact='+str(interactions[day])
		#print 'PAscore ='+str(PAscore[day])
		if interactions[day] > 0:
			pylab.plt.bar(interactions[day],PAscore[day],bottom=activeBase,linewidth=1)
			activeBase += PAscore[day]
		elif interactions[day] < 0:
			pylab.plt.bar(interactions[day],PAscore[day],bottom=sedentBase,linewidth=1)
			sedentBase += PAscore[day] 
		else: # interactions[day] == 0
			pylab.plt.bar(interactions[day],PAscore[day],bottom=zeroBase,linewidth=1)
			zeroBase   += PAscore[day]

	pylab.plt.ylabel('physical activity score')
	pylab.plt.xlabel('<-sedentary                   zero                   active->\navatar behavior')

	pylab.plt.draw()
