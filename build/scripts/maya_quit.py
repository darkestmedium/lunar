import sys
import telnetlib


def quitMayaRemotley():
	port = 20230

	if len(sys.argv) > 1:
		port = sys.argv[1]

	try:
		tn = telnetlib.Telnet("localhost", port)
		tn.write('catchQuiet(`quit -force`)'.encode())
		tn.close()
	except:
		pass