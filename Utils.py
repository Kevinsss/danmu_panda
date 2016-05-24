# coding:utf-8
__author__ = 'Sun'

class Utils(object):

	def __init__(self):
		"""Do nothing,by default!"""

	@staticmethod
	def toConsole(danmuDict):
		if danmuDict['type'] == "1": 
			# danmu text msg
			# output nickName and danmu content!
			print danmuDict['data']['from']['nickName'] + ": " + danmuDict['data']['content']

		# elif danmuDict['type'] == "207":
		# 	# Bamboo gift,ignore
		# 	print ''
		# elif danmuDict['type'] == "208":
		# 	# Audience, ignore
		# 	print ''
	@staticmethod
	def toFile(danmuDict,f):
		if danmuDict['type'] == "1":
			tmp = danmuDict['data']['from']['nickName'] + u': ' + danmuDict['data']['content']
			print tmp
			text = tmp + '\n'
			f.write(text.encode('utf-8'))
			f.flush()
