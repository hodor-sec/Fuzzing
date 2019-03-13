#!/bin/sh

if [ $# -eq 1 ]; then
	sqlite3 ./$1  "SELECT test_case_index, type, data FROM steps WHERE test_case_index IN (SELECT test_case_index FROM steps where type == 'fail') and type == 'send' ORDER BY test_case_index ASC LIMIT 0, 50000;"
	else echo "Give a Sqlite3 DB from Boofuzz as an argument."
fi

