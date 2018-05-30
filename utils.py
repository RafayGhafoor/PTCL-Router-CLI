import re

def validate_gateway(gateway):
    if not re.search("https?://", gateway) and not gateway.endswith('/'):
        return True
    return False


def convert_time(start_time="1", end_time="23:59"):
        # TODO : Add test that the numbers after : shouldn't exceed 60 (minutes)
        '''
        Converts time to minutes.
        Takes time and splits it by ":", the first element before ":" is in
        hour and the second element is in minutes.

        Parameters:
        - start_time: start time to apply limit from. Eg: 1:00 (am)
        - end_time:   end time to apply limit till. Eg: 13:00 (pm)

        Return (Integer):
            sum of start_time and end_time in format (Hours * 60 + minutes).

        Example:
        >>> convert_time(13:00, 18:08)
            # returns (13 * 60) + 00, (18 * 60) + 08
            780, 1080
        '''
        start_time = [int(i) for i in start_time.split(':')]
        end_time = [int(i) for i in end_time.split(':')]
        if len(start_time) == 1:
            start_time.append(00)
        if len(end_time) == 1:
            end_time.append(00)
        # if end_time[0] > 24 or start_time[0] > 24 or end_time[1] > 60 or start_time[1] > 60:
            # raise custom Exception
        start_time = (start_time[0] * 60) + start_time[1]
        end_time = (end_time[0] * 60) + end_time[1]
        return (start_time, end_time)