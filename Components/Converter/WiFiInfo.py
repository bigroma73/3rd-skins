# WifiInfo by 2boom 2012 v.0.4
#<widget source="session.CurrentService" render="Progress" pixmap="750HD/icons/linkq_ico.png" position="1103,35" zPosition="3" size="28,15" transparent="1" >
#    <convert type="WiFiInfo">linkqua</convert>
#  </widget>
#<widget source="session.CurrentService" render="Label" position="462,153" size="50,22" font="Regular; 17" zPosition="2" backgroundColor="background1" foregroundColor="white" transparent="1">
#    <convert type="WiFiInfo">link</convert>
#  </widget>
#<widget source="session.CurrentService" render="Label" position="462,153" size="50,22" font="Regular; 17" zPosition="2" backgroundColor="background1" foregroundColor="white" transparent="1">
#    <convert type="WiFiInfo">level</convert>
#  </widget>
#<widget source="session.CurrentService" render="Label" position="462,153" size="50,22" font="Regular; 17" zPosition="2" backgroundColor="background1" foregroundColor="white" transparent="1">
#    <convert type="WiFiInfo">noise</convert>
#  </widget>

from Poll import Poll
from Components.Converter.Converter import Converter
from Components.Element import cached
from pythonwifi.iwlibs import  Wireless

class WiFiInfo(Poll, Converter, object):
	link = 0
	level = 1
	noise = 2
	linkqua = 3
	
	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)
		if type == "link":
			self.type = self.link
		elif type == "level":
			self.type = self.level
		elif type == "noise":
			self.type = self.noise
		elif type == "linkqua":
			self.type = self.linkqua
		self.poll_interval = 3000
		self.poll_enabled = True
		
	def linkMax(self):
		ifobj = Wireless('wlan0')
		return int(ifobj.getQualityMax().quality)
		
	@cached
	def getText(self):
		wifi = " "
		for line in open("/proc/net/wireless"):
			if self.type == self.link and line.split()[0] == "wlan0:":
				try:
					linkq = int(int(line.split()[2][:-1]) * 100) / self.linkMax()
				except:
					linkq = 0
				wifi = "%s%%" % linkq
			elif self.type == self.level and line.split()[0] == "wlan0:":
				wifi = ("%s dBm" % line.split()[3])
			elif self.type == self.noise and line.split()[0] == "wlan0:":
				wifi = ("%s dBm" % line.split()[4])
		return wifi
	text = property(getText)
	
	@cached
	def getValue(self):
		linkq = 0
		for line in open("/proc/net/wireless"):
			if self.type == self.linkqua and line.split()[0] == "wlan0:":
				try:
					linkq = int(int(line.split()[2][:-1]) * 100) / self.linkMax()
				except:
					linkq = 0
		return linkq
	value = property(getValue)
	range = 100

	def changed(self, what):
		if what[0] == self.CHANGED_POLL:
			self.downstream_elements.changed(what)
