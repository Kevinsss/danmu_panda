# Crawl Bullet screen of PandaTV

## Decription
	Crawl bullet scree(or "dan mu" in Chinese) of PandaTV's Liveroom.
	main.py: start point.
	Utils.py: tools class.
	PandaTv.py: connect TCP server(ip:port) to crawl bullet scree data.
	PandaMsg.py: type of PandaTV message.

## Environment
	Python: 2.7.*
	System: Windows/Linux/Mac

## Usage
	To run main.py normaly,you need these parameter:
		-rid roomid : 	PandaTV room id
		-f(Optional): 	whether out to file
	Example:
		python main.py -rid 123456 -f (crawl roomid:123456 and output result to file) 
		python main.py -rid 123456	(crawl roomid:123456 and output result to console)




