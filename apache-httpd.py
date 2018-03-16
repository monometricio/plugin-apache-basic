#!/opt/mm-agent/python/bin/python2
import os
import re
import sys
import urllib2

interestingKeys = {
    'Total Accesses': '_counter.apache.requests_per_sec',
    'Total kBytes': '_counter.apache.kb_per_sec',
    'BusyWorkers': 'apache.busy_workers',
    'IdleWorkers': 'apache.idle_workers',
}

scoreboardCharToStatus = {
    '_' : 'apache.workers.waiting_for_connection',
    'R' : 'apache.workers.reading',
    'W' : 'apache.workers.sending_reply',
    'K' : 'apache.workers.keepalive',
    'D' : 'apache.workers.dns_lookup',
    'C' : 'apache.workers.closing',
    'L' : 'apache.workers.login',
    'G' : 'apache.workers.gracefully_finishing',
    'I' : 'apache.workers.idle_cleanup',
    '.' : 'apache.workers.open_slot',
}

scoreboardCharToCount = { }

try:
    lines = urllib2.urlopen(os.environ['MMIO_HTTPD_URL']).readlines()
except Exception as e:
    sys.stderr.write("Couldn't fetch status page: " + str(e) + "\n")
    sys.exit(1)

def parseScoreboard(value):
    for char in value:
        if not char in scoreboardCharToStatus:
            continue
        if not char in scoreboardCharToCount:
            scoreboardCharToCount[char] = 0
        scoreboardCharToCount[char] += 1
    for char in scoreboardCharToCount:
        print "%s: %s" % (scoreboardCharToStatus[char], scoreboardCharToCount[char])

for line in lines:
    matches = re.match(r'([\w ]+):\s*([\d.]+)', line)
    if matches:
        if matches.group(1) in interestingKeys:
            print "%s: %s" % (interestingKeys[matches.group(1)], matches.group(2))
            continue
    if line.startswith('Scoreboard: '):
        value = line[len('Scoreboard: '):]
        parseScoreboard(value)

