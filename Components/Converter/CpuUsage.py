#
# CpuUsage Converter for Enigma2 (CpuUsage.py)
# Coded by vlamo (c) 2012
#
# Version: 0.1 (10.01.2012 00:20)
# Support: http://dream.altmaster.net/
# mod by 2boom nontype output

from Converter import Converter
from Poll import Poll
from Components.Element import cached

class CpuUsage(Converter, Poll, object):
	CPU_CALC  = -3
	CPU_ALL   = -2
	CPU_TOTAL = -1

	def __init__(self, type):
		Converter.__init__(self, type)
		
		self.short_list = True
		self.cpu_count = 0
		self.prev_info = self.getCpuInfo(self.CPU_CALC)
		
		if type == "Total":
			self.type = self.CPU_TOTAL
			self.sfmt = "CPU: $0"
		elif not type:
			self.type = self.CPU_TOTAL
			self.sfmt = "$0"
		else:
			self.type = self.CPU_ALL
			self.sfmt = txt = str(type)
			pos = 0
			while True:
				pos = self.sfmt.find("$", pos)
				if pos == -1: break
				if pos < len(self.sfmt)-1 and self.sfmt[pos+1].isdigit():
					x = int(self.sfmt[pos+1])
					if x > self.cpu_count:
						self.sfmt = self.sfmt.replace("$" + self.sfmt[pos+1], "n/a")
				pos += 1
		
		self.curr_info = self.getCpuInfo(self.type)
		
		Poll.__init__(self)
		self.poll_interval = 500
		self.poll_enabled = True

	def getCpuInfo(self, cpu=-1):
		def validCpu(c):
			if cpu == self.CPU_CALC and c.isdigit():
				return True
			elif cpu == self.CPU_ALL:
				return True
			elif c == " " and cpu == self.CPU_TOTAL:
				return True
			elif c == str(cpu):
				return True
			return False
		
		res = []
		calc_cpus = cpu == self.CPU_CALC and self.cpu_count == 0
		try:
			fd = open("/proc/stat", "r")
			for l in fd:
				if l[0] != "c": continue
				if l.find("cpu") == 0 and validCpu(l[3]):
					if calc_cpus:
						self.cpu_count += 1
						continue
					total = busy = 0
					# tmp = [cpu, usr, nic, sys, idle, iowait, irq, softirq, steal]
					tmp = l.split()
					for i in range(1, len(tmp)):
						tmp[i] = int(tmp[i])
						total += tmp[i]
					# busy = total - idle - iowait
					busy = total - tmp[4] - tmp[5]
					if self.short_list:
						# append [cpu, total, busy]
						res.append([tmp[0], total, busy])
					else:
						tmp.insert(1, total)
						tmp.insert(2, busy)
						# append [cpu, total, busy, usr, nic, sys, idle, iowait, irq, softirq, steal]
						res.append(tmp)
			fd.close()
		except:
			pass
		return res

	@cached
	def getText(self):
		res = self.sfmt
		self.prev_info, self.curr_info = self.curr_info, self.getCpuInfo(self.type)
		for i in range(len(self.curr_info)):
			# xxx% = (cur_xxx - prev_xxx) / (cur_total - prev_total) * 100
			try:
				p = 100 * ( self.curr_info[i][2] - self.prev_info[i][2] ) / ( self.curr_info[i][1] - self.prev_info[i][1] )
			except ZeroDivisionError:
				p = 0
			res = res.replace("$" + str(i), "% 3d%%" % (p))
		return res.replace("$?", "%d" % (self.cpu_count))
	
	text = property(getText)

	def changed(self, what):
		if what[0] == self.CHANGED_POLL:
			self.downstream_elements.changed(what)
