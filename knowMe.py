
import pylab
import savReaderWriter
from src.post_view_event_steps_bars import makeTheActualPlot

savFileName = "./../knowMeData/knowMeData.sav"
lineN = 0
FILE_END = 41970
messageObjs = list()
messages = list()
pnums = list()
HRs = list()
counter = 0  # count of messages logged

#try:
with savReaderWriter.SavReader(savFileName, ioLocale='en_US.UTF-8') as reader:
    for line in reader:
        hr = line[27]
        if hr is not None:  # if outgoing sms sent
            msgContent = line[7].strip()
            if len(msgContent) > 0:
                counter += 1
                pid = line[0]
                day = line[1]
                time = line[6]
                #print 'p', pid, '->', msgContent, ' @ d', day, 't', time, ' HR:', hr

                messageObjs.append({"msg":msgContent, "pnum":line[0], "HR":[hr]})
                messages.append(msgContent)
                pnums.append(pid)
                HRs.append([hr])

                counter += 1

            if len(messageObjs) > 0:
                messageObjs[-1]["HR"].append(line[27])
                HRs[-1].append(line[27])

        lineN += 1
        if lineN >= FILE_END:  # yeah... that happens...
            break
#except:
#    print 'ERR @ line !!!', lineN

print '   ===   ===   ===   \n         n=', counter, '\n   ===   ===   ===   '
MINS = 60

# trim if too long
for i in range(len(HRs)):
    HRs[i] = HRs[i][:MINS]

tooShort = 0
# remove if too short
trimmedHRs = list()  # this is a poor name choice, since this includes only events w/ full arrays
for i in range(len(HRs)):
    if len(HRs[i]) < MINS:
        HRs[i] = [0]*MINS
        tooShort += 1
    else:
        trimmedHRs.append(HRs[i])

print 'too short:', tooShort
makeTheActualPlot(MINS,pnums, trimmedHRs, 36)
pylab.show()