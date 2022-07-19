""" This scrips monitors net conectivity. It does ping to a list of hosts
	It writes a log file called pingmonitor.log
	"""
__author__ = 'pablo33'


import subprocess, logging, time
from datetime import datetime, timedelta


###  Parameters  ###
logging_file = 'pingmonitor.log'								# Name the log file
hosts = ('8.8.8.8','192.168.1.1','www.google.es','10.218.1.1')  # list of hosts
timetosleep = 30												# time to sleep
timetoretry = 5													# time to retry if any host is down

logging.basicConfig(
    level=logging.CRITICAL,
    format='%(asctime)s : %(levelname)s : %(message)s',
    filename = logging_file,
    filemode = 'w',
)

###  Functions  ###

class crono ():
	"""A simple cronometer class"""
	def __init__(self, start=True):
		self.timerstart = None
		self.timerstop = None
		self.running = False
		if start:
			self.start()

	def start (self):
		self.timerstart = datetime.now()
		if self.running:
			self.timerstop = None
		self.running = True

	def stop (self):
		if self.running:
			self.timerstop = datetime.now()
			self.running = False
		else:
			self.reset()

	def reset(self):
		if self.running:
			self.__init__(start = True)
		else:
			self.__init__(start=False)

	@property
	def elapsed (self):
		if self.running:
			return datetime.now() - self.timerstart
		elif self.timerstart == None:
			return timedelta(0)
		else:
			return self.timerstop - self.timerstart

	def __str__(self):
		return self.elapsed


def ping(host):
	""" Checks if ping is possible and its response
	"""
	ret = subprocess.run(
		['ping', '-c 3', '-w 5', host ],
		capture_output=True,
		)
	return ret

###  Main  ###
if __name__ == '__main__':
	ok_count = 0
	# initializing cronos
	clist = list()
	for c in range(0,len(hosts)):
		clist.append(crono(start=False))
	
	while True:
		for h in range(0,len(hosts)):
			p = ping (hosts[h])
			if p.returncode == 0 :
				if ok_count < len (hosts):
					logging.info (f'{hosts[h]} is responding')
					ok_count += 1
					if clist[h].running:
						clist[h].stop()
						logging.critical (f"{hosts[h]} was not responding since {clist[h].timerstart} ({clist[h].elapsed})")
						clist[h].reset()
			else:
				logging.warning(f"{h} is not responding: return code {p.returncode}, {p.stderr.decode('utf-8')[:-1]}")
				ok_count = 0
				if not clist[h].running:
					clist[h].start()

		if ok_count >= len (hosts):
			logging.debug(f"# All hosts are responding, sleeping {timetosleep} seconds")
			time.sleep(timetosleep)	# All hosts are responding
		else:
			logging.debug(f"# At least one host is not responding, retrying in {timetoretry} seconds")
			time.sleep(timetoretry) # At least one host is not responding
