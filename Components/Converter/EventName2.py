from Components.Converter.Converter import Converter
from Components.Element import cached
from enigma import eEPGCache, eServiceReference

class EventName2(Converter, object):
	NAME = 0
	SHORT_DESCRIPTION = 1
	EXTENDED_DESCRIPTION = 2
	FULL_DESCRIPTION = 3
	NEXTEVENT = 4
	ID = 5

	def __init__(self, type):
		Converter.__init__(self, type)
		self.epgcache = eEPGCache.getInstance()
		if type == "FullDescription":
			self.type = self.SHORT_DESCRIPTION
		elif type == "ExtendedDescription":
			self.type = self.EXTENDED_DESCRIPTION
		elif type == "Description":
			self.type = self.FULL_DESCRIPTION
		elif type == "NextEvent":
			self.type = self.NEXTEVENT			
		elif type == "ID":
			self.type = self.ID
		else:
			self.type = self.NAME

	@cached
	def getText(self):
		event = self.source.event
		if event is None:
			return " "
			
		if self.type == self.NAME:
			return event.getEventName()
		elif self.type == self.SHORT_DESCRIPTION:
			return event.getShortDescription()
		elif self.type == self.EXTENDED_DESCRIPTION:
			return event.getExtendedDescription()
		elif self.type == self.NEXTEVENT:
		       
			ref = self.source.service
			info = ref and self.source.info
			eventNext = self.epgcache.lookupEvent(['IBDCTSERNX', (ref.toString(), 1, -1)])
			if eventNext:
                                desc = "%s %s" % ( len(eventNext[0]) > 5 and eventNext[0][5] or "", len(eventNext[0]) > 6 and eventNext[0][6] or "" )
                                return desc

					
		elif self.type == self.FULL_DESCRIPTION:
			desc = event.getShortDescription() or ""
			if desc != "":
				desc = desc + ''
			desc = desc + event.getExtendedDescription() or ""
			return desc
		elif self.type == self.ID:
			return str(event.getEventId())

		
					
	text = property(getText)
