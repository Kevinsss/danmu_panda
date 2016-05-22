# coding:utf-8
__author__ = 'Sun'

import time
import threading
import json
import urllib2
import urllib
import socket
import struct
import sys
import math
import threading
from PandaMsg import PandaMsg
from Utils import Utils
from bs4 import BeautifulSoup


class PandaTV(object):

	def __init__(self,roomid):
		self.roomid = roomid
		currTime = int(time.time())
		# set roomid and unixtimestamp to get rid,roomid,sign...
		url1 = "http://www.panda.tv/ajax_chatroom?roomid=" + roomid + "&_=" + str(currTime)
		# set User-agent to FireFox,to avoid being refused
		headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0'}
		request = urllib2.Request(url1, headers = headers)
		data1 = json.loads(urllib2.urlopen(request).read())
		errno = data1['errno']
		if not 0 == errno:
			print u'ERROR: Could not get sign code!';
			sys.exit()

		# set rid,roomid,sign... to get chat_addr_list,appid...
		currTime = int(time.time())
		url2 = "http://api.homer.panda.tv/chatroom/getinfo?rid=" + str(data1['data']['rid']) + "&roomid=" + roomid +"&retry=0&sign=" + data1['data']['sign'] + "&ts=" + str(data1['data']['ts']) + "&_=" + str(currTime)
		request = urllib2.Request(url2,headers = headers)
		data2 = json.loads(urllib2.urlopen(request).read())
		errno = data2['errno']
		if not 0 == errno:
			print u'ERROR: Could not get server address!'
			sys.exit()
		temp = tuple(data2['data']['chat_addr_list'][1].split(':'))
		self.server_addr = (temp[0],int(temp[1]))
		self.authType = str(data2['data']['authType'])
		self.ts = str(data2['data']['ts'])
		self.sign = str(data2['data']['sign'])
		self.appid = str(data2['data']['appid'])
		self.rid = str(data2['data']['rid'])
		self.k = "1" 
		self.t = "300"
		print u'Successful initialization!'


	def connectServer(self,outfile):
		data = "u:" + self.rid + "@" + self.appid + "\n" + "k:" + self.k + "\n" +"t:" + self.t + "\n" +"ts:" + self.ts + "\n" +"sign:" + self.sign + "\n" +"authtype:" + self.authType
		try:
			self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error, msg:
			print "Creating Socket Failure. Error Code : " + str(msg[0]) + " Message : " + msg[1]
			sys.exit()
		print self.server_addr
		self.client.connect(self.server_addr)
		self.client.sendall(self.message(data))
		th = threading.Thread(target=PandaTV.heart,args=(self,))
		th.setDaemon(True)
		th.start()
		# reading
		print 'reading data...'
		if outfile:
			try:
				self.f = open(self.roomid + '.txt' ,'a')
			except IOError:
				print 'can not open file!'

		while True:
			danmuJsonList = self.read()
			for danmuJson in danmuJsonList:
				danmuDict = json.loads(danmuJson)
				self.analyzeData(danmuDict,outfile)
		self.client.close()
		self.f.close()

	def read(self):
		result = []
		tmp = self.client.recv(4)
		# each data start with [0x00,0x06,0x00,0x03]
		if tmp == b'\x00\x06\x00\x03':
			# ack info packets
			ackLen = self.client.recv(2)
			ackLen = int(ord(ackLen[0]) * math.pow(16,2) + ord(ackLen[1]))

			self.client.recv(ackLen)
			tmp = bytes(self.client.recv(4))
			# compute length of data   
			dataLen = int(ord(tmp[0]) * math.pow(16,6) + ord(tmp[1]) * math.pow(16,4) + ord(tmp[2]) * math.pow(16,2) + ord(tmp[3]))
			data = self.client.recv(dataLen)

			danmu_flag = data[0:4] #danmu message flag
			i = 0
			while i < len(data):
				if data[i] == danmu_flag[0] and data[i+1] == danmu_flag[1] and data[i+2] == danmu_flag[2] and data[i+3] == danmu_flag[3] :
					i = i + 4
					i = i + 8 # skip useless bytes
					j = 0
					length = 0
					while j < 4:
						n = ord(data[i+j])
						if n < 0:
							n = 256 + n
						length += n * math.pow(16,2*(3-j))
						j += 1

					i += 4
					length = int(length)
					result.append(data[i:i+length])
				else:
					i += 1
		else:
			tmp = self.client.recv(2)
			dataLen = int(ord(tmp[0]) * math.pow(16,2) + ord(tmp[1]))
			data = self.client.recv(dataLen)
			# print data

		return result

	def message(self, content):
		return PandaMsg(content).getBytes()

	def heart(self):
		HEART_TIME = 60 # Heartbeat packet 120 seconds
		while True:
			print ">>>>>>>>>>>>>>>>>>Heartbeat>>>>>>>>>>>>>>>>"
			# heartbeat packets is [0x00,0x06,0x00,0x00]
			self.client.sendall(b'\x00\x06\x00\x00')
			time.sleep(HEART_TIME)

	def analyzeData(self,danmuDict,outfile):
		if not outfile:
			Utils.toConsole(danmuDict)
		else:
			print ">>>>>saveToFile>>>>"
			Utils.toFile(danmuDict,self.f)

		
if __name__ == '__main__':
	crawl = PandaTV(roomid)
	crawl.connectServer()
