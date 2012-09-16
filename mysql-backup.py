#!/usr/bin/env python
# -*-coding:Utf-8 -*-

import sys
import os
import getopt
import time
import tempfile
import shutil

config = {'host': '', 'user': '', 'password': False, 'database': '', 'directory': '', 'import': False, 'export': True}

def usage():
	print "By Jamal Youssefi"
	print "Dumping structure and contents of MySQL databases."
  	print "usage: mysql-backup [options] \n"
  	print "--help                 : Display this help message and exit."
  	print "-v, --version          : Output version information and exit."
  	print "--list=name            : List dump file for database 'name' in backup directory."
  	print "--list-all             : List dump file for all databases in backup directory."
  	print "-h, --host=name        : Connect to host."
  	print "-u, --user=name        : User for login if not current user."
  	print "-p, --password         : If need password."
  	print "-d, --database=name    : Dump several databases. Note the difference in usage; in this case no tables are given. All name arguments are regarded as database names. 'USE db_name;' will be included in the output."
  	print "-D, --directory=name   : Backup directory."
  	print "-i, --import           : Import action."
  	print "-e, --export           : Export action. (default action)"

def version():
	print "mysql-backup.py v1"

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

def exportDatabase():

	database = config['database']

	if(database == ""):
		print "You have to specifie which database you want to export"
		sys.exit()

	args = ""

	if(config['host'] != ""):
		args = args+"-h "+config['host']+" "

	if(config['user'] != ""):
		args = args+"-u "+config['user']+" "

	if(config['password'] == True):
		args = args+"-p "

	args = args+"-B "+config['database']+" "

	tmpFile, tmpFilePath = tempfile.mkstemp()
	args = args+" > "+tmpFilePath
		
	cmd = "mysqldump {0}".format(args)

	if(os.system(cmd) == 0):
		path = os.path.join(config["directory"], config['database'])
		path = os.path.join(path, time.strftime("%d-%m-%Y"))
	
		if(not(os.path.exists(path))):
			os.makedirs(path)

		path = os.path.join(path, time.strftime("%H:%M:%S")+".sql")

		shutil.move(tmpFilePath, path)

		if os.path.isfile(path): 
			print "Database export successful !"
		else:
			print "Database export failed !"			
	else:
		print "Database export failed !"

def importDatabase():
	pass

def loadOptions():
	try:                                
		options, args = getopt.getopt(sys.argv[1:], "vh:u:pd:D:ie", ["version", "list=", "list-all", "host=", "user=", "password", "database=", "directory=", "import", "export", "help"])
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
			elif(key == "--list"):			
				listBackup(value)
				sys.exit()
			elif(key == "--list-all"):			
				listAllBackup()
				sys.exit()
			elif(key in ['-h', '--host']):
				config["host"] = value	
			elif(key in ['-u', '--user']):
				config["user"] = value	
			elif(key in ['-p', '--password']):
				config["password"] = True	
			elif(key in ['-d', '--database']):
				config["database"] = value
			elif(key in ['-D', '--directory']):
				config["directory"] = value
			elif(key in ['-i', '--import']):
				config["import"] = True
				config["export"] = False
			elif(key in ['-e', '--export']):
				config["export"] = True

		if(config['export'] and config['import']):
			print "Can't use options import and export in same time."
			print "use option --help to display help message."
			sys.exit()

def loadConfig():
	try:

  		with open("/etc/mysql-backup.conf", "r") as f:
			for line in f.readlines():

				line_config = line.rstrip("\n").split("=");
				
				key = line_config[0]	
				value = line_config[1]

				if(key in config and value):
					if(key == "password"):
						config[key] = bool(value)
					else:
						config[key] = value	

	except IOError as e:
		print "Fichier de config manquant. ({0})".format(e.strerror)	

loadConfig()
loadOptions()

if(config['import']):
	importDatabase()
elif(config['export']):
	exportDatabase()
else:
	sys.exit()

