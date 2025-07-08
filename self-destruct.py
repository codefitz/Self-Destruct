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
import time
import ast

pwd = os.getcwd()

#argv = sys.argv[1:] # Additional Args

parser = argparse.ArgumentParser(description='Self Destruct',formatter_class=RawTextHelpFormatter)
parser.add_argument('-k', '--key', dest='key',  type=str, required=True, help='Safety Key.', metavar='<key>')
parser.add_argument('-f', '--fakeout', dest='fakeout', action='store_true', required=False, help=argparse.SUPPRESS)

global args
args = parser.parse_args()

now = datetime.date.today()
destroy = False
expired = False
wrong_secret = False

try:
    decoded_bytes = base64.b64decode(args.key)
    decoded_str = decoded_bytes.decode('utf-8')
    decoded_list = ast.literal_eval(decoded_str)
    expiry_time = datetime.datetime.fromtimestamp(int(float(decoded_list[0])))
    now_tuple = now.timetuple()
    timestamp = time.mktime(now_tuple)
    today = datetime.datetime.fromtimestamp(int(float(timestamp)))
    if today > expiry_time:
        expired = True
        destroy = True
    if decoded_list[1] != "random_key":
        wrong_secret = True
        destroy = True
except:
    print("There is a problem with the key!")
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
        delbat = open("c:\\temp\\_{0}.bat".format(args.key),'w+')
        delbat.write('''
                        @echo off
                        :Repeat
                        del "{0}" > nul 2> nul
                        if exist "{0}" goto Repeat
                        del "c:\temp\_{1}.bat";
                    '''.format(sys.argv[0],args.key))
        delbat.close()
        os.startfile(r"c:\temp\_{0}.bat".format(args.key))
    else: # Linux Desktop
        os.remove("%s"%sys.argv[0])
sys.exit(0)