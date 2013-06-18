# -*- coding: utf-8 -*-

# this script reads in mMonitor's DAILY_TOTALS and viewLog data, creates a simple 'score' for each, and plots the scores. This function assumes that the data sets come from the EXACT same days (and number of days); no checking is done to verify this, but data with different numbers of days prints a 'arrays must be same size' error.

import pylab # for plotting commands & array

from ..settings import * 
from ..PA.timeSeries.PAdata import *
from ..interaction.timeSeries.multicolorBars import data as interactionData

def plot():
	# load interaction data
	interact = interactionData()
	interact.getData(viewFileLoc)
	# generate interaction 'score'
	interactScore = list()
	interactDate   = list()
	# gather data from timestamps in interact.x together by day
	i = 0
	while i+1 < len(interact.x)-1:
		score = 0
		#print str(interact.x[i].date()) +'=?='+str(interact.x[i+1].date())
		while interact.x[i].date() == interact.x[i+1].date(): # count up all in same day
			date = interact.x[i]
			#print str(i)
			score += interact.a1[i]+interact.a2[i]+interact.a3[i]-(interact.p1[i]+interact.p2[i]+interact.p3[i])
			i+=1
			if i+1 > len(interact.x)-1:
				break
		score += interact.a1[i]+interact.a2[i]+interact.a3[i]-(interact.p1[i]+interact.p2[i]+interact.p3[i])
		i+=1
		# now score is day's total, add it to the list
		interactScore.append(score)
		interactDate.append(date)


	# load PA data
	PA = PAdata()
	PA.getData(PAfileLoc)
	# generate daily PA 'score'
	PAscore = list()
	PAdate  = list()
	for i in range(0,len(PA.time)):
		PAscore.append(4*PA.vig[i]+3*PA.mod_vig[i]+2*PA.mod[i]+PA.light[i]-PA.sedentary[i])
		PAdate.append(PA.time[i])
	PAscore = PAscore[::-1]	#invert the list to match interaction data
	PAdate  = PAdate[::-1]

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

		#print '\n'+str(interactDate)
		#print '\n'+str(PAdate)+'\n'

	pltName = 'PA vs interaction'
	print 'making plot "'+pltName+'"'
	pylab.figure(pltName)
	#p = pylab.figure()
	# lineGraph = p.add_subplot(211)
	# lineGraph.plot(x,y)
	#barGraph = p.add_subplot(111)
	pylab.plt.scatter(PAscore,interactScore,color='b')

	pylab.plt.ylabel('physical activity score')
	pylab.plt.xlabel('proteus PA influence')

	pylab.plt.draw()

