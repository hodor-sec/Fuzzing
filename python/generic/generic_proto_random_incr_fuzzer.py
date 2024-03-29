#!/usr/bin/env python
import sys, socket, struct, random, string, time
 
if len(sys.argv) <= 2:
    print("Usage: python " + sys.argv[0] + " [host] [port]")
    exit()

def random_string(str_size, allowed_chars):
    return ''.join(random.choice(allowed_chars) for x in range(str_size))

host = sys.argv[1]    
port = int(sys.argv[2])

maxlength = 5000
mess_size = 50
increment = 100

chars = string.ascii_letters + string.punctuation

print("[+] Connecting to " + host + "\n")

while True and (mess_size < maxlength):
    try:
        payload = random_string(mess_size,chars)
        
        print("\n[+] Fuzzing string: ")
        for char in payload:
            sys.stdout.write("\\x%x" % ord(char))
        print('\n')
        print("[+] Fuzzing with " + str(mess_size) + " length message...")
        
        req = (
                payload
        )
    
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((host, port))
        s.send(req)
        s.recv(1024)
        s.close()

        time.sleep(0.5)
    
        mess_size += increment
    except Exception as e:
        print("[!] Error occured: " + str(e))
        print("[*] Crashed occured at buffer length: " + str(len(payload)))
        sys.exit()

