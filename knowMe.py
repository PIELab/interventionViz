
import pylab
import savReaderWriter
from src.post_view_event_steps_bars import makeTheActualPlot

 # list of indicies which are manually identified as interventions
INDEXES_TAGGED_INTERVENTION = [5, 7, 9, 10, 30, 33, 34, 38, 41, 42, 47, 52, 56, 57, 58, 60, 62, 66, 70, 97,
              99, 113, 119, 120, 134, 139, 141, 146, 152, 153, 157, 167, 178, 205, 206, 217,
              222, 223, 231, 237, 261, 271, 272, 280, 287, 290, 296, 299]
# list of indicies which are manually id'd as praise for being active
INDEXES_TAGGED_REINFORCEMENT = [0, 16, 19, 55, 71, 98, 111, 112, 130, 136, 143, 148, 169, 180, 183, 185,
                 207, 214, 220, 226, 239, 246, 247, 252, 255, 261, 269, 277, 279, 289, 298]
                 # also 157 (but praise is for previous day so not included above)

FILE_END = 41970
HIGHEST_PNUM = 36


class DataStream(object):
    """
    a list of data points which are sequential (no gaps!)
    """
    def __init__(self, data=[], data_start_index=0):
        self.data = data
        self.data_start_index = data_start_index  # index of the first point in data relative to the full database

    def add_data(self, row):
        self.data.append(row)


class MessageData(object):
    """
    a message and the context associated with it
    """
    def __init__(self, data_section, index):
        """
        :param data_section: the section of data containing the message
        :param index: the index of the message
        """
        self.data_section = data_section
        self.index = index
        self.data = data_section[index]


class MessageSet(object):
    """
    represents a single set of messages delivered consecutively
    """
    def __init__(self, message='', index=None, data_stream=DataStream()):
        self.message = message
        self.index = index
        self.data_stream = data_stream


def get_data_dict(line, index):
    """
    returns data dict for given line in file
    :param line: array of values
    :param index: original index of row
    :return: dict with keyed data
    """
    return {
        "pid": line[0],
        "day": line[1],
        "rcvd_consec": line[2],
        "sent_consec": line[3],
        "sms_rec": line[4],
        "sms_sent": line[5],
        "time": line[6],
        "sent_txt": line[7].strip(),
        "rcvd_txt": line[8].strip(),
        "sms_type": line[9],  # Type of SMS(1=text sent , 2= text received, 3=text received and text sent
        "rcvd_daily": line[10],
        "sent_daily": line[11],
        "total_Consec": line[12],
        "total_daily": line[13],
        "all_txt": line[14].strip(),
        "base_acc_cnts": line[15],
        "int_acc_cnts": line[16],
        "Flup_Acc_Cnts": line[17],  # TODO: make these lowercase
        "KM_Lying_Min": line[18],
        "KM_Sit_Min": line[19],
        "KM_SitFidg_Min": line[20],
        "KM_Stnd_Min": line[21],
        "KM_StndFidg_Min": line[22],
        "KM_Wii_Min": line[23],
        "KM_SlwWlk_Min": line[24],
        "KM_BrskWlk_Min": line[25],
        "KM_Run_Min": line[26],
        "KM_HR": line[27],
        "index": index
        # NOTE: the indexes in consts are relative to the index of outgoing sms, not all rows, so this doesn't work:
        #"intervention": (index in INDEXES_TAGGED_INTERVENTION),
        #"reinforcement": (index in INDEXES_TAGGED_REINFORCEMENT)
    }


def get_data_sections(file_name):
    """
    :param file_name: name of save file to read
    :return: array of arrays of consecutive data like [[d1, d2], [d6, d7, d8]]
    """
    data_sections = [[]]
    with savReaderWriter.SavReader(file_name, ioLocale='en_US.UTF-8') as reader:
        row_n = 0
        for line in reader:
            if line[27] is not None:  # test for if line has data we want in it
                #print get_data_dict(line, row_n)
                data_sections[-1].append(get_data_dict(line, row_n))
            else:  # move to next data section
                if len(data_sections[-1]) > 0:  # only move if not already an empty array
                    data_sections.append([])
            row_n += 1
            if row_n >= FILE_END:  # yeah... that happens...
                break
    return data_sections


def load_n_plot(savFileName):
    """
    loads & displays data
    :return: None
    """

    messages = []
    data_streams = []
    row_n = 0

    with savReaderWriter.SavReader(savFileName, ioLocale='en_US.UTF-8') as reader:
        for line in reader:
            hr = line[27]
            if hr is not None:  # if hr data present
                # append to current data stream or create new
                try:
                    data_streams[-1].add_data(line)
                except IndexError:
                    data_streams.append(DataStream())
                    data_streams[-1].add_data(line)

                msg_content = line[7].strip()
                if len(msg_content) > 0:  # if there is a message here
                    try:
                        messages[-1].add_data_point()
                        # if a consecutive message
                        #   add to existing messageSet
                    except IndexError:
                        #   create new messageData
                        messages.append(MessageData(data_start_index=row_n, message_text=msg_content))
                        messages[-1].add_data_point()

            else:
                # move to next data stream
                pass

            row_n += 1


def _load_n_plot_dep(savFileName):
    """
    depreciated method which loads & displays data
    :return: None
    """
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
        if i in INDEXES_TAGGED_INTERVENTION:
            filteredMessages.append(messages[i])
            filteredPnums.append(pnums[i])
            filteredHRs.append(HRs[i])

    print len(filteredMessages), ' intervention-type messages'

    MINS = 20
    trim_to(filteredHRs, MINS)

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


def trim_to(filteredHRs, leng):
    # trim if too long
    for i in range(len(filteredHRs)):  # TODO: rename to filteredHRs...
        filteredHRs[i] = filteredHRs[i][:leng]

if __name__ == "__main__":
    save_file = "./../knowMeData/knowMeData.sav"
    sections = get_data_sections(save_file)

    # make event list
    msg_send_events = list()
    for sec_i, section in enumerate(sections):
        event_n = 0
        for row_i, row in enumerate(section):
            #print row['sms_sent']
            if len(row['sent_txt']) > 0:
                msg_send_events.append(MessageData(section, row_i))
                event_n += 1
        #print "section ", sec_i, "\tlen:", len(section), "\tevents:", event_n

    print "\t===\ntotal messages:", len(msg_send_events)

    # select intervention events from event list
    intervention_events = list()
    for e_i, event in enumerate(msg_send_events):
        if e_i in INDEXES_TAGGED_INTERVENTION:
            intervention_events.append(event)
            #print event.data['sent_txt']

    # get everything into arrays for plotting
    pids = list()
    bars = list()
    pre_win = 20  # window size before event
    post_win = 40  # window size after event
    exclude_n = 0
    for event in intervention_events:
        data = list()
        event_pid = None
        for data_point in event.data_section:
            if event_pid != data_point['pid'] or event_pid is None:
                event_pid = data_point['pid']
            data.append(data_point['KM_HR'])
        start = event.index - pre_win
        end = event.index + post_win
        dat = data[start:end]
        if len(dat) == pre_win+post_win:
            bars.append(dat)
            pids.append(event_pid)
        else:
            print "event excluded due to insufficient data, only", len(dat), 'points'
            exclude_n += 1

    print 'plotting ', len(bars), 'events;', exclude_n, 'excluded'

    print pids

    makeTheActualPlot(pre_win+post_win, pids, bars, HIGHEST_PNUM)
    pylab.axvline(x=pre_win, linewidth=5, linestyle='--', color='gray', label='event')
    #pylab.plot(pre_win, 0, marker='*', color='black', markersize=20, fillstyle="full")
    pylab.show()