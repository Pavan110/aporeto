import sys
import os

args = sys.argv
file_to_save = None
verbose_flag = False
prompt = False
help_flag = False

if len(args)>0:
	args.remove(args[0])

class Constants():
	create_file = "--create-file"
	no_prompt = "--no-prompt"
	verbose = "-verbose"
	help = "--help"
	args_h = "-h"
	invalid_arg_prefix = "-"

def create_file_args(arg_to_parse):
	if Constants.create_file in arg_to_parse:
		return True, arg_to_parse.split("=")[1]
	return False, None

def print_logs(print_str, force_log=False):
	if verbose_flag or force_log:
		print print_str

def call_help():
	print_logs("Help", force_log=True)
	print_logs("args				Description", force_log=True)
	print_logs("%s		Create file"%Constants.create_file, force_log=True)
	print_logs("%s		No prompt"%Constants.no_prompt, force_log=True)
	print_logs("%s		Verbose"%Constants.verbose, force_log=True)
	exit(0)

def call_invalid_argument():
	print_logs("Bad command: one or more invalid arguments passed", force_log=True)
	exit(2)

args_for_loop = list(args)
for arg in args_for_loop:
	create_file_flag, file_name = create_file_args(arg)
	if create_file_flag:
		file_to_save = file_name
		args.remove(arg)
	elif arg == Constants.verbose:
		verbose_flag = True
		args.remove(arg)
	elif arg == Constants.no_prompt:
		prompt = True
		args.remove(arg)
	elif arg == Constants.args_h or arg == Constants.help:
		call_help()
		args.remove(arg)
	elif Constants.invalid_arg_prefix in arg[0]:
		call_invalid_argument()
		args.remove(arg)

if file_to_save is None:
	print_logs("Save file missing, exiting", force_log=True)
	exit(2)

if os.path.exists(file_to_save):
	if not prompt:
		prompt_input = raw_input('File exists. Overwrite (y/n) ?')
		if prompt_input == "n":
			print_logs("Exiting", force_log=True)
			exit(1)
		elif prompt_input == "y":
			print_logs("Overwriting file")

f = open(file_to_save, 'w+')
print_logs("Opening file for write operation %s" %file_to_save)
for arg in args:
	f.write("%s\n"%arg)
f.close()
print_logs("Closing file")
