import argparse
import ProcessPortProtectionServer


def read_key_from_file(file):
    with open(file) as f:
        return f.readline()


# ppp -i [interface] -p [listen port] -pp [protected port] [command]

parser = argparse.ArgumentParser()
parser.add_argument('-v', '--verbose', action='store_true', help='show debug information')
parser.add_argument('-i', '--interface', metavar='interface', help='interface')
parser.add_argument('-p', '--port', type=int, metavar='port', help='listen port')
parser.add_argument('-pp', '--protect', type=int, metavar='port', help='port to protect')
parser.add_argument('-k', '--key', metavar='key', help='access key, default is 123')
parser.add_argument('-f', '--file', metavar='file', help='access key file with single line password in it')

args = parser.parse_args()

key = args.key

if args.file:
    key = read_key_from_file(args.file)

if args.port and args.interface and args.protect:
    ppp = ProcessPortProtectionServer.ProcessPortProtectionServer(args.port, args.interface, args.protect, key, args.verbose)
    try:
        ppp.start()
    except KeyboardInterrupt as e:
        print("Ctrl C pressed, exit")
        exit()

else:
    parser.print_help()
