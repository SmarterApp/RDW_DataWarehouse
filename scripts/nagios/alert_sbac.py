#! /bin/env python

import json
import http.client, urllib3, urllib

def parse_args():

    pass

def format_air_msg():
    msg = {'a':{'test':'b'}}

    return json.dumps(msg)

def send_alert():
    msg = format_air_msg()
    print(msg)
    print('ALERT SENT')


if __name__ == '__main__':
    parse_args()
    send_alert()