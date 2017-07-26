#!/bin/python

import pexpect
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description='SSH passwordless')
    parser.add_argument('--ip', action='store', dest="ip", help="IP address of target server")
    parser.add_argument('--username', action='store', default="root", dest="username", help="username of target server")
    parser.add_argument('--password', action='store', dest="password", help="password of target server")
    args = parser.parse_args()

    copyID = passwodLessSSH(args.ip, args.username, args.password)
    if not copyID.validate_params():
        parser.print_help()
        sys.exit(1)

    copyID.swap_keys()

class passwodLessSSH(object):

    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password

    def validate_params(self):
        """
        This function validate the input parameters
        :param args: input parameters
        :return: is valid (True or False)
        """
        is_valid = True

        try:
            assert isinstance(self.ip, str), "No IP was supplied"
            assert isinstance(self.username, str), "No username was supplied"
            assert isinstance(self.password, str), "No password was supplied"
        except Exception as ex:
            print ex.message
            is_valid = False
        finally:
            return is_valid

    def swap_keys(self):
        """
        This function acctially do the key swap
        :param ip: Remote server ip
        :param username: user for remote server
        :param password: password for remote server
        :return: None
        """

        console = pexpect.spawn("ssh-copy-id {user}@{ip}".format(user=self.username, ip=self.ip))
        console.logfile = sys.stdout
        console.expect(" (yes/no)?")
        console.send("yes\n")
        console.expect("password:")
        console.send("{password}\n".format(password=self.password))
        console.expect("you wanted were added")
        print console.after


if __name__ == "__main__":
    main()