#!/usr/bin/env python
from boofuzz import *

def main():
	session = Session(
		target=Target(
		    connection=SocketConnection("127.0.0.1", 110, proto='tcp')
		),
	)

        s_initialize(name="POP3 FUZZ")

	s_static("USER")
	s_delim(" ")
	s_static("yoyo")
	s_static("\r\n")
	s_string("PASS")
	s_delim(" ")
	s_string("yoyo")
	s_static("\r\n")

	s_string("STAT")
	s_static("\r\n")

	s_string("LIST")
	s_delim(" ")
	s_string("A")
	s_static("\r\n")

	s_string("RETR")
	s_delim(" ")
	s_string("A")
	s_static("\r\n")

	s_string("DELE")
	s_delim(" ")
	s_string("A")
	s_static("\r\n")

	s_string("NOOP")
	s_delim(" ")
	s_string("A")
	s_static("\r\n")

	s_string("RSET")
	s_delim(" ")
	s_string("A")
	s_static("\r\n")
	s_static("QUIT")

	session.connect(s_get("POP3 FUZZ"))
	session.fuzz()

if __name__ == "__main__":
    main()

