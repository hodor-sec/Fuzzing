#!/usr/bin/env python
import sys, socket, struct, time

if len(sys.argv) <= 2:
    print("Usage: python " + sys.argv[0] + " [host] [port]")
    exit()

host = sys.argv[1]
port = int(sys.argv[2])

maxlength = 5000
mess_size = 50
increment = 50

print("[+] Connecting to " + host + "\n")

while True and (mess_size < maxlength):
    try:
        print("[+] Fuzzing with " + str(mess_size) + " length message...")

        craftedreq =  "A" * mess_size

        req = (
                craftedreq
        )

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((host, port))
        s.send(req)
        s.recv()
        s.close()

        time.sleep(0.5)

        mess_size += increment
    except Exception as e:
        print("[!] Error occured: " + str(e))
        # print "[*] Crashed occured at buffer length: " + str(len(craftedreq))
        sys.exit()


