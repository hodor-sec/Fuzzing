#!/usr/bin/env python
from boofuzz import *

def main():
	session = Session(
		target=Target(
		    connection=SocketConnection("127.0.0.1", 25, proto='tcp')
		),
	)

	s_initialize(name='SMTP FUZZ')
	with s_block("SMTP FUZZY"):

		#Authentication 
		########################################################
		s_string("HELO localhost\r\n", name='helo_host_auth')
		s_string("AUTH", name='auth1')
		s_delim(" ")
		s_string("LOGIN", name='login1')
		s_static("\r\n")
		s_string("AUTH", name='auth2')
		s_delim(" ")
		s_string("YOYO", name='user')
		s_static("\r\n")
		s_string("AUTH", name='auth3')
		s_delim(" ")
		s_string("YAYA", name='pass')
		s_static("\r\n")
		s_static("QUIT\r\n\r\n\r\n")

		#########################################################
		# RCTP TO:
		s_static("HELO");
		s_delim(" ")
		s_string("localhost", name='host')
		s_static("\r\n")
		s_static("MAIL FROM")
		s_delim(":")
		s_delim("<")
		s_static("bob", name='frommailprefix1')
		s_delim("@")
		s_static("bob", name='frommailsuffix1')
		s_delim(".")
		s_static("com", name='frommailtld1')
		s_delim(">")
		s_static("\r\n")
		s_static("RCPT TO:")
		s_delim(" ")
		s_string("postmaster", name='tomailprefix')
		s_delim("@")
		s_string("company", name='tomailsuffix')
		s_delim(".")
		s_string("mail", name='tomailtld')
		s_static("\r\n")
		s_static("DATA")
		s_static("\r\n")
		s_string("Message-ID", name='messageidrcpt')
		s_delim(":")
		s_string("123", name='midrcpt')
		s_static("\r\n")
		s_string("AAAA", name='messagercpt')
		s_static("\r\n")
		s_static(".\r\n")
		s_static("QUIT\r\n")

		##########################################################3
		# MAIL FROM:
		s_static("HELO");
		s_delim(" ")
		s_string("localhost", name='fromhost')
		s_static("\r\n")
		s_string("MAIL FROM", name='mailfrom')
		s_delim(":")
		s_delim("<")
		s_string("bob", name='frommailprefix2')
		s_delim("@")
		s_string("bob", name='frommailsuffix2')
		s_delim(".")
		s_string("com", name='frommailtld2')
		s_delim(">")
		s_static("\r\n")
		s_static("RCPT TO:")
		s_delim(" ")
		s_static("postmaster")
		s_delim("@")
		s_static("company")
		s_delim(".")
		s_static("mail")
		s_static("\r\n")
		s_static("DATA")
		s_static("\r\n")
		s_static("Message-ID")
		s_delim(":")
		s_string("123", name='messageidfrom')
		s_static("\r\n")
		s_string("AAAA", name='messagefrom')
		s_static("\r\n")
		s_static(".\r\n")
		s_static("QUIT\r\n")
	
	session.connect(s_get("SMTP FUZZ"))
	session.fuzz()

if __name__ == "__main__":
    main()
