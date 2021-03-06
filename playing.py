#!/usr/bin/python
import json
from os.path import expanduser
import sys
import argparse

home = expanduser("~")
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, description="Parses and print Google Play Music Desktop Player song info")

def parseJson():
    try:
        with open(home + '/.config/Google Play Music Desktop Player/json_store/playback.json') as f:
            data = f.read()
    except:
        with open(home + '/GPMDP_STORE/playback.json') as f:
            data = f.read()
    return json.loads(data)

def getSong(data):
    return data['song']['title']

def getAlbum(data):
    return data['song']['album']

def getArtist(data):
    return data['song']['artist']

def convert_time(ms):
    x = ms / 1000
    x % 60
    m, s = divmod(x, 60)
    return "%d:%02d" % (m, s)
def getProgress(data):
    cur = data['time']['current']
    total = data['time']['total']
    return convert_time(cur) + "/" + convert_time(total)

def parseLayout(layout):
    displaystr = ""
    for i in layout:
        if i == 't':
            displaystr += getSong(data)
        elif i == 'a':
            displaystr += getAlbum(data)
        elif i == 'A':
            displaystr += getArtist(data)
        elif i == 'p':
            displaystr += getProgress(data)
        elif i == '-':
            displaystr += " - "
    return displaystr

def truncate(displaystr, trunclen):
    if len(displaystr) > trunclen:
        displaystr = displaystr[:trunclen]
        displaystr += '...'
        if ('(' in displaystr) and (')' not in displaystr):
            displaystr += ')'
    return displaystr

def run(data, layout, notplaying, trunclen):
    displaystr = ""
    if data['playing']:
        displaystr = parseLayout(layout)
    else:
        sys.stdout.write("")
    if sys.version[0] == '2':
        displaystr = displaystr.encode('utf-8')

    if not displaystr and notplaying:
        print("Not Playing")
    else:
        if trunclen is None:
            print(displaystr)
        else:
            print(truncate(displaystr, trunclen))

parser.add_argument("-l",
        "--layout",
        action="store",
        metavar="layout",
        help="t = Song Title\na = Song Album\nA = Artist Name\np = Track time progess\n- = Spacer\nExample: t-a-A-p",
    )
parser.add_argument("-t",
        "--trunclen",
        metavar="trunclen",
        type=int,
        help="Truncate the output"
    )
parser.add_argument("--not-playing",
        action="store_true",
        dest="notplaying",
        help="Display the text 'Not Playing' when no music is playing",
    )
args = parser.parse_args()
data = parseJson()
try:
    run(data, args.layout, args.notplaying, args.trunclen)
except:
    run(data, "t-a-A-p", False)
