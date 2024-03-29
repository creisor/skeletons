#!/bin/bash

set -o nounset
set -o errexit
set -o pipefail
shopt -s lastpipe
shopt -s inherit_errexit

## Test for root
#test $UID -eq 0 || (echo "Must be run as root" && exit 1)

# GLOBALS ############################################
VERBOSE=0
DEBUG=0
FOO=''
# Allow for overriding BAR on the commandline
: ${BAR='default'}
######################################################

usage () {
    echo "NAME:
    ${0##*/}

USAGE:

    ${0##*/} -f <foo> [-d] [-v]

Brief description goes here

OPTIONS:

    -f <foo>                An option that takes an arg
    -v                      Enable verbose mode, for debugging
    -d                      Enable debugging mode.  Will not execute commands, but will echo them.
    -h                      Prints this menu"
}

echo_v () {
    # echo only in verbose mode
    [ ${VERBOSE} -eq 1 ] && echo "VERBOSE: $*"
}

echo_d () {
    # echo only in debug mode
    [ ${DEBUG} -eq 1 ] && echo "DEBUG: $*"
}

run_cmd () {
    # run the command when *not* in debug mode
    [ ${DEBUG} -eq 1 ] && echo_d $* || eval $*
}

# Get commandline options and args
############################################################
while getopts "f:dvh" Option; do
    case $Option in
        f ) FOO=$OPTARG ;;
        d ) DEBUG='1' ;;
        v ) VERBOSE='1' ;;
        h ) usage 
            exit 0
            ;;
        * ) usage 
            exit 1
            ;;
    esac
done
############################################################

if [ ${DEBUG} -eq 1 ]; then
  set -x
fi

main () {

    echo_v "This is a verbose echo"
    echo_d "This is a debugging echo"
    echo "This is your average echo"

    if [ -n "${FOO}" ]; then
        echo "You passed '$FOO' to the -f flag"
    fi

    echo "I'm going to run an 'ls' command, unless we're in debugging mode"
    cmd="ls -l ~"
    run_cmd $cmd
}

# run the main function 
main
