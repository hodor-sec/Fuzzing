#!/usr/bin/env python
# Designed for use with boofuzz v0.0.9
from boofuzz import *

def main():
    session = Session(
        target=Target(
            connection=SocketConnection("192.168.1.9", 7510, proto='tcp')
        ),
    )

    s_initialize(name="Request")
    with s_block("Request-Line"):
        s_string("GET");
        s_delim(" ", name='space-1');
        s_string("/topology/home", name='Request-URI');
        s_delim(" ", name='space-2');
        s_string("HTTP/1.1", name='HTTP-Version');
        s_string("\r\n", name="Request-Line-CRLF 1");

        s_string("Host: ", name='Host');
        s_string("192.168.1.9", name='IP');
        s_delim(":", name='colon-1');
        s_string("7510", name='port');
        s_string("\r\n", name="Request-Line-CRLF 2");
        
        s_string("User-Agent", name='User Agent');
        s_delim(": ", name='colon-2');
        s_string("Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.1.14)", name='UA');
        s_string("\r\n", name="Request-Line-CRLF 3");
        
    s_static("\r\n", "Request-CRLF")

    session.connect(s_get("Request"))

    session.fuzz()


if __name__ == "__main__":
    main()

