#!/usr/bin/python3
# $Id:$

__author__ = "Chris Reisor"
__version__ = "0.1"

import argparse
import logging
import os
import pwd

class SkelClass(object):
    """SkelClass holds the configuration data application logic for the application"""
    def __init__(self, log_level=logging.WARNING):
        self.log_level = log_level

    def get_runner(self):
        """returns the username of the user running the application"""
        return pwd.getpwuid(os.geteuid())[0]

    def configure(self):
        """configures application based on user-provided and default options"""
        parser = argparse.ArgumentParser()
        parser.add_argument("echo", help="provide a string to echo")
        parser.add_argument("-V", "--verbose", help="increase logging verbosity (INFO)", action="store_true")
        parser.add_argument("-D", "--debug", help="more verbose than 'verbose' (DEBUG)", action="store_true")

        self.args = parser.parse_args()

        if self.args.verbose:
            self.log_level = logging.INFO
        if self.args.debug:
            self.log_level = logging.DEBUG

    def run_echo(self):
        print(self.args.echo)

    def main(self):
        self.configure()

        logging.basicConfig(level=self.log_level,
                format='%(asctime)s: %(levelname)s: %(message)s')
        logging.debug('debug logging enabled')
        logging.info(f'runner: {self.get_runner()}')

        self.run_echo()

if __name__ == "__main__":
    app = SkelClass()
    app.main()
