import argparse
import subprocess


def argsparsevalidation():
    parser = argparse.ArgumentParser(description='Script to run attacks')
    parser.add_argument('-n', '--numcont', help='Number of containers', required=True)
    parser.add_argument('-c', '--command', help='Command of attack', required=True)
    parser.add_argument('-s', '--status', help='start or stop', required=True)

    args = parser.parse_args()
    return args


def main():
    args = argsparsevalidation()
    command = args.command

    if args.status == 'start':
        for i in range(1, int(args.numcont) + 1):
            startcom = f"lxc start kali-c{i}"
            startcom = startcom.split()
            subprocess.Popen(startcom, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        for i in range(1, int(args.numcont) + 1):
            attackcom = f"lxc exec kali-c{i} -- {command}"
            attackcom = attackcom.split()
            print(attackcom)
            subprocess.Popen(attackcom, stdin=subprocess.PIPE,
             stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    elif args.status == 'stop':

        for i in range(1, int(args.numcont) + 1):
            stopcom = f"lxc stop kali-c{i}"
            stopcom = stopcom.split()
            print(stopcom)
            subprocess.Popen(stopcom, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)

if __name__ == '__main__':
    main()
