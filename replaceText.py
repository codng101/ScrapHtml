import io

list_file = io.open("list.txt", mode="r", encoding="utf-8")

for l in list_file:

    stripped_line = l.rstrip()
    prefix = stripped_line.upper()
    prefix = ''.join(prefix.split('.')[:-1])
    f1 = io.open(stripped_line, mode="r", encoding="utf-8")
    f2 = io.open('new_' + stripped_line, mode="w", encoding="utf-8")
    for line in f1:
        out = line
        temp = ''

        text_file = io.open("Output.txt", mode="r", encoding="utf-8-sig")
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
