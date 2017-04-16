iimport sys
import os

args = sys.argv
file_to_open = ten
file_to_return = None
prompt = False
verbose_flag = False
help_flag = False
seen_lines = set()

if len(args)>0:
	args.remove(args[0])

class Constants():
	open_file = "--file"
	save_file = "--output"
	no_prompt = "--no-prompt"
	verbose = "-verbose"
	help = "--help"
	args_h = "-h"
	invalid_arg_prefix = "-"

def file_args(arg_to_parse):
	if Constants.open_file in arg_to_parse:
		return True, False, arg_to_parse.split("=")[1]
	elif Constants.save_file in arg_to_parse:
		return False, True, arg_to_parse.split("=")[1]
	return False, False, None

def print_logs(print_str, force_log=False):
	if verbose_flag or force_log:
		print print_str

def call_help():
	print_logs("Help", force_log=True)
	print_logs("args				Description", force_log=True)
	print_logs("%s		Open file"%Constants.open_file, force_log=True)
	print_logs("%s		Save file"%Constants.save_file, force_log=True)
	print_logs("%s		No prompt"%Constants.no_prompt, force_log=True)
	print_logs("%s		Verbose"%Constants.verbose, force_log=True)
	exit(0)

def call_invalid_argument():
	print_logs("Bad command: one or more invalid arguments passed", force_log=True)
	exit(2)

args_for_loop = list(args)
for arg in args_for_loop:
	open_file_flag, save_file_flag, file_name = file_args(arg)
	if open_file_flag:
		file_to_open = file_name
		args.remove(arg)
	elif save_file_flag:
		file_to_return = file_name
		args.remove(arg)
	elif arg == Constants.no_prompt:
		prompt = True
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

if file_to_open is None:
	print_logs("Requested file to open is missing, exiting", force_log=True)
	exit(2)

if not os.path.exists(file_to_open):
	print_logs("File does not exists", force_log=True)
	exit(1)

if file_to_return is None:
	print_logs("Requested filename of output is missing, exiting", force_log=True)
	exit(2)

if os.path.exists(file_to_return):
	if not prompt:
		prompt_input = raw_input('Return file exists. Overwrite (y/n) ? FileName: %s'%file_to_return)
		if prompt_input == "n":
			print_logs("Exiting", force_log=True)
			exit(1)
		elif prompt_input == "y":
			print_logs("Overwriting file")

f = open(file_to_open, 'r')
r = open(file_to_return, 'w+')
print_logs("Opening file for read operation %s" %file_to_open)
print_logs("Opening file for write operation %s" %file_to_return)
for line in f:
	if line not in seen_lines:
		seen_lines.add(line)
		r.write(line)
f.close()
r.close()
print_logs("Closing file : %s"%file_to_open)
print_logs("Closing file : %s"%file_to_return)
