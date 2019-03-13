#!/usr/bin/env python
# Designed for use with boofuzz v0.0.8
from boofuzz import *
import sys,time

host = '192.168.252.10'
port = 21
program = 'csrv.exe'

def banner(sock):
    sock.recv(1024)

def main():
    start_cmd = ['C:\\Program Files (x86)\\CoreFTPServer\\' + program]
    session = Session(
    	target = Target(
	    connection = SocketConnection(host, port, proto='tcp'),
            procmon = pedrpc.Client(host, 26002),
            procmon_options = {
                "proc_name" : program,
                "stop_commands" : ['net stop "Core FTP Server"'],
                "start_commands" : [start_cmd],
            },
	),
        session_filename = "coresvr.session",
        check_data_received_each_request = True,
        receive_data_after_fuzz = True,
        receive_data_after_each_request = True,
    )

    """ Define data model. """
    # User
    s_initialize("user")
    s_static("USER hodor\r\n")

    # Pass
    s_initialize("pass")
    s_static("PASS hodorhodor\r\n")
    
    # PASV mode
    s_initialize('pasv')
    s_static('PASV\r\n')

    # FTP CMD's
    s_initialize("FTP_CMD")
    # s_group("commands", values=['CWD','MDTM','MKD','PORT','RETR','RMD','RNFR','RNTO','SIZE','CDUP'])
    # s_group("commands", values=['PBSZ','PORT','PROT','PWD','QUIT','REST','RETR','RMD','RNFR','SIZE','STOR','STRU','TYPE','USER','UTF8','XCRC'])
    s_group("commands", values=['ABORT','ACCT','CCC','CDUP','CWD','DELE','FEAT','HELP','LIST','MDTM','MKD','MODE','NOOP','OPTS','PASS','PASV','PBSZ','PORT','PROT','PWD','QUIT','REST','RETR','RMD','RNFR','SIZE','STOR','STRU','TYPE','USER','UTF8','XCRC'])
    s_block_start("CommandBlock", group="commands")
    s_static(' ')
    s_string('fuzz')
    s_static('\r\n')
    s_block_end()

    # Define order to send data
    session.connect(s_get("user"))
    session.connect(s_get("user"), s_get("pass"))
    session.connect(s_get("pass"), s_get("FTP_CMD"))

    """ grab the banner from the server """
    session.pre_send = banner
    
    """ start fuzzing - define target and data """
    session.fuzz()

if __name__ == "__main__":
    main()

