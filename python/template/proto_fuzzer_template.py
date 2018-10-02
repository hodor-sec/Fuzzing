#!/usr/bin/env python
import sys, socket, struct, requests, time
 
if len(sys.argv) <= 1:
    print "Usage: python " + sys.argv[0] + " [host] [port]"
    exit()
 
host = sys.argv[1]    
port = int(sys.argv[2])

maxlength = 100
mess_size = 50
increment = 1

print "[+]Connecting to " + host

while True:
    try:
        print "[+] Fuzzing with " + str(mess_size) + " length message..."

        craftedreq =  "A" * mess_size
    
        httpreq = (
        "PARAM" + craftedreq + "\r\n"
        )
    
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((host, port))
        s.send(httpreq)
        s.close()

        time.sleep(0.5)
    
        mess_size += increment
    except:
        print "[*] Crashed occured at buffer length: " + len(craftedreq)
        sys.exit()
