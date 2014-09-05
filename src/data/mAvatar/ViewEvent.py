__author__ = 'tylar'


class EventTypes(object):
    """
    a) "glance" wallpaper is viewed between 1s and 60s in length.
    b) "fault_short" wallpaper is viewed for less than minimum view time, no event.
    c) "usage" wallpaper viewed multiple times, insufficient recovery period between, lumped into one event.
    d) "fault_long" unrealistically long view time (red) is replaced with shorter view times at beginning and end.
    """
    glance, usage = 1, 2

    # these two aren't actually used...
    fault_short, fault_long = -1, -2


class ViewEvent(object):
    def __init__(self, first_point):
        self.points = [first_point]

        # === view event info ===
        self.length = first_point.len
        # "density" is amount of time in the event len which avatar is actually viewed...
        self.density = first_point.len
        self.type = EventTypes.glance
    #    self.has_next_event
    #    self.next_event_point
    #    self.time_until_next_event

        # === info for looking up the view event in the data later ===
    #    self.pnum
        self.t0 = first_point.t0
        self.tf = first_point.tf

    def extend_event(self, next_point):
        """
        continues a view event with another logged point
        :param next_point: next log point to be included in this one
        :return:
        """
        self.points.append(next_point)
        self.length = self.points[0].t0 - next_point.tf
        self.density += next_point.len
        self.type = EventTypes.usage
        self.tf = next_point.tf

    def end_event(self, next_event_point = None):
        """
        ends this event
        :param next_event_point:
        :return:
        """
        if next_event_point is None:
            self.has_next_event = False
        else:
            self.has_next_event = True
            self.next_event_point = next_event_point
            self.time_until_next_event = next_event_point.t0 - self.points[-1].tf
