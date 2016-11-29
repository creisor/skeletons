#!/usr/bin/env ruby

# === NAME
#
#     script_name - brief script description goes here
#
# === SYNOPSIS
#
#     usage: script_name [-h|-v] arg
#
# === DESCRIPTION
#
# Detailed description goes here
#
# === AUTHOR
#
#     Chris Reisor (creisor@groupon.com)

$LOAD_PATH.unshift(File.expand_path(File.join(File.dirname(__FILE__), "../lib")))

require 'logger'
require 'optparse'

ME = File.basename $0

$Log = Logger.new(STDERR)
$Log.level = Logger::WARN

options = {
  :verbose => false,
  :something => 'default',
}


def main
  opts = OptionParser.new do |opts|
    opts.on('-h', '--help', 'display this help text and exit') do
    end
    opts.on('-f', '--somearg SOMETHING', 'option that takes an argument') do |something|
      options[:something] = something
    end
    opts.on('-v', '--verbose', 'write debug output to stderr') do
      options[:verbose] = true
      $Log.level = Logger::DEBUG
      $Log.debug "VERBOSE enabled"
    end
    opts.parse!(ARGV)
  end
end

if $0 == __FILE__
  main
end
