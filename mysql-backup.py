#!/usr/bin/env python
# -*-coding:Utf-8 -*-

import sys
import os
import getopt
import time
import tempfile
import shutil

config = {'login-path': '', 'databases': '', 'directory': ''}

def usage():
	print "Dumping structure and contents of MySQL databases."
  	print "usage: mysql-backup [options] \n"
  	print "--help                 : Display this help message and exit."
  	print "-v, --version          : Output version information and exit."
  	print "-l, --login-path=name  : Login path name."
  	print "-D, --databases=name   : databases name to dump."
  	print "-d, --directory=name   : Backup directory."

def version():
	print "Mysql Backup v1"

def listAllBackup():
	for f in os.listdir(config["directory"]):
		listBackup(f)

def listBackup(name):
	path = os.path.join(config["directory"], name)
	print name
	for d in os.listdir(path):
		print "  "+d
		subpath = os.path.join(path, d)
		for h in os.listdir(subpath):
			print "    "+h

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
				print "Export successful for database '"+database+"'"
			else:
				print "Export failed for database '"+database+"'"
		else:
			print "Export failed for database '"+database+"'"

def options():
	try:
		options, args = getopt.getopt(sys.argv[1:], "vl:B:d:", ["version", "login-path=", "databases=", "directory=", "help"])
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

options()
export()