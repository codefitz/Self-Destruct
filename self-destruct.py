# Author: Wes Moskal-Fitzpatrick
#
# This script requires a generated key to run.
#

import datetime
import sys
import os
import argparse
from argparse import RawTextHelpFormatter
import base64
import binascii
import time
import ast

pwd = os.getcwd()

#argv = sys.argv[1:] # Additional Args

parser = argparse.ArgumentParser(description='Self Destruct',formatter_class=RawTextHelpFormatter)
parser.add_argument('-k', '--key', dest='key',  type=str, required=True, help='Safety Key.', metavar='<key>')
parser.add_argument('-f', '--fakeout', dest='fakeout', action='store_true', required=False, help=argparse.SUPPRESS)

args = parser.parse_args()

now = datetime.date.today()
destroy = False
expired = False
wrong_secret = False

try:
    b64decoded = base64.b64decode(args.key)
    # base64 decode returns bytes under Python 3.  Convert to a string
    # before processing the list representation.
    decoded_str = b64decoded.decode('utf-8')
    decoded_list = decoded_str.strip('[]').replace("'", "").split(', ')
    decoded = decoded_list[0]
    expiry_time = datetime.datetime.fromtimestamp(int(float(decoded)))
    now_tuple = now.timetuple()
    timestamp = time.mktime(now_tuple)
    today = datetime.datetime.fromtimestamp(int(float(timestamp)))
    if today > expiry_time:
        expired = True
        destroy = True
    if decoded_list[1] != "random_key":
        wrong_secret = True
        destroy = True
except (ValueError, binascii.Error) as exc:
    print(f"There is a problem with the key: {exc}")
    sys.exit(1)

if args.fakeout:
    print("Debugging..")
    print("now:",now)
    print("b64decoded:",decoded_bytes)
    print("decoded_list",decoded_list)
    print("expiry_time:",expiry_time)
    print("now_tuple:",now_tuple)
    print("timestamp:",timestamp)
    print("today:",today)
    print("destroy:",destroy)
    print("expired:",expired)
    print("wrong_secret:",wrong_secret)
elif destroy:
    print("This script has expired and will now self-destruct.")
    print("Removing %s..."%sys.argv[0])
    if sys.platform == "win32":
        with open("c:\\temp\\_{0}.bat".format(args.key), 'w', encoding='utf-8') as delbat:
            delbat.write('''
                        @echo off
                        :Repeat
                        del "{0}" > nul 2> nul
                        if exist "{0}" goto Repeat
                        del "c:\temp\_{1}.bat";
                    '''.format(sys.argv[0],args.key))
        os.startfile(r"c:\temp\_{0}.bat".format(args.key))
    else: # Linux Desktop
        os.remove("%s"%sys.argv[0])
sys.exit(0)
