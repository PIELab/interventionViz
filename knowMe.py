import pylab
import savReaderWriter
from src.post_view_event_steps_bars import makeTheActualPlot, PLOT_TYPES

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


def makePlot(type=PLOT_TYPES.bars):
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
    for e_i, event in enumerate(intervention_events):
        data = list()
        event_pid = event.data_section[0]['pid']
        for data_point in event.data_section:
            if event_pid != data_point['pid']:
                raise Error('pid changed without change in sensor section!')
            data.append(data_point['km_hr'])
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

    print 'plotting ', len(bars), 'events;', exclude_n, 'excluded'

    makeTheActualPlot(pre_win+post_win, pids, bars, HIGHEST_PNUM, type=type,
                      event_time=pre_win, yLabel="Heart Rate (BPM)")

if __name__ == "__main__":
    makePlot()
    pylab.show()