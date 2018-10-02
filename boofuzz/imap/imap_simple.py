#!/usr/bin/env python
from boofuzz import *

def main():
	session = Session(
		target=Target(
		    connection=SocketConnection("127.0.0.1", 143, proto='tcp')
		),
	)

	s_initialize(name='IMAP FUZZ')
        s_static("A01 ")
        s_group("commands", values=["LIST","AUTHENTICATE","LOGIN"])

        if s_block_start("command", group="commands"):
            s_string("1234", name="imap_command")
            s_static("\r\n")
        s_block_end()

	session.connect(s_get("IMAP FUZZ"))
	session.fuzz()

if __name__ == "__main__":
    main()

