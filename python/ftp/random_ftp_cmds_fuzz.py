# Author: hodorsec
# Description: uses randomly chosen ASCII friendly characters as string to fuzz several FTP commands as written by RFC's
# Modify username/password for own convenience

#!/usr/bin/env python
import sys, socket, struct, random, string, time
 
if len(sys.argv) <= 2:
    print "Usage: python " + sys.argv[0] + " [host] [port]"
    exit()

def random_string(str_size, allowed_chars):
    return ''.join(random.choice(allowed_chars) for x in range(str_size))

host = sys.argv[1]    
port = int(sys.argv[2])

username = "hodor"
password = "hodorhodor"

maxlength = 20000
mess_size = 0
increment = 1000

chars = string.ascii_letters + string.punctuation

commands = (['ABORT','ACCT','CCC','CDUP','CWD','DELE','FEAT','HELP','LIST','MDTM','MKD','MODE','NOOP','OPTS','PASS','PASV','PORT','PROT','PWD','QUIT','REST','RETR','RMD','RNFR','SIZE','STOR','STRU','TYPE','USER','UTF8','XCRC'])

print "[+] Connecting to " + host + "\n"

for command in commands:
    mess_size = 0
    while (mess_size < maxlength):
        try:
		payload = random_string(mess_size,chars)
		
		print "\n[+] Fuzzing string: "
		for char in payload:
		    sys.stdout.write("\\x%x" % ord(char))
		print '\n'
		print "[+] Fuzzing " + command + " with " + str(mess_size) + " length message..."
		
		req = (
                        command + " " + payload
		)
	    
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.settimeout(2)
		s.connect((host, port))
		s.recv(1024)
		s.send("USER " + username + "\r\n")
		s.recv(1024)
		s.send("PASS " + password + "\r\n")
		s.recv(1024)
		s.send(req)
		s.recv(1024)
		s.close()

		mess_size += increment
        except Exception,e:
            print "[!] Error occured: " + str(e)
            print "[*] Crashed occured at buffer length: " + str(len(payload))
            sys.exit()

