#!/usr/bin/env python
#coding:utf-8
import sys
import os
import telnetlib
import time
import threading
import datetime
now = datetime.datetime.now()

#Use for loop to telnet into each routers and execute commands
class Bakconf(threading.Thread):
    def __init__(self,host,USERNAME,PASSWORD):
        threading.Thread.__init__(self)
        self.host=host
        self.USERNAME=USERNAME
        self.PASSWORD=PASSWORD
    def run(self):
        try:
            tn = telnetlib.Telnet(self.host,port=22,timeout=5)
            tn.set_debuglevel(5)
            tn.read_until(b"Username:", timeout=2)
            tn.write(self.USERNAME +b"\n")
            tn.read_until(b"Password:", timeout=2)
            tn.write(self.PASSWORD +b"\n")
            tn.write(b"\n")
            time.sleep(1)
            tn.write("system-view"+"\n")
            #######executive command in the txt file########
            for COMMANDS in open(r'/home/tonyfu/netmiko-develop/examples/show_command/1-cmdlist.txt').readlines():
                COMMAND = COMMANDS.strip('\n')
                tn.write("%s\n" %COMMAND)
            #######executive command in the txt file########
            time.sleep(60)   #Delay setting to made the command below have enough time to get response
            output = tn.read_very_eager()      #get return
            tn.write("quit"+"\n")
            filename = "/home/tonyfu/netmiko-develop/examples/show_command/%s_%i-%.2i-%.2i_%.2i:%.2i:%.2i.log" % (self.host,now.year,now.month,now.day,now.hour,now.minute,now.second)    #format the file name
            time.sleep(.1)
            fp = open(filename,"w")
            fp.write(output)
            fp.close()
        except:
            print "Can't connection %s"%self.host
            return

def main():
    USERNAME = "tonyfu"    #login name
    PASSWORD = "P@ssw0rd"    #login password
    for host in open(r'//home/tonyfu/netmiko-develop/examples/show_command/1-iplist.txt').readlines():
        dsthost = host.strip('\n')
        bakconf=Bakconf(dsthost, USERNAME, PASSWORD)
        bakconf.start()
if __name__=="__main__":
    main()