f = open('requirements_origin.txt', 'r')
lines = f.readlines()
f.close()

new_file = []
for line in lines:
    if line[0] == '#':
        continue
    parts = line.strip('\n').split('=')

    new_line = parts[0] + '==' + parts[1] + '\n'
    new_file.append(new_line)

new_f = open('requirements.txt', 'w+')
for line in new_file:
    new_f.write(line)

new_f.write('guincorn==20.0.4\n')
new_f.close()
