# coding:utf-8
__author__ = 'Sun'
import sys
from PandaTV import PandaTV

if __name__ == '__main__':
	#get args from cmd line
	roomid = ''
	outfile = False
	argflag = True
	if roomid.strip() == '':
		roomid = '2009';
	
	for i in range(len(sys.argv)):
		if sys.argv[i] == '-rid':
			roomid = sys.argv[i+1]
			argflag = False
		if sys.argv[i] == '-f':
			outfile = True
			argflag = False
		if sys.argv[i] != 'main.py':
			argflag = True
			argflag = False

	if argflag:
		print 'Argrument Error:'
		print '***************************************************'
		print '-u roomid		: PandaTV room id'
		print '-f 	(Optional)	: whether out to file'
		print 'Example: python main.py -u 202512 -f'
		print '***************************************************'
		sys.exit()

	# start
	panda = PandaTV(roomid)
	panda.connectServer(outfile)