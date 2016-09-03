import pylab
import savReaderWriter
from src.post_view_event_steps_bars import makeTheActualPlot, PLOT_TYPES
from math import log

 # list of indicies which are manually identified as interventions
INDEXES_TAGGED_INTERVENTION = [5, 7, 9, 10, 30, 33, 34, 38, 41, 42, 47, 52, 56, 57, 58, 60, 62, 66, 70, 97,
                               99, 113, 119, 120, 134, 139, 141, 146, 152, 153, 157, 167, 178, 205, 206, 217,
                               222, 223, 231, 237, 261, 271, 272, 280, 287, 290, 296, 299]
# list of indicies which are manually id'd as praise for being active
INDEXES_TAGGED_REINFORCEMENT = [0, 16, 19, 55, 71, 98, 111, 112, 130, 136, 143, 148, 169, 180, 183, 185,
                                207, 214, 220, 226, 239, 246, 247, 252, 255, 261, 269, 277, 279, 289, 298]
                                # also 157 (but praise is for previous day so not included above)

FILE_END = 41970

"""
NOTES:



"""


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
        "flup_acc_cnts": line[17],
        "km_lying_min": line[18],
        "km_sit_min": line[19],
        "km_sitfidg_min": line[20],
        "km_stnd_min": line[21],
        "km_stndfidg_min": line[22],
        "km_Wii_Min": line[23],
        "km_slwwlk_min": line[24],
        "km_brskwlk_min": line[25],
        "km_run_min": line[26],
        "km_hr": line[27],
        "sms_intervention": line[28],
        "index": index
        # NOTE: the indexes in consts are relative to the index of outgoing sms, not all rows, so this doesn't work:
        #"intervention": (index in INDEXES_TAGGED_INTERVENTION),
        #"reinforcement": (index in INDEXES_TAGGED_REINFORCEMENT)
    }


def get_data_sections(file_name, filterColumnNumber=16):# or 27
    """
    loads chunks of data surrounding sms interventions.
    assumes data is sorted by pid, day, and time.
    :param file_name: name of save file to read
    :param filterColumnNumber: column which must be present for data to be included
    :return: array of arrays of consecutive data like [[d1, d2], [d6, d7, d8]]
    """
    data_sections = [[]]
    with savReaderWriter.SavReader(file_name, ioLocale='en_US.UTF-8') as reader:
        row_n = 0
        currentPID = 9
        for line in reader:
            if (line[filterColumnNumber] is not None  # test for if line has data we want in it
                and line[0] == currentPID):
                #print get_data_dict(line, row_n)
                data_sections[-1].append(get_data_dict(line, row_n))
            else:  # move to next data section
                if len(data_sections[-1]) > 0:  # only move if not already an empty array
                    data_sections.append([])
                currentPID = line[0]
            row_n += 1
            if row_n >= FILE_END:  # yeah... that happens...
                break
    return data_sections

def load_arx_model_data(file_name):
    """
    assumes data in file_name is sorted by pid, day, and time.
    loads SMS_intervention and heart rate data for use in arx modeling.
    NOTE: current implementation ignores gaps in data and simply concats.
    """
    filterColumnNumber = 16  # or 27
    SMS_INTERVENTION_KEY = 'sms_intervention'
    SMS_INTERVENTION_COL = 28
    INT_ACC_CNTS_KEY = 'int_acc_cnts'
    INT_ACC_CNTS_COL = 16
    PID_COL = 0


    data = {}
    with savReaderWriter.SavReader(file_name, ioLocale='en_US.UTF-8') as reader:

        # data {
        #     9: {
        #         'SMS_intervention': [1,2,3,6,2,23], 'int_acc_cnts':[34,1,5,63]
        #     },
        #     15: {
        #         '':[], '':[]
        #     }
        # }
        row_n = 0
        for line in reader:
            pid = line[PID_COL]
            if line[filterColumnNumber] is not None:  # test for if line has data we want in it
                # print pid, line[SMS_INTERVENTION_COL], line[INT_ACC_CNTS_COL]
                try:  # append to existing participant
                    sms_interv = line[SMS_INTERVENTION_COL] or 0
                    acc_cnt = line[INT_ACC_CNTS_COL] or 0
                    if acc_cnt > 0:
                        acc_cnt = log(acc_cnt)
                    if sms_interv != 0 or acc_cnt != 0:
                        # print 'append ' + str(sms_interv) + ',' + str(acc_cnt)
                        data[pid][SMS_INTERVENTION_KEY].append(sms_interv)
                        data[pid][INT_ACC_CNTS_KEY].append(acc_cnt)
                        # TODO: use actual dates
                        # data[pid][DATE_KEY].append(#TODO: format date)
                        # print data[pid]
                    # else nvm
                except KeyError as ex:  # new participant
                    data[pid] = {}
                    data[pid][SMS_INTERVENTION_KEY] = []
                    data[pid][INT_ACC_CNTS_KEY] = []
                    # data[pid][DATE_KEY] = []
            row_n += 1
            if row_n >= FILE_END:  # yeah... that happens...
                break
    return data

def makePlot(type=PLOT_TYPES.bars, selected_data='km_hr', yLabel="Heart Rate (BPM)",
             pre_win=20, post_win=40, smooth=None):
    """
    pre_win = 20  # window size before event
    post_win = 40  # window size after event
    :param type:
    :param selected_data:
    :param yLabel:
    :return:
    """
    save_file = "./data/knowMeData.sav"
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
    intervention_events = []
    control_events = []
    for e_i, event in enumerate(msg_send_events):
        if e_i in INDEXES_TAGGED_INTERVENTION:
            intervention_events.append(event)
            #print event.data['sent_txt']
        elif e_i in INDEXES_TAGGED_REINFORCEMENT:
            control_events.append(event)

    # get everything into arrays for plotting
    pids = list()
    bars = list()
    exclude_n = 0
    for e_i, event in enumerate(intervention_events):
        data = list()
        event_pid = event.data_section[0]['pid']
        for data_point in event.data_section:
            if event_pid != data_point['pid']:
                raise Exception('pid changed without change in sensor section!')
            data.append(data_point[selected_data])
        start = event.index - pre_win
        end = event.index + post_win
        dat = data[start:end]
        if len(dat) == pre_win+post_win:
            bars.append(dat)
            pids.append(event_pid)
        else:
            print "exclude#", e_i, "\tinsuff data for win ", pre_win, ':', post_win, \
                "s=", len(data[:event.index]), '\t:\t', len(data[event.index:]), '\t(', len(data), ')'
            exclude_n += 1

    pid_remap = list()
    seen_pids = list()
    for pid in pids:
        if pid not in seen_pids:
            seen_pids.append(pid)
        pid_remap.append(seen_pids.index(pid))

    highest_pnum = len(seen_pids)

    print 'plotting ', len(bars), 'events;', exclude_n, 'excluded'

    makeTheActualPlot(pre_win+post_win, pid_remap, bars, highest_pnum, type=type,
                      event_time=pre_win, yLabel=yLabel, smooth=smooth)


def makePlots(type=PLOT_TYPES.bars, show=True, pre_win=20, post_win=40):
    interesting_data_types = {
        "km_hr": "Heart Rate (BPM)",
        "int_acc_cnts": "Accelerometry Count",
        "km_lying_min": "s lying down",
        "km_sit_min": "s sitting",
        "km_sitfidg_min": "s fidgiting",
        "km_stnd_min": "s standing",
        "km_stndfidg_min": "s standing and fidgiting",
        "km_Wii_Min": "s playing wii",
        "km_slwwlk_min": "s walking slow",
        "km_brskwlk_min": "s brisk walking",
        "km_run_min": "s running"
    }

    for data_type in interesting_data_types:
        key = data_type
        descrip = interesting_data_types[key]
        if not show:
            print 'plotting ', descrip
            pylab.figure(key)
        makePlot(type=type, selected_data=key, yLabel=descrip, pre_win=pre_win, post_win=post_win)
        if show:
            pylab.show()


if __name__ == "__main__":
    makePlots()
