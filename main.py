#!/bin/python

import pexpect
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description='Ansible inventory creator')
    parser.add_argument('--ip', action='store', dest="ip", help="IP address of target server")
    parser.add_argument('--username', action='store', default="root", dest="username", help="username of target server")
    parser.add_argument('--password', action='store', dest="password", help="password of target server")
    args = parser.parse_args()

    if not validate_params(args):
        parser.print_help()
        sys.exit(1)

    swap_keys(args.ip, args.username, args.password)

def validate_params(args):
    """
    This function validate the input parameters
    :param args: input parameters
    :return: is valid (True or False)
    """
    is_valid = True

    try:
        assert isinstance(args.ip, str), "No IP was supplied"
        assert isinstance(args.username, str), "No username was supplied"
        assert isinstance(args.password, str), "No password was supplied"
    except Exception as ex:
        print ex.message
        is_valid = False
    finally:
        return is_valid

def swap_keys(ip, username, password):
    """
    This function acctially do the key swap
    :param ip: Remote server ip
    :param username: user for remote server
    :param password: password for remote server
    :return: None
    """
    
    console = pexpect.spawn("ssh-copy-id {user}@{ip}".format(user=username, ip=ip))
    console.logfile = sys.stdout
    console.expect(" (yes/no)?")
    console.send("yes\n")
    console.expect("password:")
    console.send("{password}\n".format(password=password))
    console.expect("you wanted were added")
    print console.after


if __name__ == "__main__":
    main()