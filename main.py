#!/bin/python

import pexpect
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description='Ansible inventory creator')
    parser.add_argument('--ip', action='store', dest="ip", help="IP address of target server")
    parser.add_argument('--username', action='store',default="root", dest="username", help="username of target server")
    parser.add_argument('--password', action='store', dest="password", help="password of target server")
    args = parser.parse_args()
    try:
        assert isinstance(args.ip, str), "No IP was supplied"
        assert isinstance(args.username, str), "No username was supplied"
        assert isinstance(args.password, str), "No password was supplied"
    except Exception as ex:
        print ex.message
        parser.print_help()

    console = pexpect.spawn("ssh-copy-id {user}@{ip}".format(user=args.username, ip=args.ip))
    console.logfile = sys.stdout
    console.expect(" (yes/no)?")
    console.send("yes\n")
    console.expect("password:")
    console.send("{password}\n".format(password=args.password))
    console.expect("you wanted were added")
    print console.after

if __name__ == "__main__":
    main()