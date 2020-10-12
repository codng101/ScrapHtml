import io
import os
from bs4 import BeautifulSoup
import sys
from datetime import datetime


### Functions ###


def replaceText(listFile, output):
    list_file = io.open(listFile, mode="r", encoding="utf-8")

    for l in list_file:

        stripped_line = l.rstrip()
        prefix = stripped_line.upper()
        prefix = ''.join(prefix.split('.')[:-1])
        f1 = io.open(stripped_line, mode="r", encoding="utf-8")
        f2 = io.open('new_' + stripped_line, mode="w", encoding="utf-8")
        for line in f1:
            out = line
            temp = ''

            text_file = io.open(output, mode="r", encoding="utf-8-sig")
            for k in text_file:
                if k.startswith(prefix):

                    key = ''.join(k.split('=')[:-1])
                    value = ''.join(k.split('=')[1:])
                    value = value.rstrip()

                    if value in line and len(value) > len(temp):
                        temp = '' + value
                        out = line.replace(value, '«WRITEKEY %s»' % key)
                    elif value in line and len(value) < len(temp) and value not in temp:
                        out = out.replace(value, '«WRITEKEY %s»' % key)
                        break

            text_file.close()

            f2.write(out)
        f1.close()
        f2.close()

    list_file.close()
    return


def replaceTextFreePrefix(listFile, output):
    list_file = io.open(listFile, mode="r", encoding="utf-8")

    for l in list_file:

        stripped_line = l.rstrip()

        f1 = io.open(stripped_line, mode="r", encoding="utf-8")
        f2 = io.open('new_' + stripped_line, mode="w", encoding="utf-8")
        for line in f1:
            out = line
            temp = ''

            text_file = io.open(output, mode="r", encoding="utf-8-sig")
            for k in text_file:
                key = ''.join(k.split('=')[:-1])
                value = ''.join(k.split('=')[1:])
                value = value.rstrip()

                if value in line and len(value) > len(temp):
                    temp = '' + value
                    out = line.replace(value, '«WRITEKEY %s»' % key)
                elif value in line and len(value) < len(temp) and value not in temp:
                    out = out.replace(value, '«WRITEKEY %s»' % key)
                    break

            text_file.close()

            f2.write(out)
        f1.close()
        f2.close()

    list_file.close()
    return


def scrapHtml(listFile, output):
    list_file = io.open(listFile, mode="r", encoding="utf-8")
    text_file = io.open(output, mode="w", encoding="utf-8-sig")
    for l in list_file:
        stripped_line = l.rstrip()
        a_file = io.open(stripped_line, mode="r", encoding="utf-8-sig")

        html = a_file.read()
        html = html.replace("<br>", "<br> \n")
        html = html.replace("</br>", "<br> \n")
        html = html.replace("<br/>", "<br/> \n")
        soup = BeautifulSoup(html, features="html.parser")

        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()  # rip it out

        # get text
        text = soup.get_text()
        # print(text)
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        # chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        # text = '\n'.join(chunk for chunk in chunks if chunk)
        i = 000
        prefix = stripped_line.upper()
        prefix = ''.join(prefix.split('.')[:-1])
        for line in lines:
            if line:
                txt = ''.join(line)
                txt = txt.replace('*', '')
                txt = txt.replace('(1)', '')
                txt = txt.replace('(2)', '')
                txt = txt.replace('(3)', '')
                txt = txt.replace('(4)', '')
                i += 1
                out = prefix
                out += ("_%s=" % i)
                out += txt + "\n"
                # print(out)
                text_file.write(out)
            txt = ''
            out = ''
        a_file.close()
    text_file.close()
    return


def scrapHtmlOnePrefix(listFile, output, azPrefix):
    i = 000
    list_file = io.open(listFile, mode="r", encoding="utf-8")
    text_file = io.open(output, mode="w", encoding="utf-8-sig")
    prefix = azPrefix
    for l in list_file:
        stripped_line = l.rstrip()
        a_file = io.open(stripped_line, mode="r", encoding="utf-8-sig")

        html = a_file.read()
        html = html.replace("<br>", "<br> \n")
        html = html.replace("</br>", "<br> \n")
        html = html.replace("<br/>", "<br/> \n")
        soup = BeautifulSoup(html, features="html.parser")

        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()  # rip it out

        # get text
        text = soup.get_text()
        # print(text)
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        # chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        # text = '\n'.join(chunk for chunk in chunks if chunk)


        for line in lines:
            if line:
                txt = ''.join(line)
                txt = txt.replace('*', '')
                txt = txt.replace('(1)', '')
                txt = txt.replace('(2)', '')
                txt = txt.replace('(3)', '')
                txt = txt.replace('(4)', '')
                txt = txt.replace('details', '')
                i += 1
                out = prefix
                out += ("_%s=" % i)
                out += txt + "\n"
                # print(out)
                text_file.write(out)
            txt = ''
            out = ''
        a_file.close()
    text_file.close()
    return


def deleteDouble(output, keyFile):
    lines_seen = set()  # holds lines already seen
    outfile = io.open(output, mode="w", encoding="utf-8-sig")
    duplicate = io.open("duplicate.txt", mode="w", encoding="utf-8-sig")
    for line in io.open(keyFile, mode="r", encoding="utf-8-sig"):
        dup = False
        for l in lines_seen:  # not a duplicate
            temp = line.split('_')
            temp.pop()
            prefix = ''.join(temp)
            value = ''.join(line.split('=')[1:])
            temp = l.split('_')
            temp.pop()
            prefixl = ''.join(temp)
            valuel = ''.join(l.split('=')[1:])
            # print('prefixl : '+prefixl)
            # print('prefix : '+prefix)
            if prefixl == prefix and value == valuel:
                duplicate.write(line)
                dup = True
        if not dup:
            outfile.write(line)
            lines_seen.add(line)

    outfile.close()

    return


def deleteDoubleFreePrefix(output, keyFile):
    lines_seen = set()  # holds lines already seen
    outfile = io.open(output, mode="w",encoding="utf-8-sig")
    duplicate = io.open("duplicate.txt", mode="w",encoding="utf-8-sig")
    for line in io.open(keyFile, mode="r", encoding="utf-8-sig"):
        dup = False
        for l in lines_seen:  # not a duplicate
            temp = line.split('_')
            temp.pop()
            value = ''.join(line.split('=')[1:])
            temp = l.split('_')
            temp.pop()
            valuel = ''.join(l.split('=')[1:])
            if value == valuel:
                duplicate.write(line)
                dup = True
        if not dup:
            outfile.write(line)
            lines_seen.add(line)

    outfile.close()

    return


def unused(listFile, keyfile, output):
    unused_key = open("unused.txt", "w")
    list_file = io.open(listFile, mode="r", encoding="utf-8")
    key_file = io.open(output, mode="r", encoding="utf-8-sig")
    out_file = io.open(output, mode="w", encoding="utf-8-sig")
    for l in list_file:
        stripped_line = l.rstrip()
        a_file = io.open(stripped_line, mode="r", encoding="utf-8-sig")
        key_file = io.open(output, mode="r", encoding="utf-8-sig")
        prefix = stripped_line.upper()
        prefix = ''.join(prefix.split('.')[:-1])
        for k in key_file:
            if k.startswith(prefix):
                html = a_file.read()
                key = ''.join(k.split('=')[:-1])
                if key not in html:
                    unused_key.write(k)
                else:
                    out_file.write(k)

    return


### Main ###

mode = 0
listFile = 'list.txt'
output = 'output.txt'
keyfile = ''
prefix = 'BLOOBIZ'

mode = sys.argv[1]
listFile = sys.argv[2]
output = sys.argv[3]
# keyfile= sys.argv[4]
if mode == '0':
    print('Mode 0 : create keys and replace')
    keyfile = 'keyfile.txt'
    scrapHtml(listFile, keyfile)
    print("File(s) scraped and keys created ")
    deleteDouble(output, keyfile)
    print("duplicate keys deleted and stored in duplicate.txt")
    replaceText(listFile, output)
    print("Keys replaced in text")
    os.remove(keyfile)
    print("temporary key file removed")
elif mode == '1' and keyfile != '':
    print('Mode 1 : sort unused keys')
    unused(listFile, keyfile, output)
    print('unused key sorted')
elif mode == '1' and keyfile == '':
    print('error : no keyfile ')
elif mode == '2':
    print('Mode 2 : create keys and replace with oner prefix ')
    keyfile = 'keyfile.txt'
    scrapHtmlOnePrefix(listFile, keyfile, prefix)
    print("File(s) scraped and keys created ")
    deleteDoubleFreePrefix(output, keyfile)
    print("duplicate keys deleted and stored in duplicate.txt")
    replaceTextFreePrefix(listFile, output)
    print("Keys replaced in text")
    os.remove(keyfile)
    print("temporary key file removed")

else:
    print('error : unkown mode ')
now = datetime.now()
print('End ', now)
