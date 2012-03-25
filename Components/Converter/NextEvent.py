#
#  NextEvent - Converter
#
#  ver 0.1
#
#  Coded by bigroma  from Domica team
#
#  This plugin is licensed under the Creative Commons 
#  Attribution-NonCommercial-ShareAlike 3.0 Unported 
#  License. To view a copy of this license, visit
#  http://creativecommons.org/licenses/by-nc-sa/3.0/ or send a letter to Creative
#  Commons, 559 Nathan Abbott Way, Stanford, California 94305, USA.
#
#  Alternatively, this plugin may be distributed and executed on hardware which
#  is licensed by Dream Multimedia GmbH.

#  This plugin is NOT free software. It is open source, you are allowed to
#  modify it (if you keep the license), but it may not be commercially 
#  distributed other than under the conditions noted above.

from Components.Converter.Converter import Converter
from enigma import eEPGCache, eServiceReference
from Components.Element import cached
#from Poll import Poll

class NextEvent(Converter, object):
	EVENT = 0
	EXT_DESC = 1

	def __init__(self, type):
#		Poll.__init__(self)
		Converter.__init__(self, type)
		self.epgcache = eEPGCache.getInstance()
		if type == "Name":
			self.type = self.EVENT
		elif type == "ExtDescription":
			self.type = self.EXT_DESC
		else:
			self.type = self.EXT_DESC

	@cached
	def getText(self):
		if not self.suspended:
			ref = self.source.service
			info = ref and self.source.info
			if info:
				eventNext = self.epgcache.lookupEvent(['IBDCTSERNX', (ref.toString(), 1, -1)])
				if eventNext:
					if self.type == self.EVENT:
						if len(eventNext[0]) > 4 and eventNext[0][4]:
							return "%s" %  eventNext[0][4]
						else:
							return ""
					else:
						if len(eventNext[0]) > 6 and eventNext[0][6]:
							return "%s" %  eventNext[0][6]
						elif len(eventNext[0]) > 5 and eventNext[0][5]:
							return "%s" %  eventNext[0][5]
						else:
							return ""

		return ""

	text = property(getText)
