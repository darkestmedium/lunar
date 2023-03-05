import sys
import telnetlib

port = 20230

if len(sys.argv) > 1:
	port = sys.argv[1]

try:
	tn = telnetlib.Telnet("localhost", port)
	tn.write('catchQuiet(`loadPlugin "mlunar"`)'.encode())
	tn.close()
except:
	pass