#!/usr/bin/python
# $Id:$
__author__ = "Chris Reisor"
__version__ = "0.0"

import os, sys, pdb, pprint, pwd, logging
from logging.handlers import SysLogHandler
from optparse import OptionParser
import subprocess

class SkelClass(object):
    def __init__(self, foo, bar):
        self.__foo = foo
        self.__bar = bar
        self.loglevel = logging.WARNING # the default log level
        self.logger = logging.getLogger(os.path.basename(__file__))
        self.verbose = False
        self.debug = False

    # Property methods
    #-----------------------------------------------------#
    def __get_foo(self):
        return self.__foo

    def __set_foo(self, val):
        self.print_v("setting foo to: %s" % val)
        self.__foo = val

    def __get_bar(self):
        return self.__bar

    def __set_bar(self, val):
        self.print_v("setting bar to: %s" % val)
        self.__bar = val
    #-----------------------------------------------------#

    # Properties
    #-----------------------------------------------------#
    foo = property(__get_foo, __set_foo)
    bar = property(__get_bar, __set_bar)
    #-----------------------------------------------------#

    def get_runner(self):
        user = pwd.getpwuid(os.geteuid())[0]
        return user

    def print_v(self, string):
        self.logger.debug(string)

    def print_d(self, string):
        self.logger.info(string)

    def run_cmd(self, cmd):
        results = { 'exit_code': None,
                    'stdout': None,
                    'stderr':None}
        if self.debug is True:
            self.print_d(cmd)
            return results
        else:
            p_cmd = cmd.split(' ')
            try:
                p = subprocess.Popen(   p_cmd,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        close_fds=True)
            except OSError, e:
                results['exit_code'] = e.errno
                results['stderr'] = e.strerror
                return results

            results['stdout'] = p.stdout.read().rstrip()
            results['stderr'] = p.stderr.read().rstrip()
            p.stdout.close()
            p.stderr.close()

            results['exit_code'] = p.wait()
            return results

    def configure_options(self):

        desc = "This program can both foo and bar."
        epilog="""
Examples:
    %prog -f spam -b eggs -v
    %prog -f spam -v -d

"""
        class MyParser(OptionParser):
            def format_epilog(self, formatter):
                return self.epilog

        opt_parser = MyParser(epilog=epilog, description=desc)

        msg = 'An option that takes an argument'
        opt_parser.add_option('-f', '--foo', help=msg)

        msg = 'Another option that takes an argument'
        opt_parser.add_option('-b', '--bar', help=msg)

        msg = 'Enable logging to syslog in addition to the screen'
        opt_parser.add_option('-l', '--log', help=msg, action="store_true")

        msg = 'Turns on verbosity'
        opt_parser.add_option('-v', '--verbose', help=msg, action="store_true")

        msg = 'Debugging mode.  Will not execute commands, but will print them'
        opt_parser.add_option('-d', '--debug', help=msg, action="store_true")

        (options, args) = opt_parser.parse_args()

        self.verbose = options.verbose or False
        self.debug = options.debug or False

        if options.debug is True:
            self.debug = True
            # DEBUG messages will go to the INFO log
            self.loglevel = logging.INFO

        # we have to set DEBUG after setting INFO because it is a lower level
        if options.verbose is True:
            # VERBOSE messages will go to the DEBUG log
            self.loglevel = logging.DEBUG

        # now set up logging
        self.logger.setLevel(self.loglevel)
        console = logging.StreamHandler()
        console.setLevel(self.loglevel)
        console_formatter = logging.Formatter('%(levelname)s: %(message)s')
        console.setFormatter(console_formatter)
        self.logger.addHandler(console)
        # if the user specified to write to log:
        if options.log is True:
            syslog = SysLogHandler(address='/dev/log')
            syslog_formatter = logging.Formatter('%(name)s: %(levelname)s: %(message)s')
            syslog.setFormatter(syslog_formatter)
            self.logger.addHandler(syslog)
            self.print_v("Logging to syslog")

        self.foo = options.foo or None
        self.bar = options.bar or None

    def main(self):
        """An example implementation of this module.  There is no need to run
        main.  You could always define your own and run that."""
        self.configure_options()
        self.print_v("This is a verbose message")
        self.print_d("This is a debugging message")
        if self.foo:
            print "Foo is set to: %s" % self.foo
        if self.bar:
            print "Bar is set to: %s" % self.bar
        if not self.foo and not self.bar:
            print "Neither foo nor bar are set"

        cmd = 'ls -l /tmp'
        results = self.run_cmd(cmd)
        if results['exit_code'] is not None:
            print "\nRan command: %s" % cmd
            for key in results.keys():
                print "%s:\n" % key + '-' * 50
                print "%s" % results[key]


if __name__ == "__main__":
    skel = SkelClass('foo', 'bar')
    print "--> Running as user: %s <--" % skel.get_runner()

    # here's a trick for overriding or imitating the commandline args:
    #sys.argv.append('-v')
    skel.main()
