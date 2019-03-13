from boofuzz import *

def main():
	session = Session(
		target=Target(
		    connection=SocketConnection("127.0.0.1", 80, proto='tcp')
		),
	)

	s_initialize(name='HTTP POST SEARCH')
	with s_block("HTTP POST SEARCH-Line"):
		s_static("POST /search.ghp?forumid=")
		s_string("1", name='forumid')
		s_static(" HTTP/1.1\r\n")
		s_static("Content-Type: application/x-www-form-urlencoded\r\n")
		s_static("User-Agent: Mozilla/5.0\r\n")
		s_static("Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8\r\n")
		s_static("Referer: http://192.168.1.9/\r\n")
		s_static("Accept-Encoding: gzip, deflate\r\n")
		s_static("Accept-Language: en-US\r\n")
		s_static("Cookie: UserID=")
		s_string("1234", name='userid')
		s_delim("; PassWD=")
		s_string("1234", name='passwd')
		s_delim("; SESSIONID=")
		s_string("1234", name='sessionid')
		s_static("\r\n")
		s_static("Connection: close\r\n")
		s_static("\r\n\r\n")
		s_static("searchitem=")
		s_string("1234", name='searchitem')
		s_delim("&gosearch.x=", name='gosearch.x')
		s_string("15")
		s_delim("&gosearch.y=", name='gosearch.y')
		s_string("14")
		s_static("\r\n\r\n")
	
	session.connect(s_get("HTTP POST SEARCH"))
	session.fuzz()

if __name__ == "__main__":
    main()
