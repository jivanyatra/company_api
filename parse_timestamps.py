import re
import pendulum

DELIMITERS = ',|"|:(?=\D)'

EX = '''2020-10-25 16:14:49.186,"+BUFF:GTDOG,F50904,015181002677699,,0,1,1,2,0.0,0,26.2,-74.436438,40.509986,20201025161205,0310,0410,0936,0C68860F,48.5,9,20201025160418,00D0$"'''


def split_line(line):
    
    # will remove the colon from the +RESP:GTFRI section, but not the server_time
    fields = re.split(DELIMITERS, line)
    
    # get rid of empty fields that took place of double quotes
    fields.pop(1)
    fields.pop(-1)
    
    # remove leading and trailing chars from respective fields
    fields[1] = [fields][1:]
    fields[-1] = fields[-1][:-1]
    
    return fields

def parse_times(fields: list) -> dict:
    '''Takes list of fields (parsed via split_line) and returns
    dictionary of the 3 relevant datetime obj with relevant tz
    '''
    aws_stamp = pendulum.parse(fields[0], tz='America/New_York')
    gps_lock = pendulum.from_format(fields[15], 'YYYYMMDDhhmmss')
    send_stamp = pendulum.from_format(fields[-2], 'YYYYMMDDhhmmss')
    return {"aws_stamp": aws_stamp, "gps_lock": gps_lock, "send_stamp": send_stamp}

def convert_server_time(timestamp):
    pass

def convert_device_time(timestamp):
    pass
    
# parse first string as server_time
# add time zone info

# parse second string into list
# find strings that are dates
# parse first date UTC as sent_time
# parse second date UTC as lock_time

# take time delta of lock_time and sent_time
# take time delta of sent_time and server_time

# write to csv
# output has these columns:
### msg_count, gps_acc, lock_time, delta, sent_time, delta, server_time, buff/resp, lat, long, msg_type, raw_data