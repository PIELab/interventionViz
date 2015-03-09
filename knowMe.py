
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

 # list of indicies which are manually identified as interventions
manualTags = [5, 7, 9, 10, 30, 33, 34, 38, 41, 42, 47, 52, 56, 57, 58, 60, 62, 66, 70, 97,
              99, 113, 119, 120, 134, 139, 141, 146, 152, 153, 157, 167, 178, 205, 206, 217,
              222, 223, 231, 237, 261, 271, 272, 280, 287, 290, 296, 299]
# list of indicies which are manually id'd as praise for being active
reinforceTags = [0, 16, 19, 55, 71, 98, 111, 112, 130, 136, 143, 148, 169, 180, 183, 185,
                 207, 214, 220, 226, 239, 246, 247, 252, 255, 261, 269, 277, 279, 289, 298]
                 # also 157 (but praise is for previous day so not included above)

#try:
with savReaderWriter.SavReader(savFileName, ioLocale='en_US.UTF-8') as reader:
    for line in reader:
        hr = line[27]
        if hr is not None:  # if outgoing sms sent
            msgContent = line[7].strip()
            if len(msgContent) > 0:
                pid = line[0]
                day = line[1]
                time = line[6]
                #print 'p', pid, '->', msgContent, ' @ d', day, 't', time, ' HR:', hr
                #print counter,': ', msgContent
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

print '   ===   ===   ===   \n'
print counter, '(', len(messages), ') messages'

# filter for messages tagged as "interventions"
filteredHRs = list()
filteredPnums = list()
filteredMessages = list()
for i in range(len(messages)):  # TODO: rename to messages
    if i in manualTags:
        filteredMessages.append(messages[i])
        filteredPnums.append(pnums[i])
        filteredHRs.append(HRs[i])

print len(filteredMessages), ' intervention-type messages'

MINS = 20
HIGHEST_PNUM = 36

# trim if too long
for i in range(len(filteredHRs)):  # TODO: rename to filteredHRs...
    filteredHRs[i] = filteredHRs[i][:MINS]

tooShort = 0
# remove if too short
trimmedHRs = list()  # this is a poor name choice, since this includes only events w/ full arrays
trimmedPnums = list()
trimmedMessages = list()
for i in range(len(filteredHRs)):
    if len(filteredHRs[i]) < MINS:
        filteredHRs[i] = [0]*MINS
        tooShort += 1
    else:
        trimmedHRs.append(filteredHRs[i])
        trimmedPnums.append(filteredPnums[i])
        trimmedMessages.append(filteredMessages[i])

print tooShort, ' too close to other messages'
print 'analyzing ', len(trimmedMessages), ' perfect data points'

makeTheActualPlot(MINS, trimmedPnums, trimmedHRs, HIGHEST_PNUM)
pylab.show()