#!/usr/bin/perl
# $Id$

use strict;
use warnings;
use Getopt::Std;

my $foo;
my $bar;
my $DEBUG = 0;
my $VERBOSE = 0;

# Argument and option setup
#####################################################################
$main::VERSION = "0.1";
$Getopt::Std::STANDARD_HELP_VERSION = 1;
sub HELP_MESSAGE {
    print STDERR "Usage: $0 -f <foo> -b <bar> [-d] [-v] | [--help]

    -f <foo>        Some foo
    -b <bar>        Some bar
    -d              OPTIONAL: debugging mode. Will not execute commands, but will echo them.
    -v              OPTIONAL: verbose mode
    --help          Prints this message
\n"
}
#####################################################################

# Argument and option processing
#####################################################################
our($opt_f, $opt_b, $opt_d, $opt_v);
getopts('f:b:dv');

# require option arguments
exit HELP_MESSAGE() unless defined($opt_f) && defined($opt_b);

# Process the args
$foo = $opt_f;
$bar = $opt_b;

if (defined($opt_d)) {
    $DEBUG = 1;
}
if (defined($opt_v)) {
    $VERBOSE = 1;
}
#####################################################################

# Subroutines
#####################################################################
sub print_v {
    $VERBOSE && print "VERBOSE: @_";
}

sub print_d {
    $DEBUG && print "DEBUG: @_";
}

sub run_cmd {
    # runs a simple shell command
    my $output = '';
    my $cmd = "@_";
    $DEBUG ? &print_d("$cmd\n") : system(split(' ', $cmd));
}
#####################################################################


# MAIN
#####################################################################

sub main {
    print_v "This is a verbose statement\n";
    print_d "This is a debugging statement\n";

    print "foo is set to: $foo\n";
    print "bar is set to: $bar\n";

    my $cmd = 'ls -l';
    &run_cmd($cmd);

    my $bad_cmd = "foobar";
    &run_cmd($bad_cmd);

    my $exit_code = $?;
    if ($exit_code) {
        print "Bad exit from command.  exit_code: $exit_code\n";
    }
}

&main
