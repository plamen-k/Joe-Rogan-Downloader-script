#! /usr/bin/python

import sys, getopt, os, urllib, hashlib, requests, time
from sqlite_plugin import read_checksum, write_checksum
from helpers import fork, parse_args
QUEUE = 10
processes = []
def main(argv):
    opts, args = getopt.getopt(argv,"hi:o:",["help","ofile="])
    episode_to = 0
    episode_from = 0

    from_ep, to_ep = parse_args(argv)
    for episode in range(from_ep,to_ep+1):
        processes.append(fork(episode))
        if len(processes) % QUEUE == 0:
            for pid in processes:
                pid, status = os.waitpid(pid, 0)
                processes.remove(pid)
            # sleep a bit (don't upset the servers) :)

    for pid in processes:
        pid, status = os.waitpid(pid, 0)
        processes.remove(pid)
    sys.exit(0)





if __name__ == '__main__':
    main(sys.argv[1:])
