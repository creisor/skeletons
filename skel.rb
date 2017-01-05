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
#     Chris Reisor (creisor@gmail.com)

$LOAD_PATH.unshift(File.expand_path(File.join(File.dirname(__FILE__), "../lib")))

require 'logger'
require 'optparse'

class App
  def initialize
    @log = Logger.new(STDERR)
    @log.level = Logger::WARN
    @options = {
      :verbose => false,
    }
  end

  def main
    opts = OptionParser.new do |opts|
      opts.on('-v', '--verbose', 'write debug output to stderr') do
        @options[:verbose] = true
        @log.level = Logger::DEBUG
        @log.debug "VERBOSE enabled"
      end
      opts.parse!(ARGV)
    end
  end
end

if $0 == __FILE__
  app = App.new
  app.main
end
