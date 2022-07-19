# pingmonitor
Get a conectivity log doing pings to a Hosts list

This scripts does pings to a defined list of hosts. It is intended to supervise Internet conectivity, but you can supervise other hosts on your lan.  

# Why I did this script?
My router started to restart once a day, so I decided to get a log and detect when Internet was unable.  

# How it works
The script takes a list of hosts, you can set it IPs or domain names. The script will ping this hosts every X seconds (configurable) to check its  response.  
A log file is generated: A new line is added every time a host is not responding. Just one line is added if the host is responding.  
So the script is intended to log when a host is not reachable.  

This is a python3 file, define your hosts and times by editting the code.  

Have fun!  
