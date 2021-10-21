#!/usr/bin/env python3
# Start/Stop tcpreplay

import argparse
from subprocess import STDOUT, run


def start():
    try:
        stop()
        run('cd /root && screen -dmSL tcp-replay tcpreplay -i sw1 --stats=10 AppDDos_rw.pcap', stderr=STDOUT, shell=True)
    except Exception as ex:
        print(ex)
        run('cd /root && screen -dmSL tcp-replay tcpreplay -i sw1 --stats=10 AppDDos_rw.pcap', stderr=STDOUT, shell=True)


def stop():
    try:
        run('killall screen', stderr=STDOUT, shell=True)
        #run('screen -S s-tcpreplay -X quit', stderr=STDOUT, shell=True)
    except Exception as ex:
        print(ex)


def main():
    parser = argparse.ArgumentParser(description="Smart-Defender System")
    parser.add_argument('-c', '--command', help='Start tcpreplay', required=False)
    args = parser.parse_args()

    cmd = 'start'
    if args.command:
        cmd = args.command

    if 'start' in cmd.lower():
        start()
    else:
        stop()


if __name__ == "__main__":
    main()