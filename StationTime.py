import time

class StationTime (object):
    def __init__(self, name):
        """"
        Initializes a Station with 4 platforms as well as a print string at the end.
        :param name: The name of the station object
        :return: Platforms initialized with no time stamp
        """

        self.station = name
        self.next1 = Interval()
        self.next2 = Interval()
        self.next3 = Interval()
        self.next4 = Interval()
        self.string = ""


    def difference(self, dct):
        """
        Checks if a new train of a specific line is in the station and returns the line name and the time difference. Function that intakes a dictionary
        of a sample of the trains in the station at a given time and returns an updated string with the difference in time passed since the specific line
        had last been at the station
        :param dct: Information about lines arriving at the specific object
        :return: Sting of time difference between the line arriving at the station
        """

        color1, diff1 = Interval(dct[1][0]) - self.next1
        color2, diff2 = Interval(dct[2][0]) - self.next2
        color3, diff3 = Interval(dct[3][0]) - self.next3
        color4, diff4 = Interval(dct[4][0]) - self.next4

        self.string += f"{color1}{diff1}{color2}{diff2}{color3}{diff3}{color4}{diff4}"


    def __str__(self):
        """
        Returns the station and the corresponding data points gathered from the experiment
        :return: String of the station and datapoints
        """
        return f"{self.station},{self.string},"


class Interval (object):
    def __init__(self, next_train =[]):
        """
        Initializes a list that will store the time of the last train of each line for the specified platform in StationTime
        :param next_train: Tests whether a train line is in the station for a specific platform
        """

        # Storage of the last train for the Red, Green, Orange, Blue, Silver, Yellow lines respectively
        self.lines = ['', '', '', '', '', '']

        # If the event is not the initialization of a platform for the StationTime object, this line should run
        try:
            next_train[0]
            next_train[3]

            # If the next train is at, or arriving at the station update the corresponding item in the self.lines list
            if next_train[3] == 'BRD' or next_train[3] == 'ARR':
                if next_train[0] == 'Red Line':
                    self.lines[0] = time.time()
                elif next_train[0] == 'Green Line':
                    self.lines[1] = time.time()
                elif next_train[0] == 'Orange Line':
                    self.lines[2] = time.time()
                elif next_train[0] == 'Blue Line':
                    self.lines[3] = time.time()
                elif next_train[0] == 'Silver Line':
                    self.lines[4] = time.time()
                elif next_train[0] == 'Yellow Line':
                    self.lines[5] = time.time()
        except:
            pass

    def _update(self, new_time, i):
        """
        Internal function used in the subtract function for Interval objects
        :param new_time: the updated time of the new train arriving at the station
        :param i: index of the train line being utilized
        :return:
        """
        self.lines[i] = new_time
        return

    def __sub__(self, other):
        """
        Determines the time elapsed and the line that has reached the platform, if there's no new train it returns nothing.
        :param other: Most previous time that was saved for each platform in the StationTime object
        :return: Line Code, time elapsed
        """

        # Lines correspond to Red, Green, Orange, Blue, Silver, Yellow
        lines_lst = [',R', ',G', ',O', ',B', ',S', ',Y']
        for i in range(6):
            # Checks both the new and old time stamps must be present, as well as the time stamps are not the same
            if type(self.lines[i]) == float and type(other.lines[i]) == float and self.lines[i] - other.lines[i] > 1:
                # Calculated the difference between the two values and updates the StationTime object with the new time of arrivial
                change = self.lines[i] - other.lines[i]
                other._update(self.lines[i], i)
                return lines_lst[i],change
            elif type(self.lines[i]) == float:
                other._update(self.lines[i], i)

        # If the initial StationTime is not initialized or doesn't have a train yet
        return '', ''
