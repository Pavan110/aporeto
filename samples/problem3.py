import sys
import os
import urllib2
import re

args = sys.argv
urls_to_open = None
verbose_flag = False
help_flag = False

if len(args)>0:
	args.remove(args[0])

class Constants():
	create_file = "-urls"
	verbose = "-verbose"
	help = "--help"
	args_h = "-h"
	invalid_arg_prefix = "-"

def parse_url_args(arg_to_parse):
	if Constants.create_file in arg_to_parse:
		return True, arg_to_parse.split("=")[1].split(",")
	return False, None

def print_logs(print_str, force_log=False):
	if verbose_flag or force_log:
		print print_str

def call_help():
	print_logs("Help", force_log=True)
	print_logs("args				Description", force_log=True)
	print_logs("%s		Create file"%Constants.create_file, force_log=True)
	print_logs("%s		Verbose"%Constants.verbose, force_log=True)
	exit(0)

def call_invalid_argument():
	print_logs("Bad command: one or more invalid arguments passed", force_log=True)
	exit(2)

args_for_loop = list(args)
for arg in args_for_loop:
	create_file_flag, urls_list = parse_url_args(arg)
	if create_file_flag:
		urls_to_open = urls_list
		args.remove(arg)
	elif arg == Constants.verbose:
		verbose_flag = True
		args.remove(arg)
	elif arg == Constants.args_h or arg == Constants.help:
		call_help()
		args.remove(arg)
	elif Constants.invalid_arg_prefix in arg[0]:
		call_invalid_argument()
		args.remove(arg)

if urls_to_open is None:
	print_logs("Missing urls, exiting", force_log=True)
	exit(2)

word_count_dict = {}

for url in urls_to_open:
	url_data = urllib2.urlopen(url)
	print_logs("Opening file for write operation %s" %urls_to_open)
	for data in url_data:
		data_words = data.split(" ")
		for w in data_words:
			try:
				word_count_dict[w] += 1
			except KeyError:
				word_count_dict[w] = 1

for word, count in word_count_dict.iteritems():
	if word.isalnum():
		print word, ": ", count




