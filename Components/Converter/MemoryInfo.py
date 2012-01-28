# MemoryInfo by 2boom 2012 v. 0.2
# <widget source="session.CurrentService" render="Label" position="189,397" zPosition="4" size="350,20" noWrap="1" valign="center" halign="center" font="Regular;14" foregroundColor="clText" transparent="1"  backgroundColor="#20002450">
#	<convert type="MemoryInfo">MemTotal</convert>
# </widget>			

from enigma import iServiceInformation
from Components.Converter.Converter import Converter
from Components.Element import cached
import os

class MemoryInfo(Converter, object):
	MemTotal = 0
	MemFree = 1
	SwapTotal = 2
	SwapFree = 3
	
	def __init__(self, type):
		Converter.__init__(self, type)
		self.type = {
				"MemTotal": (self.MemTotal),
				"MemFree": (self.MemFree),
				"SwapTotal": (self.SwapTotal),
				"SwapFree": (self.SwapFree),
			}[type]
			
	@cached
	def getText(self):
		service = self.source.service
		info = service and service.info()
		try:
			meminfo = os.popen("cat /proc/meminfo")
		except:
			return None

		if meminfo is not None:
			for line in meminfo:
				if self.type == self.MemTotal and line.find("MemTotal") > -1:
					try:
						info = "%s Kb" % line.split()[1]
					except:
						return None
				elif self.type == self.MemFree and line.find("MemFree") > -1:
					try:
						info = "%s Kb" % line.split()[1]
					except:
						return None
				elif self.type == self.SwapTotal and line.find("SwapTotal") > -1:
					try:
						info = "%s Kb" % line.split()[1]
					except:
						return None
				elif self.type == self.SwapFree and line.find("SwapFree") > -1:
					try:
						info = "%s Kb" % line.split()[1]
					except:
						return None
			meminfo.close()
			return info
		else:
			meminfo.close()
			return ""

	text = property(getText)

	def changed(self, what):
		Converter.changed(self, what)
