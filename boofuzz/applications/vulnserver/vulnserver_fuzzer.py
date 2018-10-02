#!/usr/bin/python

from boofuzz import *
import sys
import time

host = "192.168.1.9"
port = 9999

def banner(sock):
    sock.recv(1024)

def main():

    start_cmd = ['C:\\Users\\lol\\Desktop\\vulnserver\\vulnserver.exe']

    session = Session(
    	target = Target(
	    connection = SocketConnection(host, port, proto='tcp'),
            procmon = pedrpc.Client(host, 26002),
            procmon_options = {
                "proc_name" : "vulnserver.exe",
                "start_commands" : [start_cmd],
                 "stop_commands" : ['wmic process where (name="vulnserver.exe") delete'],
             #   "stop_commands" : ['taskkill /IM vulnserver.exe /F'],
            },
	),
        session_filename = "vulnserver.session",
    )

    """ Define data model. """
    s_initialize(name="VulnserverDATA")
    s_group("commands", values=['GMON', 'KSTET', 'GTER', 'HTER'])
    if s_block_start("CommandBlock", group="commands"):
        s_delim(' ')
        s_string('fuzz')
        s_static('\r\n')
    s_block_end("CommandBlock")
    
    """ Define state model. """
    session.connect(s_get("VulnserverDATA"))
    
    """ grab the banner from the server """
    session.pre_send = banner
    
    """ start fuzzing - define target and data """
    session.fuzz()

if __name__ == "__main__":
    main()

