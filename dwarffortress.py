#!/bin/python3

import sqlite3
import sys
import getpass
import hashlib
import MySQLdb as mdb

from subprocess import call

# global db connection
CON = None

def login():
	print "Enter blank username to cancel"
	call(["clear"])
	good = False
	cur = CON.cursor()

	while not good:
		userName = raw_input("Username: ")

		# exit back to main menu if user enters no username
		if userName == "":
			break
		passwd = getpass.getpass()

		# get data from mysql
		cur.execute( "select * from dfusers where name='" + userName + "'")
		data = cur.fetchall()
		if data == ():
			print "incorrect login information provided"

		# hash the remote password
		remotePasswordHash = data[0][1]

		# hash the local password
		localPasswordHash = hashlib.md5()
		localPasswordHash.update( passwd )

		if localPasswordHash.digest() == remotePasswordHash:
			result = call(["sh", "/usr/share/df_linux/df_script_helper", userName])
			good = True
		else:
			print "incorrect login information provided"

def createAccount():
	call(["clear"])
	good = False
	cur = CON.cursor()
	passwd = None

	while not good:
		print "Enter a username with no special characters or spaces"
		uname = raw_input("> ")

		# get a list of usernames from the db
		cur.execute("select name from dfusers")
		data = cur.fetchall()
		users = [];

		for element in data:
			users.append(element[0])


		# check if username is not already in use
		if not uname in users:
			print "Enter a password"
			passwd1 = getpass.getpass()
			print "Enter the password again"
			passwd2 = getpass.getpass()
			# handle non-matching passwords
			if not passwd2 == passwd1:
				print "The passwords did not match, try again"
			else:
				good = True
				# hash the passwords
				passwd = hashlib.md5()
				passwd.update(passwd1)

		else:
			good = False;
			print "Username already exists"

	# if the data was good, add it to the db
	if( good ):
		cur.execute("insert into dfusers (name, password) values ('" + uname + "','" + passwd.digest() + "')")

def quit():
	call(["clear"])
	sys.exit(0)

def printOptions():
	# clear the screen
	call(["clear"])

	# print out our main stat
	print "Welcome to Dwarf Fortress!"
	print "Please select an option"
	print "---------------------------"
	print " (l)ogin and start"
	print " (c)reate account"
	print " (q)uit"

# the function dictionary
options = { 'l':login, 'c':createAccount, 'q':quit }
validInput = [ 'l', 'c', 'q' ]

def main():
	# connect to the db
	global CON
	CON = mdb.connect('localhost', 'script', 'dfdfdf', 'df' )

	user = None
	good = False
	run = True

	while run:
		while not good:
			printOptions()
			user = raw_input("Make a selection> ")

			# check to make sure the input is valid
			if user in validInput:
				good = True

		function = options[user]
		function()
		good = False

main()
