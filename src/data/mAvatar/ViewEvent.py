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

    @staticmethod
    def is_valid(val):
        """
        returns true if valid value is given
        """
        if val in [-2, -1, 1, 2]:
            return True
        else:
            return False


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
        self.activity_type = first_point.type
        self.activities = [first_point.activity]

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
        if next_point.type != self.activity_type:
            raise AssertionError('logpoint type ' + str(next_point.type) + ' does not match ViewEvent type ' + str(self.activity_type))

        self.points.append(next_point)
        self.activities += next_point.activity
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
