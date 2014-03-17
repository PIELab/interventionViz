'''
show() method loads data for all (USF) participants and summarizes study lengths
'''

from src.settings import setup, HIGHEST_P_NUMBER
from src.metaData.studyLength import studyLength

DATA_LOC = '../subjects/'

def show():
	# load in all the data
	participants = list()
	studyLengths = list()

	for pNum in range(HIGHEST_P_NUMBER+1): #cycle through all participants

		settings = setup(dataset='USF', dataLoc=DATA_LOC, subjectN=pNum)

		pid = str(pNum)
					
		try:
			lenData = studyLength(fileLoc=settings.getFileName('metaData'))
			studyLen = len(lenData.days)
			
		except IOError:
			# print 'p '+pid+' metaData file not found'
			continue
			
		# if no problems:
		participants.append(pid)
		studyLengths.append(studyLen)
	
	# print a nice little table of interaction lengths
	divider = '======================================'
	print divider
	cols = ['pid', 'studyLen']
	row_format ="{:>15}" * (len(cols))
	print row_format.format(*cols)
	for pid, length in zip(participants, studyLengths):
		print row_format.format(pid, length)
	print divider