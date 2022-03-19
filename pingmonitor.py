""" This scrips monitors net conectivity. It does ping to a list of hosts
	It writes a log file called pingmonitor.log
	"""
__author__ = 'pablo33'


import subprocess, time, logging

###  Parameters  ###
logging_file = 'pingmonitor.log'	# Name 
hosts = ('8.8.8.8','192.168.1.1','www.google.es','10.218.1.1')
timetosleep = 30
timetoretry = 5

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s : %(levelname)s : %(message)s',
    filename = logging_file,
    filemode = 'w',
)

###  Functions  ###

def ping(host):
	""" Checks if ping is possible and its response
	"""
	ret = subprocess.run(
		['ping', '-c 3', '-w 5', host ],
		capture_output=True,
		)
	return ret

###  Main  ###
ok_count = 0
while True:
	for h in hosts:
		p = ping (h)
		if p.returncode == 0 :
			if ok_count < len (hosts):
				logging.info (f'{h} is responding')
				ok_count += 1
		else:
			logging.warning(f"{h} is not responding: return code {p.returncode}, {p.stderr.decode('utf-8')[:-1]}")
			ok_count = 0

	if ok_count >= len (hosts):
		time.sleep(timetosleep)	# All hosts are responding
	else:
		time.sleep(timetoretry) # At least one host is not responding
