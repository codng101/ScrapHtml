# coding: utf-8


import io

from bs4 import BeautifulSoup
list_file =io.open("list.txt", mode="r", encoding="utf-8")
text_file = io.open("Output.txt", mode="w", encoding="utf-8-sig")
for l in list_file:
    stripped_line = l.rstrip()
    a_file = io.open(stripped_line, mode="r", encoding="utf-8-sig")

    html = a_file.read()
    soup = BeautifulSoup(html, features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    #chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    #text = '\n'.join(chunk for chunk in chunks if chunk)
    i=000
    prefix= stripped_line.upper()
    prefix=''.join(prefix.split('.')[:-1])
    for line in lines:
        if line:
            txt = ''.join(line )
            i+=1
            out=prefix
            out+=("_%s=" % i)
            out+=txt+"\n"
            print(out)
            text_file.write(out)
        txt=''
        out=''
    a_file.close()
text_file.close()


