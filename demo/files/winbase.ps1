get-date | out-file -filepath 'c:\salt\var\pstest.txt'

add-content 'c:\salt\var\pstest.txt' {{ MID }}