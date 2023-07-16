#!/usr/bin/env python
from boofuzz import *
import sys, time

host = '192.168.252.10'
port = 80
program = 'hfs_23m.exe'

def banner(sock):
    sock.recv(1024)

def main():
    s_initialize(name="Request")
    s_group("Method", ['GET'])#, 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE'])
    s_delim(" ",fuzzable=False)
    # s_static("/")
    s_static("/?search=")
    s_string("12345", name="search")
    s_static("&tpl=")
    s_string("list", name="tpl")
    s_delim(" ",fuzzable=False)
    s_static('HTTP/1.1')   
    s_static("\r\n")
    
    s_static("Host:")
    s_delim(" ",fuzzable=False)
    s_string(host, name='host')
    s_static("\r\n")
    
    s_static("User-Agent:")
    s_delim(" ",fuzzable=False)
    s_string("Firefox/60.0", name='UA')
    s_static("\r\n")
    s_static("Accept:")
    s_delim(" ",fuzzable=False)
    s_string("text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", name='Accept')
    s_static("\r\n")
    s_static("\r\n")    

    start_cmd = ['C:\\users\\vbox\\desktop\\vuln_progs\\hfs\\' + program]
    session = Session(
        target = Target(
        connection = SocketConnection(host, port, proto='tcp'),
            procmon = pedrpc.Client(host, 26002),
            procmon_options = {
                "proc_name" : program,
                "stop_commands" : ['wmic process where (name="' + program + '") delete'],
                "start_commands" : [start_cmd],
            },
    ),
        session_filename = "hfs.session",
    )

    session.connect(s_get("Request"))    
    session.fuzz()

if __name__ == "__main__":
    main()
