#!/bin/python3

import sqlite3
import sys
import MySQLdb as mdb

from subprocess import call

# global db connection
CON = None

def login():
	call(["clear"])
	good = False
	cur = CON.cursor()

	while not good:
		userName = raw_input("Username> ")

		call(["clear"])

		passwd = raw_input("Password> ")

		cur.execute( "select * from dfusers where name='" + userName + "'")

		data = cur.fetchall()
		if data == ():
			print "incorrect login information provided"
		elif passwd == data[0][1]:
			result = call(["sh", "/usr/share/df_linux/df_script_helper", userName])
			good = True
		else:
			print "incorrect login information provided"

def createAccount():
	call(["clear"])
	good = False
	cur = CON.cursor()

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
			print "Enter a password, this will be stored with no encryption"
			passwd = raw_input("> ")
			print "Enter the password again"
			passwd2 = raw_input("> ")
			# handle non-matching passwords
			if not passwd2 == passwd:
				print "The password did not match, try again"
			else:
				good = True
		else:
			good = False;
			print "Username already exists"

	# if the data was good, add it to the db
	if( good ):
		cur.execute("insert into dfusers (name, password) values ('" + uname + "','" + passwd + "')")

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
