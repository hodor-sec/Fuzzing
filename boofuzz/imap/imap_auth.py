#!/usr/bin/env python
from boofuzz import *

def main():
	session = Session(
		target=Target(
		    connection=SocketConnection("127.0.0.1", 143, proto='tcp')
		),
	)

        s_initialize(name="IMAP FUZZ - 1 param")
        with s_block("1_param"):
            s_static("A01 LOGIN yoyo@hodor.local yoyo\r\n")
            s_static("A02")
            s_delim(" ", name="space-1")
            s_group("commands-1-param", values=["CREATE"])
            s_delim(" ", name="space-2")
            s_string("AAAA", name="1param_1")
            s_static("\r\n")
        #s_block_end()

        s_initialize(name="IMAP FUZZ - 2 params")
        with s_block("2_params"):
            s_static("A01 LOGIN yoyo@hodor.local yoyo\r\n")
            s_static("A02")
            s_delim(" ", name="space-3")
            s_group("commands-2-params", values=["LIST","RENAME"])
            s_delim(" ", name="space-4")
            if s_block_start("command", group="commands-2-params"):
                s_string("1234", name="2param_1")
                s_delim(" ", name="space-5")
                s_string("5678", name="2param_2")
                s_static("\r\n")
            #s_block_end()
        #s_block_end()
	
        session.connect(s_get("IMAP FUZZ - 1 param"))
	session.fuzz()

if __name__ == "__main__":
    main()

