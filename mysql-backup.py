#!/usr/bin/env python

import sys
import os
import getopt
import time
import tempfile
import shutil
from datetime import date
from datetime import datetime

config = {'login-path': '', 'databases': '', 'directory': '', 'max-days': 15}

def usage():
	print "Dumping structure and contents of MySQL databases."
  	print "usage: mysql-backup [options] \n"
  	print "--help                 : Display this help message and exit."
  	print "-v, --version          : Output version information and exit."
  	print "-l, --login-path=name  : Login path name."
  	print "-D, --databases=name   : databases name to dump."
  	print "-d, --directory=path   : Backup directory."
  	print "-m, --max-days=days    : Maximum days of backup (default 15 days)."

def version():
	print "Mysql Backup v2"

def export():
	databases = config['databases'].split()

	if(len(databases) == 0):
		print "You have to specifie which databases you want to export"
		sys.exit()

	for database in databases:
		args = ""

		if(config['login-path'] != ""):
			args = args+" --login-path='"+config['login-path']+"'"

		args = args+" "+database

		tmpFile, tmpFilePath = tempfile.mkstemp()
		args = args+" > "+tmpFilePath

		cmd = "mysqldump{0}".format(args)

		if(os.system(cmd) == 0):
			path = os.path.join(config["directory"], database)
			path = os.path.join(path, time.strftime("%d-%m-%Y"))

			if(not(os.path.exists(path))):
				os.makedirs(path)

			path = os.path.join(path, time.strftime("%H:%M:%S")+".sql")

			shutil.move(tmpFilePath, path)

			if os.path.isfile(path):
				cleanup(database)
				print "Export successful for database '"+database+"'"
			else:
				print "Export failed for database '"+database+"'"
		else:
			print "Export failed for database '"+database+"'"

def cleanup(database):
	today = date.today()
	min_date = today.replace(day= today.day-config["max-days"])

	path = os.path.join(config["directory"], database)

	for day in os.listdir(path):
		full_date = datetime.strptime(day, "%d-%m-%Y").date()

		if full_date < min_date:
			shutil.rmtree(os.path.join(path, day))

def options():
	try:
		options, args = getopt.getopt(sys.argv[1:], "vl:B:d:m:", ["version", "login-path=", "databases=", "directory=", "max-days=", "help"])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	else:
		for key, value in options:
			if(key in ['-v', '--version']):
				version()
				sys.exit()
			elif(key == "--help"):
				usage()
				sys.exit()
			elif(key in ['-l', '--login-path']):
				config["login-path"] = value
			elif(key in ['-B', '--databases']):
				config["databases"] = value
			elif(key in ['-d', '--directory']):
				config["directory"] = value
			elif(key in ['-m', '--max-days']):
				config["max-days"] = int(value)

options()
export()